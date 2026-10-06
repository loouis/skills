// Run with puppeteer available, passing an output directory outside the skill.
// Exports all 76 forward frames at 25 fps plus contact, mobile and mask views.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const puppeteer = require('puppeteer');
const out = process.argv[2];
if (!out) throw new Error('Usage: node demo/verify.cjs <output-directory>');
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage(), errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(path.join(__dirname, 'index.html')).href);
    const report = await page.evaluate(async () => {
      const demo = window.vectorMaskDemo;
      async function raster(source) {
        const svg = document.getElementById('art').cloneNode(true);
        svg.setAttribute('width', 600); svg.setAttribute('height', 420);
        const url = URL.createObjectURL(new Blob([source || new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' }));
        try {
          const img = new Image(); img.src = url; await img.decode();
          const canvas = document.createElement('canvas'); canvas.width=600; canvas.height=420;
          const ctx = canvas.getContext('2d'); ctx.drawImage(img,0,0);
          return ctx.getImageData(0,0,600,420).data;
        } finally { URL.revokeObjectURL(url); }
      }
      function diff(a,b) {
        let changed=0,max=0;
        for(let i=0;i<a.length;i+=4) {
          // Transparent RGB is undefined; compare premultiplied RGBA.
          let delta=Math.abs(a[i+3]-b[i+3]);
          for(let c=0;c<3;c++) delta=Math.max(delta,Math.abs(a[i+c]*a[i+3]/255-b[i+c]*b[i+3]/255));
          if(delta>0) changed++;
          max=Math.max(max,delta);
        }
        return {changed,max};
      }
      demo.seek(0);
      const closed=await raster();
      const front=await raster('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="420" viewBox="0 0 600 420"><rect x="230" y="90" width="140" height="240" fill="none" stroke="#233d39" stroke-width="6"/></svg>');
      const result={closed:diff(closed,front),variants:[],interiorLeaks:0,travelGaps:0};
      for(const gap of [8,14]) {
        demo.setGap(gap);
        demo.seek(75,{masked:true}); const masked=await raster();
        demo.seek(75); const original=await raster();
        result.variants.push({gap,handover:diff(masked,original)});
        for(let frame=0;frame<=75;frame++) {
          const state=demo.seek(frame,{masked:true});
          const pixels=await raster();
          // A rear outline must never be visible inside the foreground piece.
          for(let y=95;y<325;y++) for(let x=235;x<365;x++) {
            if(pixels[(y*600+x)*4+3]!==0) result.interiorLeaks++;
          }
          // Once exposed, travel must have continuous opaque top ink into the front line.
          if(state.phase==='Travel' && state.left.x>40) {
            for(const x of [225,226,227,228,371,372,373,374]) {
              if(pixels[(90*600+x)*4+3]<250) result.travelGaps++;
            }
          }
        }
      }
      demo.setGap(8); demo.seek(0);
      return result;
    });
    assert.deepEqual(report.closed,{changed:0,max:0},'Closed pose must equal the foreground alone');
    assert.equal(report.interiorLeaks,0,'Rear lines leaked through the foreground');
    assert.equal(report.travelGaps,0,'Travel must remain flush');
    // These rect/arc fixtures should match exactly, including their clipped line endings.
    for(const variant of report.variants) assert.deepEqual(variant.handover,{changed:0,max:0},`Gap ${variant.gap} handover`);
    const art=await page.$('#art');
    for(let frame=0;frame<=75;frame++) {
      await page.evaluate(frame=>window.vectorMaskDemo.seek(frame),frame);
      await art.screenshot({path:path.join(out,`frame-${String(frame).padStart(2,'0')}.png`)});
    }
    await page.click('#compare');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().showOriginal),false);
    await page.click('#compare');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().showOriginal),true);
    await page.click('#inspect');
    await page.screenshot({path:path.join(out,'mask.png')});
    await page.click('#inspect');
    await page.click('#reverse');
    await page.waitForFunction(()=>window.vectorMaskDemo.state().frame===0,{timeout:10000});
    await page.click('#play');
    await page.waitForFunction(()=>window.vectorMaskDemo.state().frame===75,{timeout:10000});
    await page.focus('#scrub'); await page.keyboard.press('Home');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().frame),0);
    await page.keyboard.press('End');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().frame),75);
    await page.setViewport({width:390,height:844,deviceScaleFactor:1});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'Mobile overflow');
    await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
    await page.emulateMediaFeatures([{name:'prefers-reduced-motion',value:'reduce'}]);
    await page.reload();
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().showOriginal),true);
    await page.click('#reverse');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().frame),0);
    await page.click('#play');
    assert.equal(await page.evaluate(()=>window.vectorMaskDemo.state().frame),75);
    assert.deepEqual(errors,[],'Browser errors');

    const sheet=await browser.newPage();
    await sheet.setViewport({width:1200,height:810,deviceScaleFactor:1});
    const frames=[0,5,10,18,25,32,39,52,75];
    await sheet.setContent(`<style>*{box-sizing:border-box}body{margin:0;padding:20px;background:#f5f3ec;color:#233d39;font:13px system-ui;display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0;border:1px solid #d2d8cf;padding:10px}img{width:100%;height:197px;object-fit:contain}figcaption{padding:6px}</style>`+frames.map(frame=>`<figure><img src="data:image/png;base64,${fs.readFileSync(path.join(out,`frame-${String(frame).padStart(2,'0')}.png`)).toString('base64')}"><figcaption>Frame ${String(frame).padStart(2,'0')} · ${(frame/25).toFixed(2)} s</figcaption></figure>`).join(''));
    await sheet.evaluate(()=>Promise.all(Array.from(document.images,img=>img.decode())));
    await sheet.screenshot({path:path.join(out,'contact-sheet.png')});
    fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({ok:true,report,frames:76,checks:['forward/reverse playback','original comparison','mask inspection','keyboard scrub','mobile layout','reduced motion','browser errors']}));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
