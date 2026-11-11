// Shared helpers for the repo scripts: find skills and read their metadata.
const fs = require('node:fs'), path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const SKILLS = path.join(ROOT, 'skills');

function frontmatter(text) {
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---', 4);
  if (end < 0) return null;
  const out = {};
  for (const line of text.slice(4, end).split('\n')) {
    const m = line.match(/^([a-z_-]+):\s*(.*)$/i);
    if (m) out[m[1]] = m[2].trim();
  }
  return out;
}
function yamlInterface(text) {
  const out = {};
  for (const line of text.split('\n')) {
    const m = line.match(/^\s+([a-z_]+):\s*"(.*)"\s*$/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}
function titleOf(readme, fallback) {
  const m = readme && readme.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : fallback;
}
// every SKILL.md under skills/, at any depth. A skill's category is the folder path
// between skills/ and the skill folder, e.g. "ui/sections".
function listSkills() {
  const out = [];
  const rel = p => path.relative(ROOT, p).split(path.sep).join('/');
  (function walk(dir) {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      if (!fs.statSync(full).isDirectory()) continue;
      const file = path.join(full, 'SKILL.md');
      if (!fs.existsSync(file)) { walk(full); continue; }
      const text = fs.readFileSync(file, 'utf8');
      const agents = path.join(full, 'agents', 'openai.yaml');
      const ui = fs.existsSync(agents) ? yamlInterface(fs.readFileSync(agents, 'utf8')) : {};
      const has = p => fs.existsSync(path.join(full, p));
      out.push({
        category: path.relative(SKILLS, dir).split(path.sep).join('/'), name, dir: full, rel: rel(full), fm: frontmatter(text) || {}, ui,
        display: ui.display_name || name, short: ui.short_description || '',
        demo: has('demo/index.html') ? rel(path.join(full, 'demo/index.html')) : null,
        preview: has('demo/preview.jpg') ? rel(path.join(full, 'demo/preview.jpg')) : null,
        prompt: has('demo/PROMPT.md') ? rel(path.join(full, 'demo/PROMPT.md')) : null,
      });
    }
  })(SKILLS);
  return out.sort((a, b) => (a.category + '/' + a.name).localeCompare(b.category + '/' + b.name));
}
function categories(skills) {
  const cats = [...new Set(skills.map(s => s.category))];
  return cats.map(c => {
    const readme = path.join(SKILLS, c, 'README.md');
    const text = fs.existsSync(readme) ? fs.readFileSync(readme, 'utf8') : '';
    const leaf = c.split('/').pop();
    return { id: c, title: titleOf(text, leaf[0].toUpperCase() + leaf.slice(1)), readme, text, skills: skills.filter(s => s.category === c) };
  });
}
function replaceBetween(text, tag, body) {
  const a = `<!-- ${tag}:start -->`, b = `<!-- ${tag}:end -->`;
  const i = text.indexOf(a), j = text.indexOf(b);
  if (i < 0 || j < i) return null;
  return text.slice(0, i + a.length) + '\n' + body.trim() + '\n' + text.slice(j);
}
// Search titles and tags for each skill's generated landing page (README.md in the skill folder).
const PAGES = path.join(__dirname, 'skill-pages.json');
function skillPages() { return fs.existsSync(PAGES) ? JSON.parse(fs.readFileSync(PAGES, 'utf8')) : {}; }
// Where the repository and its GitHub Pages site live (scripts/build-site.cjs builds the site).
const REPO = 'https://github.com/loouis/skills';
const SITE = 'https://loouis.github.io/skills';
module.exports = { ROOT, SKILLS, REPO, SITE, listSkills, categories, replaceBetween, frontmatter, yamlInterface, skillPages };
