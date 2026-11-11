// node scripts/build-site.cjs [out-dir]
// Builds the GitHub Pages site (default out-dir: _site/, which is not committed):
//   /                      home page, every skill grouped by category
//   /<skill-name>/         the skill's page: search title, description, preview, tags, install steps
//   /<skill-name>/...      the skill folder itself, so its demo runs live at /<skill-name>/demo/
//   /sitemap.xml, /404.html
// Titles and tags come from scripts/skill-pages.json, like the README landing pages.
// .github/workflows/pages.yml runs this on every push to main and deploys the result.
const fs = require('node:fs'), path = require('node:path');
const { ROOT, REPO, SITE, listSkills, categories, skillPages } = require('./lib.cjs');

const OUT = path.resolve(ROOT, process.argv[2] || '_site');
const MARK = '.skills-site';
if (OUT === ROOT || ROOT.startsWith(OUT + path.sep)) throw new Error(`refusing to build into ${OUT}`);
if (fs.existsSync(OUT) && fs.readdirSync(OUT).length && !fs.existsSync(path.join(OUT, MARK))) throw new Error(`${OUT} is not empty and was not made by this script`);
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, MARK), '');

const skills = listSkills(), cats = categories(skills), pages = skillPages();
const missing = skills.filter(s => !pages[s.name]).map(s => s.name);
if (missing.length) throw new Error(`no entry in scripts/skill-pages.json for: ${missing.join(', ')}`);

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const sentence = s => /[.!?]$/.test(s) ? s : s + '.';
const clip = (s, n) => s.length <= n ? s : s.slice(0, s.lastIndexOf(' ', n - 1)).replace(/[,;:·]$/, '') + '…';
const firstSentence = s => (s.match(/^.*?[.!?](?=\s|$)/) || [s])[0];
const plain = md => md.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/`([^`]+)`/g, '$1').replace(/\*\*([^*]+)\*\*/g, '$1');
const intro = text => plain((text.replace(/^#.*\n/m, '').trim().split(/\n\s*\n/)[0] || '').replace(/<!--[\s\S]*$/, '').trim());
const write = (rel, text) => { const f = path.join(OUT, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, text); };
const ld = obj => `<script type="application/ld+json">${JSON.stringify(obj).replace(/</g, '\\u003c')}</script>`;
const TAGLINE = 'Agent skills for web designers and 3D builders';
const AGENTS = 'An agent skill for Claude Code, Codex and other AI coding agents.';

function head({ title, desc, url, image, root }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${esc(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="loouis/skills">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${esc(url)}">
${image ? `<meta property="og:image" content="${esc(image)}">\n<meta property="og:image:width" content="1280">\n<meta property="og:image:height" content="720">\n` : ''}<meta name="twitter:card" content="${image ? 'summary_large_image' : 'summary'}">
<link rel="stylesheet" href="${root}assets/site.css">
`;
}
const header = root => `<header class="bar"><a class="brand" href="${root}">loouis/skills</a><a href="${REPO}">GitHub</a></header>`;
const footer = root => `<footer><p>${esc(TAGLINE)}. Clone <a href="${REPO}">loouis/skills</a> and run <code>python3 install.py</code> to add them all to Claude Code.</p><p><a href="${root}">All skills</a> · <a href="${REPO}">GitHub</a></p></footer>`;
const card = (s, prefix) => `<a class="card" href="${prefix}${s.name}/">${s.preview ? `<img src="${prefix}${s.name}/demo/preview.jpg" alt="${esc(pages[s.name].title)}" width="1280" height="720" loading="lazy">` : `<div class="noimg">${esc(s.display)}</div>`}<div class="meta"><b>${esc(s.display)}</b><span>${esc(s.short)}</span></div></a>`;

