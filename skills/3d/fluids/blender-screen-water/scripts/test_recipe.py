"""Exercise preparation, cache guards and a small real FFmpeg encoding."""
import argparse
import gzip
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILL/'assets/recipe'))
from recipe_io import parse_frames, read_bobj, render_output
from encode_water import encode
spec=importlib.util.spec_from_file_location('prepare_job',SKILL/'scripts/prepare_job.py')
prepare_job=importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare_job)
parser=argparse.ArgumentParser();parser.add_argument('--blender',default='blender');parser.add_argument('--ffmpeg',default='ffmpeg')
args, unittest_args=parser.parse_known_args()


def mesh(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=struct.pack('<i',3)+struct.pack('<9f',0,0,0,1,0,0,0,1,0)+struct.pack('<ii',0,1)+struct.pack('<3i',0,1,2)
    path.write_bytes(gzip.compress(data))


def png(path,colour):
    width,height=32,120
    def chunk(name,data): return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data)&0xffffffff)
    data=(b'\0'+bytes(colour)*width)*height
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(data))+chunk(b'IEND',b''))


class RecipeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='screen-water-test-');self.root=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def prepare_args(self,**changes):
        values=dict(output=self.root/'job',rebake=True,simulation=None,scale=2,samples=128,device='CPU',blender=args.blender,ffmpeg=args.ffmpeg)
        values.update(changes);return argparse.Namespace(**values)
    def test_prepare_without_execution(self):
        result=prepare_job.prepare(self.prepare_args())
        self.assertEqual(result['resolution'],[960,3600]);self.assertFalse(result['render_executed'])
        self.assertFalse((self.root/'job/simulation').exists())
        job=json.loads((self.root/'job/job.json').read_text())
        self.assertEqual(len(job['source_hashes']),5)
        with self.assertRaises(FileExistsError): prepare_job.prepare(self.prepare_args())
    def test_cache_and_refusal_before_writes(self):
        simulation=self.root/'sim'
        with self.assertRaises(FileNotFoundError): prepare_job.prepare(self.prepare_args(rebake=False,simulation=simulation))
        self.assertFalse((self.root/'job').exists())
        for i in range(1,181): mesh(simulation/'cache/mesh'/f'fluid_mesh_{i:04d}.bobj.gz')
        result=prepare_job.prepare(self.prepare_args(rebake=False,simulation=simulation))
        self.assertEqual(result['cache_meshes_pinned'],180)
    def test_invalid_preparation(self):
        for kwargs in [dict(scale=0),dict(scale=5),dict(samples=0),dict(blender='nonexistent-water-blender')]:
            with self.assertRaises(ValueError): prepare_job.prepare(self.prepare_args(**kwargs))
            self.assertFalse((self.root/'job').exists())
    def test_cache_parser_and_frame_bounds(self):
        file=self.root/'mesh.bobj.gz';mesh(file)
        vertices,faces=read_bobj(file)
        self.assertEqual(len(vertices),3);self.assertEqual(faces,[(0,1,2)])
        file.write_bytes(gzip.compress(struct.pack('<i',99)))
        with self.assertRaises(ValueError): read_bobj(file)
        self.assertEqual(parse_frames('90,1:3,90'),[1,2,90])
        for value in ['0','181','1:182','2:1']:
            with self.assertRaises(ValueError): parse_frames(value)
    def test_resume_guards(self):
        sim=self.root/'sim';file=sim/'cache/mesh/fluid_mesh_0001.bobj.gz';mesh(file)
        settings={'samples':128}
        output=render_output(self.root/'look',sim,[1],settings)
        self.assertEqual(output,render_output(output,sim,[1],settings))
        with self.assertRaises(ValueError): render_output(output,sim,[1],{'samples':64})
        (output/'water-0001.partial.png').write_bytes(b'interrupted')
        with self.assertRaises(ValueError): render_output(output,sim,[1],settings)
        (output/'water-0001.partial.png').unlink()
        file.write_bytes(file.read_bytes()+b'changed')
        with self.assertRaises(ValueError): render_output(output,sim,[1],settings)
    def test_encoder(self):
        frames=self.root/'frames';frames.mkdir();dest=self.root/'media'
        with self.assertRaises(FileNotFoundError): encode(frames,dest,args.ffmpeg)
        self.assertFalse(dest.exists())
        for i in range(1,181): png(frames/f'water-{i:04d}.png',(i,0,0))
        result=encode(frames,dest,args.ffmpeg)
        self.assertEqual(result['count'],180);self.assertEqual(len(result['decoded_hashes']),180)
        with self.assertRaises(FileExistsError): encode(frames,dest,args.ffmpeg)
        # Decode actual movie pixels. Early frames preserve the ramp; the end blends
        # toward frame 90 rather than retaining source frame 180.
        raw=subprocess.check_output([args.ffmpeg,'-v','error','-i',str(dest/'water.mp4'),'-f','rawvideo','-pix_fmt','rgb24','-'])
        self.assertEqual(len(raw),32*120*3*180)
        sample=lambda i:raw[(i-1)*32*120*3]
        self.assertLess(abs(sample(30)-30),5)
        self.assertLess(abs(sample(180)-90),8)
        self.assertLess(abs(sample(180)-sample(91)),8)

if __name__=='__main__': unittest.main(argv=[sys.argv[0]]+unittest_args)
