"""Numerical invariants for the portable field; run with Blender's Python or Python + NumPy."""
import importlib.util,json,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('field',ROOT/'assets/contact_field.py');f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
C=json.loads((ROOT/'assets/contact-settings.json').read_text())
class FieldTest(unittest.TestCase):
    def test_closed_contact_direction(self):
        fun=lambda x,y:f.contact_level(x,y,C['base'],np.sin,np.exp,np.sqrt,np.clip)
        self.assertLess(fun(.0035,-.029),fun(.032,0)-.002)
    def test_finite_and_quiet_far(self):
        x,y=np.meshgrid(np.linspace(-1,1,151),np.linspace(-1,1,151))
        for t in [0,.5,1,1.5,47/24]:
            z=f.evaluate(x,y,t,C);self.assertTrue(np.isfinite(z).all());self.assertLess(np.max(np.abs(z-.007)),.004)
        self.assertAlmostEqual(float(f.evaluate(2.,2.,47/24,C)),.007,places=8)
    def test_plates_agree_at_contact(self):
        x,y=np.meshgrid(np.linspace(-.06,.06,81),np.linspace(-.08,.05,81))
        np.testing.assert_allclose(f.evaluate(x,y,47/24,C),f.evaluate(x,y,47/24,C,quiet=True),atol=1e-12)
    def test_temporal_continuity(self):
        x=np.linspace(-.15,.15,113);y=np.linspace(-.8,.1,113)
        self.assertLess(np.max(np.abs(f.evaluate(x,y,1,C)-f.evaluate(x,y,1+1e-5,C))),1e-7)
    def test_composition_gain(self):
        a=f.gain(np.linspace(0,1,2001));self.assertTrue(np.all(np.diff(a)<=1e-12));self.assertEqual(a[0],1);self.assertEqual(a[-1],.75)
        q=np.ones((5,2,3))*.2;b=np.ones_like(q)*.6;n=np.ones_like(q)*.3;r=np.linspace(0,1,5)[:,None,None]
        result=f.compose(q,b,n,r);np.testing.assert_allclose(result[0],.5);np.testing.assert_allclose(result[-1],.425)
    def test_no_fine_ripple(self):self.assertEqual(C['base']['fine_amp'],0)
if __name__=='__main__':unittest.main(argv=['test_field'])
