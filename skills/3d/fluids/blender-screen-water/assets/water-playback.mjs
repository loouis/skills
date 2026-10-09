// Pass explicit media URLs from the consuming project. No assets are bundled here.
export const LOOP = Object.freeze({ fps: 30, frames: 180, duration: 6, start: 3 });
const clamp = x => Math.max(0, Math.min(1, x));
const smooth = x => { const p = clamp(x); return p * p * (3 - 2 * p); };
export const loopFrame = ms => {
  const n = Math.floor(Math.max(0, ms) * 30 / 1000);
  return 1 + (n < 180 ? n : 90 + (n - 180) % 90);
};
export const arrivalOpacity = ms => smooth(ms / 160);
export function drainState(ms, width = 480, height = 1800) {
  const p = clamp(ms / 1100);
  return { done: p === 1, opacity: 1 - smooth(p), blur: 3.5 * height / 1800,
    boundary(x) {
      const wave = 11 * Math.sin(Math.PI * p) *
        (Math.sin(x / width * 6.1 + p * 2) + .28 * Math.sin(x / width * 12.8));
      return (-45 + 1890 * p ** 1.25 + wave) * height / 1800;
    } };
}
export function controlReturn(ms, mode) {
  if (!['cold', 'hot'].includes(mode)) throw new RangeError('Use cold or hot');
  const opacity = smooth((ms - (mode === 'hot' ? 1140 : 1230)) / 660);
  return { opacity, scale: .975 + .025 * opacity };
}
export class ScreenWaterFilm {
  constructor({ src, poster }) {
    if (!src || !poster) throw new TypeError('Supply explicit movie and poster URLs');
    this.video = document.createElement('video');
    Object.assign(this.video, { muted: true, loop: false, playsInline: true, preload: 'auto' });
    this.video.src = src;
    this.poster = new Image(); this.poster.src = poster;
    this.active = false; this.token = 0; this.error = null;
    this.onError = () => { this.error = 'Water video unavailable'; };
    this.onEnd = () => {
      if (this.active) { this.video.currentTime = LOOP.start; this.startPlayback(); }
    };
    this.video.addEventListener('error', this.onError);
    this.video.addEventListener('ended', this.onEnd);
  }
  startPlayback() {
    const token = this.token;
    this.video.play().then(() => {
      if (token !== this.token && !this.active) this.video.pause();
    }).catch(() => {
      if (token === this.token) this.error = 'Playback paused; activate again to retry';
    });
  }
  // `active` is decorative playback state. Keep it true while an exit mask drains.
  sync(active, reduced = false) {
    const next = Boolean(active && !reduced);
    if (next !== this.active) {
      this.active = next; ++this.token; this.video.pause();
      if (this.video.readyState) this.video.currentTime = 0;
      if (next) { this.error = null; this.startPlayback(); }
    }
    return !reduced && this.active && this.video.readyState >= 2 ? this.video :
      this.poster.complete && this.poster.naturalWidth ? this.poster : null;
  }
  reset() { this.sync(false); }
  dispose() {
    this.reset(); this.video.removeEventListener('error', this.onError);
    this.video.removeEventListener('ended', this.onEnd);
    this.video.removeAttribute('src'); this.video.load(); this.poster.src = '';
  }
}
