// node scripts/serve-site.cjs [port] [dir]
// Serves the built site (default _site/ on port 4317) for a local preview, at both / and
// /skills/ so it behaves like https://loouis.github.io/skills/. Build it first with
// node scripts/build-site.cjs.
const http = require('node:http'), fs = require('node:fs'), path = require('node:path');
const ROOT = path.resolve(__dirname, '..');
const port = Number(process.argv[2] || 4317), dir = path.resolve(ROOT, process.argv[3] || '_site');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.cjs': 'text/javascript', '.json': 'application/json', '.xml': 'application/xml', '.md': 'text/plain; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.py': 'text/plain; charset=utf-8', '.yaml': 'text/plain; charset=utf-8', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.gif': 'image/gif', '.mp4': 'video/mp4', '.webm': 'video/webm', '.woff2': 'font/woff2', '.glb': 'model/gltf-binary', '.wasm': 'application/wasm' };
http.createServer((req, res) => {
  let rel = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/^\/skills(?=\/|$)/, '') || '/';
  let file = path.join(dir, rel);
  if (!file.startsWith(dir)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
    if (!rel.endsWith('/')) { res.writeHead(301, { Location: req.url.split('?')[0] + '/' }).end(); return; }
    file = path.join(file, 'index.html');
  }
  const found = fs.existsSync(file) && fs.statSync(file).isFile();
  const send = found ? file : path.join(dir, '404.html');
  res.writeHead(found ? 200 : 404, { 'Content-Type': types[path.extname(send).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(send).pipe(res);
}).listen(port, () => console.log(`serving ${dir} at http://localhost:${port}/`));
