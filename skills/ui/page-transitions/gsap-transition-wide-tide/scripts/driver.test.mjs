import assert from 'node:assert/strict';
import test from 'node:test';
import { createDriver, settleWithin } from '../assets/core/driver.mjs';

const flush = async () => { for (let i = 0; i < 12; i++) await Promise.resolve(); };
function setup(reduced = false) {
  const jobs = [], phases = [], paints = [];
  const gsap = { to(target, vars) {
    assert.equal(vars.ease, 'none');
    const job = { killed: false, vars, kill() { this.killed = true; }, complete() {
      assert.equal(this.killed, false); target.time = vars.time; vars.onUpdate(); vars.onComplete();
    } }; jobs.push(job); return job;
  } };
  const driver = createDriver({ gsap, paint: t => paints.push(t), onPhase: p => phases.push(p), reducedMotion: () => reduced });
  return { driver, jobs, phases, paints };
}

test('loading and cover run together; readiness holds at cover; reveal lasts 1.25s', async () => {
  const { driver, jobs, phases } = setup();
  let loaded, ready, swapped = 0;
  const navigation = driver.run({ load: () => new Promise(r => { loaded = r; }), swap: () => { swapped++; }, ready: () => new Promise(r => { ready = r; }) });
  assert.equal(jobs[0].vars.duration, 1);
  jobs[0].complete(); await flush();
  assert.equal(phases.at(-1), 'hold'); assert.equal(swapped, 0);
  loaded('next'); await flush(); assert.equal(swapped, 1); assert.equal(jobs.length, 1);
  ready(); await flush(); assert.equal(jobs[1].vars.duration, 1.25);
  jobs[1].complete(); assert.equal(await navigation, true); assert.equal(phases.at(-1), 'idle');
});

test('repeat navigation cancels an old cover without hanging its promise', async () => {
  const { driver, jobs } = setup();
  const first = driver.begin(); const second = driver.begin();
  assert.equal(jobs[0].killed, true); assert.equal(await first.covered, false);
  assert.equal(first.signal.aborted, true);
  jobs[1].complete(); assert.equal(await second.covered, true);
  second.cancel(); assert.equal(await second.reveal(), false);
});

test('aborted and stale loads cannot swap; load failures release the cover', async () => {
  const { driver, jobs, phases } = setup();
  let load, swaps = 0;
  const old = driver.run({ load: () => new Promise(r => { load = r; }), swap: () => swaps++ });
  await flush();
  const newer = driver.begin(); assert.equal(await old, false); load(); assert.equal(swaps, 0);
  newer.cancel(); assert.equal(jobs[1].killed, true);
  await assert.rejects(driver.run({ load: () => Promise.reject(new Error('load failed')), swap: () => swaps++ }), /load failed/);
  assert.equal(phases.at(-1), 'idle');
  const aborter = new AbortController(); aborter.abort();
  const session = driver.begin(aborter.signal); assert.equal(await session.covered, false);
});

test('reduced motion navigates immediately and preference changes settle active motion', async () => {
  const reduced = setup(true); let swapped = false;
  assert.equal(await reduced.driver.run({ load: async () => 1, swap: () => { swapped = true; } }), true);
  assert.equal(swapped, true); assert.equal(reduced.jobs.length, 0);
  const { driver, jobs, phases } = setup(); const session = driver.begin();
  driver.reduce(); assert.equal(await session.covered, true); assert.equal(jobs[0].killed, true);
  assert.equal(phases.at(-1), 'idle'); assert.equal(await session.reveal(), true);
});

test('cleanup cancels readiness/reveal and permits no future begin', async () => {
  const { driver, jobs, phases } = setup(); const session = driver.begin();
  jobs[0].complete(); await session.covered;
  const revealing = session.reveal(new Promise(() => {})); await flush(); driver.destroy();
  assert.equal(await revealing, false); assert.equal(phases.at(-1), 'idle');
  assert.throws(() => driver.begin(), /destroyed/);
});

test('media timeout and media failure settle bounded readiness', async () => {
  await settleWithin(new Promise(() => {}), undefined, 1);
  await settleWithin(Promise.reject(new Error('image failed')), undefined, 100);
});
