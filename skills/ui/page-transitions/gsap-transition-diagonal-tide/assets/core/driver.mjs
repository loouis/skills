import { TIMING } from './geometry.mjs';

// Wait for readiness, cancellation, or the timeout; always remove listeners/timers.
// Media errors count as settled so a broken image cannot trap the user behind ink.
export function settleWithin(work, signal, timeoutMs = 5000) {
  return new Promise(resolve => {
    let timer;
    const finish = () => { clearTimeout(timer); signal?.removeEventListener('abort', finish); resolve(); };
    if (signal?.aborted) return finish();
    signal?.addEventListener('abort', finish, { once: true });
    timer = setTimeout(finish, timeoutMs);
    Promise.resolve(work).then(finish, finish);
  });
}

function loadUntilCancelled(load, signal) {
  return new Promise((resolve, reject) => {
    const cancel = () => { signal.removeEventListener('abort', cancel); resolve(undefined); };
    if (signal.aborted) return cancel();
    signal.addEventListener('abort', cancel, { once: true });
    Promise.resolve().then(() => load(signal)).then(
      value => { signal.removeEventListener('abort', cancel); resolve(value); },
      error => { signal.removeEventListener('abort', cancel); reject(error); },
    );
  });
}

// Router-independent lifecycle. A session owns its clock, signal and completion.
// Cancelling a tween also settles its promise; kill() alone does not do that.
export function createDriver({ gsap, paint, onPhase = () => {}, reducedMotion = () => false }) {
  let active, destroyed = false;
  const begin = externalSignal => {
    if (destroyed) throw new Error('Transition driver was destroyed.');
    active?.cancel();
    const controller = new AbortController();
    const clock = { time: 0 };
    let tween, settleTween, finished = false, revealing = false;
    let motion = !reducedMotion();
    const current = () => active === session && !finished && !controller.signal.aborted;
    const stopTween = result => {
      tween?.kill(); tween = undefined;
      const resolve = settleTween; settleTween = undefined; resolve?.(result);
    };
    const finish = () => {
      if (finished) return;
      finished = true;
      stopTween(false);
      externalSignal?.removeEventListener('abort', cancel);
      if (active === session) { active = undefined; paint(0); onPhase('idle'); }
    };
    const cancel = () => { controller.abort(); finish(); };
    const animate = (to, phase) => new Promise(resolve => {
      if (!current()) return resolve(false);
      if (!motion) { clock.time = to; return resolve(true); }
      onPhase(phase);
      settleTween = resolve;
      tween = gsap.to(clock, {
        time: to, duration: to - clock.time, ease: 'none',
        onUpdate: () => { if (current()) paint(clock.time); },
        onComplete: () => { tween = undefined; settleTween = undefined; resolve(current()); },
      });
    });
    const session = {
      signal: controller.signal,
      current,
      cancel,
      reduce() {
        if (!current()) return;
        motion = false;
        clock.time = revealing ? TIMING.duration : TIMING.swapAt;
        stopTween(true);
        paint(0); onPhase('idle');
      },
      covered: Promise.resolve(false),
      async reveal(ready = Promise.resolve(), timeoutMs = 5000) {
        if (!current() || revealing) return false;
        revealing = true;
        const covered = await session.covered;
        if (!covered || !current()) return false;
        await settleWithin(ready, controller.signal, timeoutMs);
        if (!current()) return false;
        const complete = await animate(TIMING.duration, 'reveal');
        if (current()) finish();
        return complete;
      },
    };
    active = session;
    externalSignal?.addEventListener('abort', cancel, { once: true });
    if (externalSignal?.aborted) cancel();
    paint(0);
    session.covered = animate(TIMING.swapAt, 'cover').then(ok => {
      if (ok && current() && motion) onPhase('hold');
      return ok && current();
    });
    return session;
  };
  return {
    begin,
    cancel() { active?.cancel(); },
    reduce() { active?.reduce(); },
    destroy() { active?.cancel(); destroyed = true; },
    // Start fetching alongside cover. Swap only this session's loaded destination.
    async run({ load, swap, ready = () => Promise.resolve(), signal, timeoutMs = 5000 }) {
      const session = begin(signal);
      try {
        const [destination, covered] = await Promise.all([loadUntilCancelled(load, session.signal), session.covered]);
        if (!covered || !session.current()) return false;
        await swap(destination, session.signal);
        if (!session.current()) return false;
        return await session.reveal(ready(session.signal), timeoutMs);
      } catch (error) {
        const cancelled = session.signal.aborted;
        session.cancel();
        if (cancelled) return false;
        throw error;
      }
    },
  };
}
