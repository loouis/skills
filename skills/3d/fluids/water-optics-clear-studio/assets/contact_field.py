"""Authored water-height field in metres, detached from the original scene.
X is lateral; the camera-facing region is negative Y; Z is up.
Reference cylinder is tilted 18 degrees around Y, translated to Z=-0.010.
This field is shape/optics art direction, not a wetting or buoyancy solver.
Scalar callers may use math functions and min/max clipping; array callers numpy.
"""
import math

def omega(w,clock):
 k=2*math.pi/w
 return math.sqrt(9.81*k+.072/1000*k**3)*clock

def pool_height(x,y,t,p,events,sin,exp,sqrt,clip):
 rr=sqrt(((x-.0035)/1.03)**2+y*y+.000001)
 z=.0008*exp(-((rr-.031)/.004)**2)
 # Preserve the attached contact shape, attenuate radial curvature outside it.
 z+=p['near_amp']*sin(2*math.pi*(rr+.003*sin(19*x+7*y))/p['near_wave']-omega(p['near_wave'],p['clock'])*t+.55)*exp(-((rr/.095)**2))
 # Main crests cross the view direction obliquely, with broad, smooth lateral variation.
 env=exp(-((rr/.62)**2))
 d1=.95*x+.24*y+.007*sin(9*x-5*y)
 d2=-.78*x+.38*y+.010*sin(6*x+4*y)
 d3=.5*x+.84*y+p.get('phase3_warp',0)*sin(20*x-2*y)
 if p.get('transverse'):
  d1=.96*x+.16*y+.005*sin(6*x-4*y)
  d2=-.86*x+.26*y+.009*sin(4*x+3*y)
  d3=.55*x+.84*y+.005*sin(20*x-2*y)
 if p.get('strong_cross'):
  d1=.99*x+.045*y+.0015*sin(6*x-4*y)
  d2=-.99*x+.10*y+.002*sin(4*x+3*y)
  env=env*(1-exp(-((rr/.10)**2)))
 z+=env*p['a1']*sin(2*math.pi*d1/p['w1']-omega(p['w1'],p['clock'])*t+1.15)
 z+=env*p['a2']*sin(2*math.pi*d2/p['w2']-omega(p['w2'],p['clock'])*t+.40)
 z+=env*p['a3']*sin(2*math.pi*d3/p['w3']-omega(p['w3'],p['clock'])*t+2.2)
 if p.get('fine_amp'):
  fine=.42*x+.91*y+.004*sin(19*x-4*y)
  z+=exp(-((rr/.50)**2))*p['fine_amp']*sin(2*math.pi*fine/p['fine_wave']-omega(p['fine_wave'],p['clock'])*t+1.3)
 for ev in events:
  a=clip(t-ev['impact'],0,3);d=sqrt((x-ev['xy'][0])**2+(y-ev['xy'][1])**2+1e-10);radius=.037*a
  rise=clip(a/.08,0,1);rise=rise*rise*(3-2*rise)
  z+=p['impact_amp']*rise*exp(-a*2.7)*exp(-((d-radius)/p['impact_width'])**2)*sin((d-radius)*2*math.pi/p['impact_wave'])
 return z

def extra(x,y,t,p,sin,exp,clip):
    # At frame48 start from a deliberate look-development phase; advance continuously.
    time=t-47/24
    gate=clip((-y-p.get('gate_start',.07))/p.get('gate_width',.07),0,1);gate=gate*gate*(3-2*gate)
    center=.025+.015*sin(y*8+.5)
    envelope=gate*exp(-((x-center)/p['width'])**4)*exp(-((y+p.get('span_center',.31))/p.get('span',.30))**4)
    # Chirped optical coordinate: intervals vary continuously, not random per frame.
    path=y+.009*sin(x*24+y*5)+p['warp1']*sin(y*13+.3)+p['warp2']*sin(y*31+1.7)+.005*sin(y*5-x*12)
    amplitude=1+p['envelope_variation']*sin(y*17+.8)+.12*sin(y*39-1.4)
    value=envelope*(amplitude*p['amp1']*sin(2*math.pi*path/p['w1']-1.802+p['speed']*time)+p['amp2']*sin(2*math.pi*(y*.9+x*.3+.013*sin(y*9-1.1))/p['w2']+.5*sin(x*23)-1.214-.41*time))
    if p.get('edge_soften'):
        a=clip((x-.015)/.040,0,1);a=a*a*a*(a*(a*6-15)+10)
        value=value*(1-p['edge_soften']*a)
    return value

def contact_level(x,y,cfg,sin,exp,sqrt,clip):
    xx=x-.0035;rr=sqrt(xx*xx+y*y+1e-12)
    front=clip(-y/rr,0,1)
    return cfg.get('water_level',0)+cfg.get('contact_level',.00015)-cfg['contact_depth']*front**2*(1+.08*sin(xx*52))

