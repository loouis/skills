"""Encode 180 source frames with a forward-only 3–6 second repeat section."""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess
from recipe_io import fresh_output, sha

FILTER = '[0:v]split[a][b];[b]trim=start_frame=72:end_frame=90,setpts=PTS-STARTPTS[head];[a][head]xfade=transition=custom:duration=0.6:offset=5.4:expr=A*(0.5-0.5*cos(PI*P))+B*(0.5+0.5*cos(PI*P)),format=yuv420p[v]'


def png_size(path):
    with path.open('rb') as stream:
        header = stream.read(24)
    if header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
        raise ValueError('Not a PNG: ' + str(path))
    return struct.unpack('>II', header[16:24])


def encode(frame_dir, destination, ffmpeg='ffmpeg'):
    output = fresh_output(destination)
    frame_dir = Path(frame_dir).expanduser().resolve()
    if output.is_relative_to(frame_dir):
        raise ValueError('Keep encoded output separate from source frames')
    executable = shutil.which(str(Path(ffmpeg).expanduser()))
    if not executable:
        raise ValueError('FFmpeg executable not found')
    frames = [frame_dir/f'water-{i:04d}.png' for i in range(1,181)]
    if not all(p.is_file() for p in frames):
        raise FileNotFoundError('Finish all 180 source frames before encoding')
    sizes = {png_size(p) for p in frames}
    if len(sizes) != 1 or any(v <= 0 or v % 2 for v in next(iter(sizes))):
        raise ValueError('Frames must have one consistent, positive, even pixel size')
    hashes = {p.name: sha(p) for p in frames}
    output.mkdir(parents=True,exist_ok=False)
    movie = output/'water.mp4'
    subprocess.run([executable,'-v','error','-n','-framerate','30','-start_number','1',
                    '-i',str(frame_dir/'water-%04d.png'),'-filter_complex',FILTER,'-map','[v]',
                    '-frames:v','180','-c:v','libx264','-crf','15','-preset','slow',
                    '-movflags','+faststart',str(movie)],check=True)
    subprocess.run([executable,'-v','error','-n','-i',str(movie),'-frames:v','180',
                    str(output/'frame-%03d.png')],check=True)
    decoded = [output/f'frame-{i:03d}.png' for i in range(1,181)]
    if not all(p.is_file() for p in decoded):
        raise RuntimeError('Decode did not produce 180 frames')
    if any(sha(p) != hashes[p.name] for p in frames):
        raise RuntimeError('Source changed during encoding; preserve this failed revision and create a new one')
    manifest = {'fps':30,'duration':6,'count':180,'size':list(next(iter(sizes))),
                'loop_start':3,'loop_duration':3,'blend_duration':.6,
                'source_hashes':hashes,'movie_sha256':sha(movie),
                'decoded_hashes':{p.name:sha(p) for p in decoded},'filter':FILTER}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frames',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--ffmpeg',default='ffmpeg')
    a = p.parse_args()
    encode(a.frames,a.output,a.ffmpeg)

if __name__ == '__main__': main()
