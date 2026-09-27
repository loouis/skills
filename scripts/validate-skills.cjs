// node scripts/validate-skills.cjs
// Checks every skill against the folder contract in README.md. Exits 1 on any failure.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const { ROOT, SKILLS, listSkills, categories } = require('./lib.cjs');
const skills = listSkills(), failures = [];
const fail = (where, msg) => failures.push(`${where}: ${msg}`);

function jpegSize(file) {
  const d = fs.readFileSync(file); let o = 2;
  if (d[0] !== 0xff || d[1] !== 0xd8) return null;
  while (o + 8 < d.length) {
    if (d[o] !== 0xff) { o++; continue; }
    while (d[o] === 0xff) o++;
    const m = d[o++]; if (m === 0xd9 || m === 0xda) break;
    const len = d.readUInt16BE(o);
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(m)) return { w: d.readUInt16BE(o + 5), h: d.readUInt16BE(o + 3) };
    o += len;
  }
  return null;
}

const seen = new Map();
for (const s of skills) {
  const at = s.rel;
  if (seen.has(s.name)) fail(at, `name also used by ${seen.get(s.name)} (names must be unique across categories)`);
  seen.set(s.name, at);
  if (s.fm.name !== s.name) fail(at, `frontmatter name "${s.fm.name}" must match the folder name`);
  if (!s.fm.description) fail(at, 'frontmatter needs a description');
  else {
    if (s.fm.description.length > 1024) fail(at, `description is ${s.fm.description.length} chars (max 1024)`);
    if (!/\buse\b/i.test(s.fm.description)) fail(at, 'description should say when to use the skill');
  }
  const lines = fs.readFileSync(path.join(s.dir, 'SKILL.md'), 'utf8').split('\n').length;
  if (lines > 500) fail(at, `SKILL.md is ${lines} lines; move detail into references/`);
  // agents/openai.yaml
  if (!fs.existsSync(path.join(s.dir, 'agents/openai.yaml'))) fail(at, 'missing agents/openai.yaml');
  else for (const k of ['display_name', 'short_description', 'default_prompt']) if (!s.ui[k]) fail(at, `agents/openai.yaml needs interface.${k}`);
  if (s.ui.default_prompt && !s.ui.default_prompt.includes('$' + s.name)) fail(at, `default_prompt should invoke $${s.name}`);
  // REFERENCES.md: links only
  const refs = path.join(s.dir, 'REFERENCES.md');
  if (fs.existsSync(refs)) fs.readFileSync(refs, 'utf8').split('\n').forEach((l, i) => {
    if (l.trim() && !/^- \[[^\]]+\]\([^)]+\)\s*$/.test(l)) fail(`${at}/REFERENCES.md:${i + 1}`, 'should be links only ("- [text](url)")');
  });
  // demo
  if (fs.existsSync(path.join(s.dir, 'demo'))) {
    for (const f of ['index.html', 'PROMPT.md', 'preview.jpg']) if (!fs.existsSync(path.join(s.dir, 'demo', f))) fail(at, `demo/ is missing ${f}`);
    const p = path.join(s.dir, 'demo/preview.jpg');
    if (fs.existsSync(p)) { const z = jpegSize(p); if (!z || z.w !== 1280 || z.h !== 720) fail(at, `demo/preview.jpg is ${z ? z.w + 'x' + z.h : 'not a JPEG'}, expected 1280x720`); }
  }
  // public hygiene
  for (const f of fs.readdirSync(s.dir, { recursive: true })) {
    const full = path.join(s.dir, f);
    if (fs.statSync(full).isFile() && /\.(md|[cm]?js|[cm]?ts|py|css|astro|html|yaml|json)$/.test(f) && /\/Users\/|[A-Z]:\\\\Users\\\\/.test(fs.readFileSync(full, 'utf8'))) fail(`${at}/${f}`, 'contains a private file path');
  }
}
for (const c of categories(skills)) if (!c.text) fail(`skills/${c.id}`, 'missing category README.md');
for (const g of new Set(skills.map(s => s.category.split('/')[0]))) if (skills.some(s => s.category.includes('/') && s.category.startsWith(g + '/')) && !fs.existsSync(path.join(SKILLS, g, 'README.md'))) fail(`skills/${g}`, 'missing group README.md');

// generated families: every skill in a family ships an identical copy of its shared engine
const gooey = skills.filter(s => s.name.startsWith('gooey-section-')).map(s => [s, path.join(s.dir, 'assets/gooey-section.js')]);
if (gooey.length) {
  const hash = f => fs.existsSync(f) ? crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex') : null;
  const want = hash(gooey[0][1]);
  for (const [s, f] of gooey) if (!want || hash(f) !== want) fail(s.rel, 'engine copy differs from the other gooey-section skills (rebuild them together)');
}

// Portable page-transition packages share code, with one per-package default.
const drawn = skills.filter(s => s.name.startsWith('gsap-transition-'));
if (drawn.length) {
  const core = s => path.join(s.dir, 'assets/core');
  const files = fs.readdirSync(core(drawn[0])).filter(f => f !== 'config.mjs');
  for (const s of drawn) for (const file of files) {
    const expected = fs.readFileSync(path.join(core(drawn[0]), file));
    const target = path.join(core(s), file);
    if (!fs.existsSync(target) || !fs.readFileSync(target).equals(expected)) fail(s.rel, `shared transition core differs: ${file}`);
  }
}

if (failures.length) { console.error(failures.join('\n')); console.error(`\n${failures.length} problem(s) in ${skills.length} skills`); process.exit(1); }
console.log(`ok: ${skills.length} skills in ${categories(skills).length} categories pass the folder contract`.replace("1 categories", "1 category"));
