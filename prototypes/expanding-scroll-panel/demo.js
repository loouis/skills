import { DEFAULTS, mountExpandingPanel } from './expanding-panel.js';

const stage = document.querySelector('[data-stage]');
const progressLabel = document.querySelector('[data-progress]');
const settings = document.querySelector('#tuning-panel');
const toggle = document.querySelector('.tune-button');
const guides = document.querySelector('.alignment-guides');
const engine = mountExpandingPanel(stage, ({ progress, reduced }) => {
  progressLabel.textContent = reduced ? 'Static' : `${Math.round(progress * 100)}%`;
});
document.querySelector('.demo-dock').hidden = false;

function showSettings(open) {
  settings.hidden = !open;
  toggle.setAttribute('aria-expanded', String(open));
}

toggle.addEventListener('click', () => showSettings(settings.hidden));
document.querySelector('[data-close]').addEventListener('click', () => {
  showSettings(false);
  toggle.focus();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !settings.hidden) {
    showSettings(false);
    toggle.focus();
  }
});

const inputs = ['inset', 'radius', 'finish'].map(id => document.getElementById(id));
function updateSettings() {
  const [inset, radius, finish] = inputs.map(input => Number(input.value));
  document.querySelector('#inset-value').textContent = `${inset} px`;
  document.querySelector('#radius-value').textContent = `${radius} px`;
  document.querySelector('#finish-value').textContent = `${finish}% from top`;
  engine.update({ inset, radius, endViewport: finish / 100 });
}
inputs.forEach(input => input.addEventListener('input', updateSettings));
document.querySelector('#guides').addEventListener('change', event => { guides.hidden = !event.target.checked; });
document.querySelector('#reduce').addEventListener('change', event => { engine.update({ reduced: event.target.checked }); });
document.querySelector('[data-reset]').addEventListener('click', () => {
  inputs[0].value = DEFAULTS.inset;
  inputs[1].value = DEFAULTS.radius;
  inputs[2].value = DEFAULTS.endViewport * 100;
  document.querySelector('#guides').checked = false;
  document.querySelector('#reduce').checked = false;
  guides.hidden = true;
  engine.update(DEFAULTS);
  updateSettings();
});
document.querySelectorAll('[data-replay]').forEach(button => button.addEventListener('click', event => {
  event.preventDefault();
  showSettings(false);
  engine.goTo(0);
}));
document.querySelector('[data-finish]').addEventListener('click', () => { showSettings(false); engine.goTo(1); });
