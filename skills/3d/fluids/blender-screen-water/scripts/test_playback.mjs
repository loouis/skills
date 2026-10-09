import assert from 'node:assert/strict';
import test from 'node:test';
import { loopFrame, arrivalOpacity, drainState, controlReturn, ScreenWaterFilm } from '../assets/water-playback.mjs';

test('arrival plays once, then only decoded frames 91–180 repeat',()=>{
  assert.equal(loopFrame(-1),1);assert.equal(loopFrame(0),1);
  assert.equal(loopFrame(5999),180);assert.equal(loopFrame(6000),91);
  assert.equal(loopFrame(8999),180);assert.equal(loopFrame(9000),91);
  assert.equal(arrivalOpacity(0),0);assert.equal(arrivalOpacity(80),.5);assert.equal(arrivalOpacity(160),1);
});
test('exit clears downwards and fully precedes control return',()=>{
  assert.equal(drainState(0).opacity,1);assert.equal(drainState(1100).opacity,0);
  assert.equal(drainState(0).boundary(240),-45);
  assert.equal(drainState(1100).boundary(240),1845);
  assert.equal(drainState(550,960,3600).boundary(480),drainState(550).boundary(240)*2);
  assert.equal(controlReturn(1100,'hot').opacity,0);assert.equal(controlReturn(1230,'cold').opacity,0);
  assert.deepEqual(controlReturn(1890,'cold'),{opacity:1,scale:1});
});
test('late play promises cannot restart a stopped film',async()=>{
  const oldDocument=globalThis.document,oldImage=globalThis.Image;
  let resolvePlay;
  const events={};
  const video={readyState:2,paused:true,currentTime:4,
    addEventListener:(type,fn)=>{events[type]=fn;},removeEventListener:type=>delete events[type],
    play(){this.paused=false;return new Promise(resolve=>{resolvePlay=resolve;});},
    pause(){this.paused=true;},removeAttribute(){},load(){}};
  globalThis.document={createElement:()=>video};
  globalThis.Image=class{complete=true;naturalWidth=480;};
  try{
    const film=new ScreenWaterFilm({src:'movie.mp4',poster:'poster.png'});
    film.sync(true);assert.equal(video.loop,false);assert.equal(video.currentTime,0);
    film.sync(false);resolvePlay();await Promise.resolve();assert.equal(video.paused,true);
    film.sync(true);events.ended();assert.equal(video.currentTime,3);
    assert.equal(film.sync(true,true),film.poster);assert.equal(video.paused,true);
    film.dispose();assert.deepEqual(events,{});
  }finally{globalThis.document=oldDocument;globalThis.Image=oldImage;}
});
