"""Render two generic material studies; no simulation or source project is loaded."""
import argparse
import gzip
import math
from pathlib import Path
import struct
import sys

RECIPE = Path(__file__).resolve().parents[1] / 'assets/recipe'
sys.path.insert(0,str(RECIPE))
import bpy
from recipe_io import fresh_output
from render_flow import render


def proxy_mesh(destination):
    # Original closed folded slab used to inspect optics, NOT a FLIP bake.
    nx, ny = 64, 192
    verts, faces = [], []
    for side in range(2):
        for iy in range(ny+1):
            y = -1.07 + 2.14*iy/ny
            for ix in range(nx+1):
                x = -.31 + .62*ix/nx
                z = .04 + .026*math.sin(29*x+3*math.sin(4*y)) + .011*math.sin(63*x-11*y) + .006*math.sin(17*y+5*x)
                if side: z -= .025
                # Invert the cache reconstruction transform used by the renderer.
                verts.append((x/2.12,y/2.12,(z-.14)/2.12))
    plane=(nx+1)*(ny+1)
    for side in range(2):
        off=side*plane
        for iy in range(ny):
            for ix in range(nx):
                a=off+iy*(nx+1)+ix; b=a+1; c=a+nx+2; d=a+nx+1
                tri=[(a,b,c),(a,c,d)]
                faces.extend(tuple(reversed(f)) if side else f for f in tri)
    boundary=list(range(nx+1))+[(iy+1)*(nx+1)+nx for iy in range(ny)]
    boundary+=list(range(ny*(nx+1)+nx-1,ny*(nx+1)-1,-1))
    boundary+=[iy*(nx+1) for iy in range(ny-1,0,-1)]
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):
        faces.extend([(a,a+plane,b+plane),(a,b+plane,b)])
    data=struct.pack('<i',len(verts))+b''.join(struct.pack('<fff',*p) for p in verts)
    data+=struct.pack('<i',0)+struct.pack('<i',len(faces))+b''.join(struct.pack('<iii',*f) for f in faces)
    destination.parent.mkdir(parents=True)
    destination.write_bytes(gzip.compress(data))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--samples',type=int,default=64)
    p.add_argument('--device',choices=['CPU','METAL','CUDA','OPTIX','HIP','ONEAPI'],default='CPU')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if a.samples<1: p.error('Samples must be positive')
    out=fresh_output(a.output); out.mkdir(parents=True)
    simulation=out/'generic-proxy'
    proxy_mesh(simulation/'cache/mesh/fluid_mesh_0090.bobj.gz')
    for mode in ['cold','hot']:
        render(simulation,out/mode,mode,[90],samples=a.samples,device=a.device)
        scene=bpy.context.scene
        scene.render.image_settings.file_format='JPEG'
        scene.render.image_settings.quality=94
        bpy.data.images['Render Result'].save_render(str(out/(mode+'.jpg')),scene=scene)
    print('GENERIC_STUDY_DONE',out,flush=True)

if __name__=='__main__': main()
