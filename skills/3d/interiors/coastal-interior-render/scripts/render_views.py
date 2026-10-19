"""Render an existing blend from an explicit camera manifest. Run inside Blender."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def validate_views(data, camera_names):
    views = data.get('views')
    if not isinstance(views, list) or not views:
        raise ValueError('Manifest requires a nonempty views list')
    seen = set()
    for view in views:
        slug = view.get('slug', '')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', slug) or slug in seen:
            raise ValueError('Invalid or duplicate slug: ' + repr(slug))
        seen.add(slug)
        if view.get('camera') not in camera_names:
            raise ValueError('Unknown camera: ' + repr(view.get('camera')))
        for key in ('width', 'height', 'samples'):
            value = view.get(key)
            if type(value) is not int or value < 1:
                raise ValueError(f'{slug}: {key} must be a positive integer')
    return views


def main():
    import bpy
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--device', default='CPU', choices=['CPU', 'METAL', 'CUDA', 'OPTIX', 'HIP', 'ONEAPI'])
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    source = args.scene.expanduser().resolve(strict=True)
    manifest = args.manifest.expanduser().resolve(strict=True)
    output = args.output.expanduser().resolve()
    if output.exists():
        raise FileExistsError('Choose a fresh output directory: ' + str(output))
    original_hash = digest(source)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene = bpy.context.scene
    # Blender can embed the full .blend path in PNG text even with visual stamps off.
    scene.render.use_stamp_filename = False
    if hasattr(scene.render, 'use_stamp_hostname'):
        scene.render.use_stamp_hostname = False
    views = validate_views(json.loads(manifest.read_text()), {o.name for o in scene.objects if o.type == 'CAMERA'})
    scene.render.engine = 'CYCLES'
    if args.device == 'CPU':
        scene.cycles.device = 'CPU'
    else:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = args.device
        prefs.get_devices()
        devices = [d for d in prefs.devices if d.type == args.device]
        if not devices:
            raise RuntimeError('Requested GPU backend has no devices: ' + args.device)
        for device in prefs.devices:
            device.use = device in devices
        scene.cycles.device = 'GPU'
    output.mkdir(parents=True)
    report = {'scene_sha256': original_hash, 'input_manifest_sha256': digest(manifest),
              'blender': bpy.app.version_string, 'device': args.device,
              'colour': {'transform': scene.view_settings.view_transform, 'look': scene.view_settings.look,
                         'exposure': scene.view_settings.exposure, 'gamma': scene.view_settings.gamma},
              'denoising': bool(scene.cycles.use_denoising),
              'compositing_enabled': bool(scene.render.use_compositing),
              'filename_metadata': False, 'outputs': [], 'complete': False}
    def save_report():
        (output / 'render-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    save_report()
    for view in views:
        camera = scene.objects[view['camera']]
        scene.camera = camera
        scene.render.resolution_x = view['width']
        scene.render.resolution_y = view['height']
        scene.render.resolution_percentage = 100
        scene.render.use_border = False
        scene.render.use_crop_to_border = False
        scene.cycles.samples = view['samples']
        scene.render.image_settings.file_format = 'PNG'
        pending = output / (view['slug'] + '.pending.png')
        target = output / (view['slug'] + '.png')
        scene.render.filepath = str(pending)
        bpy.ops.render.render(write_still=True)
        if not pending.is_file() or pending.stat().st_size < 100:
            raise RuntimeError('Missing/empty render: ' + str(pending))
        # Verify the file itself, not Render Result's potentially released buffer.
        check = bpy.data.images.load(str(pending), check_existing=False)
        size = list(check.size)
        bpy.data.images.remove(check)
        if size != [view['width'], view['height']]:
            raise RuntimeError('Unexpected image size: ' + repr(size))
        pending.rename(target)
        record = dict(view, file=target.name, sha256=digest(target),
                      lens=camera.data.lens, sensor_width=camera.data.sensor_width,
                      matrix_world=[list(row) for row in camera.matrix_world])
        report['outputs'].append(record)
        save_report()
        print('CAMERA_RENDER_COMPLETE', view['slug'], record['sha256'], flush=True)
    if digest(source) != original_hash:
        raise RuntimeError('Source scene changed while rendering; investigate concurrent writes')
    report['complete'] = True
    save_report()
    print('RENDER_SET_COMPLETE', len(views), flush=True)


if __name__ == '__main__':
    main()