def contact_distance(x,y,cfg,sin,exp,sqrt,clip):
    h=contact_level(x,y,cfg,sin,exp,sqrt,clip)
    ct=math.cos(math.radians(18));st=math.sin(math.radians(18))
    lx=ct*x-st*(h+.010);lz=st*x+ct*(h+.010)
    points=[(.0245,0),(.0255,.003),(.0288,.006),(.029,.012)]
    profile=[]
    for i in range(16):
        a=i/15;profile.append(tuple((1-a)**3*points[0][k]+3*(1-a)**2*a*points[1][k]+3*(1-a)*a*a*points[2][k]+a**3*points[3][k]for k in [0,1]))
    radius=profile[0][0]
    for (ra,za),(rb,zb) in zip(profile[:-1],profile[1:]):radius=radius+(rb-ra)/(zb-za)*(clip(lz,za,zb)-za)
    d=sqrt(lx*lx+y*y+1e-12)-radius
    return .5*(d+sqrt(d*d+.00003**2))

def abs_value(v,sqrt):return sqrt(v*v+1e-12)

def attached_contact(x,y,cfg,sin,exp,sqrt,clip):
    d=contact_distance(x,y,cfg,sin,exp,sqrt,clip)
    xx=x-.0035;front=clip(-y/sqrt(xx*xx+y*y+1e-12),0,1)
    decay=cfg['contact_decay']+(cfg.get('front_decay',cfg['contact_decay'])-cfg['contact_decay'])*front**2
    side=clip((abs_value(x-.007,sqrt)-.032)/.034,0,1);side=side*side*side*(side*(side*6-15)+10)
    return (1-side)*(contact_level(x,y,cfg,sin,exp,sqrt,clip)-cfg.get('water_level',0))*exp(-d/decay)

def height(x,y,t,p,cfg,events,sin,exp,sqrt,clip):
    time=t-47/24;d=contact_distance(x,y,cfg,sin,exp,sqrt,clip)
    gate=clip(d/.009,0,1);gate=gate*gate*(3-2*gate)
    rr=sqrt(((x-.0035)/1.03)**2+y*y+.000001)
    background=pool_height(x,y,47/24+time*cfg.get('base_time_scale',.45),cfg,events,sin,exp,sqrt,clip)-.0008*exp(-((rr-.031)/.004)**2)
    z=cfg.get('water_level',0)+background*gate+attached_contact(x,y,cfg,sin,exp,sqrt,clip)
    # Unequal local wave shoulders, continuously warped in space. No concentric stack.
    asym=1+cfg.get('contact_asymmetry',.24)*sin(x*48+y*27+.3)
    path=d+.0025*sin(x*65+y*39)+.0014*sin(y*98-x*27+1.1)
    crest=cfg['contact_crest']*asym*exp(-((path-cfg.get('crest_offset',.008))/cfg.get('crest_width',.005))**2)
    phase=2*math.pi*(path+.09*d*sin(x*40-y*17))/cfg.get('contact_wave',.043)-cfg.get('contact_speed',1.4)*time+.6
    ripple=cfg.get('contact_ripple',.00007)*asym*exp(-d/.032)*exp(-(d/.080)**4)*sin(phase)
    z+=gate*(crest+ripple)
    use=p if p is not None else cfg.get('shared_extra')
    if use is not None:
        optical_gate=clip(d/.004,0,1);optical_gate=optical_gate*optical_gate*(3-2*optical_gate)
        shared=1
        if p is None:
            f=clip((d-.100)/.080,0,1);f=f*f*f*(f*(f*6-15)+10);shared=1-f
        boost=1+cfg.get('near_optical_boost',0)*exp(-((y+.070)/.100)**4)
        optical_y=y+cfg.get('near_phase_shift',0)*exp(-((y+.070)/.100)**4)
        z+=boost*shared*optical_gate*extra(x,optical_y,t,use,sin,exp,clip)
    return z

def evaluate(x,y,t,settings,quiet=False):
    """Evaluate with NumPy (bundled with Blender); t is seconds, frame 48 = 47/24."""
    import numpy as np
    return height(x,y,t,None if quiet else settings['extra'],settings['base'],[],np.sin,np.exp,np.sqrt,np.clip)

def gain(top_row,start=.725,end=.840,far=.75):
    """Fixed-camera composition gain for top-origin normalized rows, not Fresnel."""
    import numpy as np
    v=np.clip((top_row-start)/(end-start),0,1)
    return 1+(far-1)*v*v*v*(v*(v*6-15)+10)

def compose(quiet,beauty,no_reflection,top_row):
    """Scene-linear RGB arrays with broadcast-compatible top_row; no coordinate warp."""
    return quiet+gain(top_row)*(beauty-no_reflection)
