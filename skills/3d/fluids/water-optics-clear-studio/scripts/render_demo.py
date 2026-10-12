"""Run in Blender: -b --python-exit-code 1 -P scripts/render_demo.py -- --output NEW_DIRECTORY.
Builds fresh generic optical benches. Does not load or modify an existing scene.
"""
import argparse,hashlib,importlib.util,json,sys,time
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('optics',ROOT/'assets/optics.py')
optics=importlib.util.module_from_spec(sp);sp.loader.exec_module(optics)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--specimen',choices=['all','droplet','cavity','fold'],default='all')
    parser.add_argument('--size',type=int,default=640)
    parser.add_argument('--samples',type=int,default=256)
    parser.add_argument('--seconds',type=float,default=45)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.size<16 or args.samples<1 or args.seconds<0:parser.error('Invalid render limits')
    out=args.output.expanduser().resolve()
    if out.is_relative_to(ROOT):parser.error('Render to a new directory outside the skill')
    out.mkdir(parents=True,exist_ok=False)
    settings=json.loads((ROOT/'assets/optics-settings.json').read_text())
    specimens=list(settings) if args.specimen=='all' else [args.specimen]
    records=[]
    for name in specimens:
        folder=out/name;folder.mkdir()
        cfg=settings[name];s=optics.setup(cfg,args.size,args.samples,name,'')
        s.cycles.time_limit=args.seconds;s.render.threads_mode='FIXED';s.render.threads=8
        s.cycles.denoiser='OPENIMAGEDENOISE';s.cycles.denoising_input_passes='RGB_ALBEDO_NORMAL';s.cycles.denoising_prefilter='ACCURATE'
        s.render.filepath=str(folder/'beauty.png');optics.raw_output(s,folder,'same-render')
        before=optics.audit(s)
        assert before and all(v['nonmanifold_edges']==0 for v in before.values())
        expected_sign=-1 if name=='cavity' else 1
        key=next(k for k in before if k.startswith('Air cavity')) if name=='cavity' else next(iter(before))
        assert before[key]['signed_volume']*expected_sign>0
        scene=folder/'scene.blend';bpy.ops.wm.save_as_mainfile(filepath=str(scene),compress=True)
        bpy.ops.wm.open_mainfile(filepath=str(scene));s=bpy.context.scene
        assert optics.audit(s)==before
        assert json.loads(s['optics_effective_config'])==cfg
        assert s.cycles.device=='CPU' and s.cycles.samples==args.samples and s.render.resolution_x==args.size
        glass=next(m for m in bpy.data.materials if m.name.startswith('Water |')).node_tree.nodes
        glass=next(n for n in glass if n.type=='BSDF_GLASS')
        assert glass.inputs['IOR'].default_value>1.3329 and glass.inputs['IOR'].default_value<1.3331
        start=time.monotonic();bpy.ops.render.render(write_still=True)
        raw=list(folder.glob('same-render-raw-*.png'));assert len(raw)==1
        rec={'specimen':name,'method':'Fresh prescribed optical still; no fluid solve or animation','device':'CPU','blender':bpy.app.version_string,'size':args.size,'samples_ceiling':args.samples,'time_limit':args.seconds,'seconds':round(time.monotonic()-start,2),'geometry':before,'saved_reopen_checks':'passed','source_sha256':sha(ROOT/'assets/optics.py'),'config':cfg,'outputs':{p.name:sha(p) for p in [scene,folder/'beauty.png',*raw]}}
        (folder/'record.json').write_text(json.dumps(rec,indent=2)+'\n');records.append(rec)
        print('SPECIMEN_DONE',name,flush=True)
    (out/'validation.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
