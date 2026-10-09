#!/usr/bin/env python3
"""Prepare an isolated recipe and commands without running Blender or FFmpeg."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import sys

SKILL = Path(__file__).resolve().parents[1]
SOURCE = SKILL / 'assets/recipe'
sys.path.insert(0, str(SOURCE))
from recipe_io import cache_snapshot, fresh_output, sha


def tool(value):
    found = shutil.which(str(Path(value).expanduser()))
    if not found:
        raise ValueError('Executable not found: ' + value)
    return str(Path(found).resolve())


def prepare(args):
    output = fresh_output(args.output)
    if not 1 <= args.scale <= 4 or args.samples < 1:
        raise ValueError('Use scale 1–4 and positive samples')
    blender, ffmpeg = tool(args.blender), tool(args.ffmpeg)
    simulation = output / 'simulation' if args.rebake else args.simulation.expanduser().resolve()
    if output.is_relative_to(simulation):
        raise ValueError('Keep output outside the input simulation')
    cache = {}
    if not args.rebake:
        for frame in range(1, 181):
            mesh = simulation / 'cache/mesh' / f'fluid_mesh_{frame:04d}.bobj.gz'
            if not mesh.is_file():
                raise FileNotFoundError('Missing cached mesh: ' + str(mesh))
        cache = cache_snapshot(simulation)
    sources = {p.name: sha(p) for p in sorted(SOURCE.glob('*.py'))}
    output.mkdir(parents=True, exist_ok=False)
    recipe = output / 'recipe'
    recipe.mkdir()
    for name in sources:
        shutil.copy2(SOURCE / name, recipe / name)
    env = ['env', 'CYCLES_METAL_DISABLE_BINARY_ARCHIVES=1'] if args.device == 'METAL' else []
    base = env + [blender, '-b', '--factory-startup', '--python-exit-code', '1', '-P']
    commands = ['# Prepared only. Inspect probes before running full sequences.']
    if args.rebake:
        commands += ['# Bake first:', shlex.join(base + [str(recipe/'build_fall.py'), '--', '--output', str(simulation)])]
    def render(mode, frames):
        return shlex.join(base + [str(recipe/'render_flow.py'), '--', '--simulation', str(simulation),
                          '--output', str(output/mode), '--mode', mode, '--frames', frames,
                          '--scale', str(args.scale), '--samples', str(args.samples), '--device', args.device])
    commands += ['# Probes:', render('cold', '1,30,90,162,180'), render('hot', '30,90'),
                 '# Full sequences:', render('cold', '1:181'), render('hot', '1:181'),
                 '# Encode each completed sequence into a fresh media folder:']
    for mode in ['cold', 'hot']:
        commands.append(shlex.join([sys.executable, str(recipe/'encode_water.py'), '--frames', str(output/mode),
                                   '--output', str(output/'media'/mode), '--ffmpeg', ffmpeg]))
    (output/'commands.txt').write_text('\n'.join(commands)+'\n')
    spec = {'schema': 1, 'prepared_only': True, 'render_executed': False,
            'resolution': [480*args.scale,1800*args.scale], 'samples': args.samples,
            'fps': 30, 'frames': 180, 'simulation': str(simulation), 'rebake_required': args.rebake,
            'source_hashes': sources, 'cache_meshes': cache, 'device': args.device,
            'blender': blender, 'ffmpeg': ffmpeg}
    (output/'job.json').write_text(json.dumps(spec,indent=2)+'\n')
    return {'output': str(output), 'resolution': spec['resolution'],
            'cache_meshes_pinned': len(cache), 'render_executed': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--simulation',type=Path)
    source.add_argument('--rebake',action='store_true')
    p.add_argument('--scale',type=int,default=1)
    p.add_argument('--samples',type=int,default=128)
    p.add_argument('--device',choices=['CPU','METAL','CUDA','OPTIX','HIP','ONEAPI'],default='CPU')
    p.add_argument('--blender',default='blender')
    p.add_argument('--ffmpeg',default='ffmpeg')
    args = p.parse_args()
    try:
        print(json.dumps(prepare(args),indent=2))
    except (ValueError,OSError) as error:
        p.error(str(error))

if __name__ == '__main__': main()