// ---------- skill folders and pages ----------
for (const c of cats) for (const s of c.skills) {
  if (fs.existsSync(path.join(s.dir, 'index.html'))) throw new Error(`${s.rel}/index.html would clash with the skill page`);
  fs.cpSync(s.dir, path.join(OUT, s.name), { recursive: true, filter: src => !/(^|[\\/])(\.DS_Store|__pycache__)$/.test(src) });
  const page = pages[s.name], url = `${SITE}/${s.name}/`, image = s.preview ? `${SITE}/${s.name}/demo/preview.jpg` : null;
  const desc = clip(firstSentence(s.fm.description), 155);
  const tree = `${REPO}/tree/main/${s.rel}`;
  const others = c.skills.filter(o => o !== s);

  if (s.demo) { // give the live demo its own description and canonical address
    const f = path.join(OUT, s.name, 'demo/index.html');
    let html = fs.readFileSync(f, 'utf8');
    if (!/<meta\s+name=["']description["']/i.test(html)) html = html.replace(/<head[^>]*>/i, m => `${m}\n<meta name="description" content="${esc(clip(`Live demo: ${page.title}. ${sentence(s.short)}`, 155))}">\n<link rel="canonical" href="${esc(url)}demo/">`);
    fs.writeFileSync(f, html);
  }

  write(path.join(s.name, 'index.html'), head({ title: `${page.title} | loouis/skills`, desc, url, image, root: '../' }) +
`${ld({ '@context': 'https://schema.org', '@graph': [
  { '@type': 'SoftwareSourceCode', name: s.display, headline: page.title, description: s.fm.description, url, codeRepository: tree, keywords: page.tags.join(', '), ...(image ? { image } : {}), isPartOf: { '@type': 'WebSite', name: 'loouis/skills', url: `${SITE}/` } },
  { '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Skills', item: `${SITE}/` }, { '@type': 'ListItem', position: 2, name: c.title, item: `${SITE}/#${c.id.replace(/\//g, '-')}` }, { '@type': 'ListItem', position: 3, name: s.display, item: url }] },
] })}
</head>
<body>
${header('../')}
<main>
<nav class="crumbs"><a href="../">Skills</a> › <a href="../#${c.id.replace(/\//g, '-')}">${esc(c.title)}</a></nav>
<h1>${esc(page.title)}</h1>
<p class="lead">${esc(sentence(s.short))} ${esc(AGENTS)}</p>
${s.preview ? `<a class="hero" href="demo/"><img src="demo/preview.jpg" alt="${esc(page.title)}" width="1280" height="720"></a>` : ''}
<p class="actions">${s.demo ? '<a class="button primary" href="demo/">Open the live demo</a>' : ''}<a class="button" href="${tree}">View on GitHub</a><a class="button" href="${REPO}/blob/main/${s.rel}/SKILL.md">Read SKILL.md</a></p>
<h2>What it does</h2>
<p>${esc(s.fm.description)}</p>
<h2>Use it</h2>
<ul>
<li><b>Claude Code</b>: copy the <a href="${tree}">skill folder</a> to <code>~/.claude/skills/${esc(s.name)}/</code> (or clone the repository and run <code>python3 install.py</code>), then ask in your own words or call <code>/${esc(s.name)}</code>.</li>
<li><b>Codex</b>: copy the folder into your Codex skills directory and ask: <q>${esc(s.ui.default_prompt)}</q></li>
<li><b>Other agents</b>: point the agent at <a href="${REPO}/blob/main/${s.rel}/SKILL.md">SKILL.md</a> and let it follow the steps.</li>
</ul>
<ul class="tags" aria-label="Tags">${page.tags.map(t => `<li>${esc(t)}</li>`).join('')}</ul>
${others.length ? `<h2>More ${esc(c.title)} skills</h2>\n<div class="grid">${others.map(o => card(o, '../')).join('')}</div>` : ''}
</main>
${footer('../')}
</body>
</html>
`);
}

// ---------- home ----------
const homeDesc = 'Agent skills for web designers and 3D builders using Claude Code, Codex and other AI coding agents, each with a live demo: gooey scroll effects, GSAP page transitions, logo motion and Blender water, interiors and chrome.';
write('index.html', head({ title: `${TAGLINE} | loouis/skills`, desc: clip(homeDesc, 160), url: `${SITE}/`, image: `${SITE}/assets/skills-preview.jpg`, root: '' }) +
`${ld({ '@context': 'https://schema.org', '@type': 'WebSite', name: 'loouis/skills', url: `${SITE}/`, description: homeDesc })}
</head>
<body>
${header('')}
<main>
<h1>${esc(TAGLINE)}</h1>
<p class="lead">${skills.length} skills for Claude Code, Codex and other AI coding agents: gooey scroll effects, hand-drawn GSAP page transitions, vector masking and logo motion, films made in code, and Blender rendering for water, interiors and polished metal. Open any skill to see its live demo.</p>
<p class="actions"><a class="button primary" href="${REPO}">Get them on GitHub</a></p>
<nav class="toc" aria-label="Categories">${cats.map(c => `<a href="#${c.id.replace(/\//g, '-')}">${esc(c.title)}</a>`).join('')}</nav>
${cats.map(c => `<section id="${c.id.replace(/\//g, '-')}">
<h2>${esc(c.title)} <small>${c.skills.length}</small></h2>
<p>${esc(intro(c.text))}</p>
<div class="grid">${c.skills.map(s => card(s, '')).join('')}</div>
</section>`).join('\n')}
</main>
${footer('')}
</body>
</html>
`);

// ---------- 404, styles, assets, sitemap ----------
write('404.html', head({ title: 'Page not found | loouis/skills', desc: homeDesc, url: `${SITE}/404.html`, image: null, root: '/skills/' }).replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"') +
`</head>
<body>
${header('/skills/')}
<main><h1>Page not found</h1><p class="lead">That page isn't here. <a href="/skills/">See all the skills</a>.</p></main>
</body>
</html>
`);
fs.cpSync(path.join(ROOT, 'assets'), path.join(OUT, 'assets'), { recursive: true, filter: src => !/\.DS_Store$/.test(src) });
write('assets/site.css', `:root { color-scheme: light dark; --bg: #F1F4EE; --ink: #161B17; --dim: rgba(22,27,23,.64); --card: #fff; --line: rgba(22,27,23,.12); --accent: #161B17; --on-accent: #F1F4EE; }
@media (prefers-color-scheme: dark) { :root { --bg: #111412; --ink: #EEF1EA; --dim: rgba(238,241,234,.64); --card: #1A1E1B; --line: rgba(238,241,234,.14); --accent: #EEF1EA; --on-accent: #111412; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }
a { color: inherit; }
.bar, main, footer { max-width: 1120px; margin: 0 auto; padding: 0 16px; }
.bar { display: flex; justify-content: space-between; align-items: center; height: 64px; }
.bar a { text-decoration: none; font-weight: 600; }
.bar a + a { font-weight: 400; color: var(--dim); }
main { padding-bottom: 48px; }
h1 { font-size: clamp(30px, 5vw, 52px); line-height: 1.08; letter-spacing: -.02em; margin: 24px 0 16px; max-width: 22ch; }
h2 { font-size: 22px; letter-spacing: -.01em; margin: 48px 0 12px; }
h2 small { font-size: 14px; color: var(--dim); font-weight: 400; margin-left: 6px; }
p, li { max-width: 70ch; }
.lead { font-size: 19px; color: var(--dim); }
.crumbs { margin-top: 16px; font-size: 14px; color: var(--dim); }
.crumbs a { text-decoration: none; }
.hero { display: block; margin: 28px 0 8px; border-radius: 14px; overflow: hidden; border: 1px solid var(--line); background: var(--card); }
img { display: block; width: 100%; height: auto; }
.actions { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
.button { display: inline-block; padding: 10px 16px; border-radius: 999px; border: 1px solid var(--line); background: var(--card); text-decoration: none; font-size: 15px; }
.button.primary { background: var(--accent); color: var(--on-accent); border-color: var(--accent); }
code { font: 14px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace; background: var(--card); border: 1px solid var(--line); border-radius: 6px; padding: 1px 5px; overflow-wrap: anywhere; }
q { font-style: italic; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; padding: 0; margin: 24px 0; }
.tags li { font-size: 13px; padding: 4px 10px; border-radius: 999px; border: 1px solid var(--line); color: var(--dim); }
.toc { display: flex; flex-wrap: wrap; gap: 8px 16px; margin: 8px 0 0; font-size: 15px; }
.toc a { color: var(--dim); }
section { scroll-margin-top: 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 16px; }
.card { display: block; background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; text-decoration: none; }
.card img, .noimg { aspect-ratio: 16 / 9; object-fit: cover; }
.noimg { display: flex; align-items: center; justify-content: center; padding: 16px; text-align: center; font-size: 20px; font-weight: 600; border-bottom: 1px solid var(--line); }
.meta { padding: 12px 14px 14px; }
.meta b { display: block; }
.meta span { color: var(--dim); font-size: 14px; }
footer { border-top: 1px solid var(--line); padding-top: 16px; padding-bottom: 40px; color: var(--dim); font-size: 14px; }
`);
const urls = [`${SITE}/`, ...skills.flatMap(s => [`${SITE}/${s.name}/`, ...(s.demo ? [`${SITE}/${s.name}/demo/`] : [])])];
write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url><loc>${u}</loc></url>`).join('\n')}
</urlset>
`);
console.log(`built ${path.relative(process.cwd(), OUT) || OUT}: home, ${skills.length} skill pages, ${skills.filter(s => s.demo).length} live demos, ${urls.length} sitemap entries`);
