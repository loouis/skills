// node scripts/verify_demo.cjs <fresh-output-directory>; needs Puppeteer and FFmpeg.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url'),{execFileSync}=require('node:child_process');
const puppeteer=require('puppeteer');
const skill=path.resolve(__dirname,'..'),out=process.argv[2];
if(!out||fs.existsSync(out)) throw new Error('Supply a fresh output directory');
fs.mkdirSync(out,{recursive:true});
execFileSync(process.env.FFMPEG||'ffmpeg',['-v','error','-n','-f','lavfi','-i','color=c=black:s=32x120:r=30:d=6','-c:v','libx264','-pix_fmt','yuv420p',path.join(out,'fixture.mp4')]);
(async()=>{
 const browser=await puppeteer.launch({headless:true});
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.setViewport({width:1280,height:720,deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(skill,'demo/index.html')).href);
  await page.evaluate(()=>Promise.all(Array.from(document.images,i=>i.decode())));
  assert.deepEqual(await page.evaluate(()=>Array.from(document.images,i=>[i.naturalWidth,i.naturalHeight])),[[480,1800],[480,1800]]);
  assert.equal(await page.evaluate(()=>document.querySelector('footer').getBoundingClientRect().bottom<=innerHeight),true);
  await page.click('#detail');assert.equal(await page.$eval('#detail',e=>e.getAttribute('aria-pressed')),'true');
  await page.screenshot({path:path.join(out,'detail.png')});await page.click('#detail');
  await page.focus('#time');await page.keyboard.press('Home');assert.match(await page.$eval('#frame',e=>e.textContent),/Frame 1 \/ 180/);
  await page.keyboard.press('End');assert.match(await page.$eval('#frame',e=>e.textContent),/Frame 91 \/ 180/);
  await page.setViewport({width:390,height:844,deviceScaleFactor:1});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
  const source=fs.readFileSync(path.join(skill,'assets/water-playback.mjs')).toString('base64');
  const src='data:video/mp4;base64,'+fs.readFileSync(path.join(out,'fixture.mp4')).toString('base64');
  const poster='data:image/jpeg;base64,'+fs.readFileSync(path.join(skill,'demo/cold.jpg')).toString('base64');
  await page.evaluate(async({source,src,poster})=>{
   const {ScreenWaterFilm}=await import('data:text/javascript;base64,'+source);
   window.checkFilm=new ScreenWaterFilm({src,poster});checkFilm.sync(true);
  },{source,src,poster});
  await page.waitForFunction(()=>checkFilm.video.readyState>=2&&!checkFilm.video.paused);
  await page.evaluate(()=>{checkFilm.video.currentTime=5.95;});
  await page.waitForFunction(()=>checkFilm.video.currentTime>=3&&checkFilm.video.currentTime<4);
  await page.waitForFunction(()=>checkFilm.poster.complete&&checkFilm.poster.naturalWidth>0);
  assert.equal(await page.evaluate(()=>checkFilm.sync(true,true)===checkFilm.poster&&checkFilm.video.paused),true);
  await page.evaluate(()=>checkFilm.dispose());assert.deepEqual(errors,[]);
  console.log('ok: native images, desktop/mobile layout, detail toggle, keyboard mapping, actual media loop, reduced-motion poster and cleanup');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
