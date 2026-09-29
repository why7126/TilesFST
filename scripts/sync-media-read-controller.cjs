// REQ-0136: compile one platform-neutral controller into the miniapp runtime root.
const fs = require('node:fs');
const path = require('node:path');
const ts = require('../src/web/node_modules/typescript');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'src/shared/media/read-controller.ts'), 'utf8');
const header = '// Generated from src/shared/media/read-controller.ts; run node scripts/sync-media-read-controller.cjs.\n';
for (const [extension, content] of [
  ['ts', source],
  ['js', ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2018, module: ts.ModuleKind.CommonJS } }).outputText],
]) fs.writeFileSync(path.join(root, `src/miniapp/utils/media-read-controller.${extension}`), header + content);
const wrapper = fs.readFileSync(path.join(root, 'src/miniapp/utils/media-read.ts'), 'utf8');
fs.writeFileSync(path.join(root, 'src/miniapp/utils/media-read.js'),
  '// Generated from media-read.ts; run node scripts/sync-media-read-controller.cjs.\n' +
  ts.transpileModule(wrapper, { compilerOptions: { target: ts.ScriptTarget.ES2018, module: ts.ModuleKind.CommonJS } }).outputText);

for (const relative of ['utils/page-media', 'components/authorized-image/index', 'pages/tile-detail/index', 'pages/certificate-detail/index']) {
  const input = fs.readFileSync(path.join(root, `src/miniapp/${relative}.ts`), 'utf8');
  fs.writeFileSync(path.join(root, `src/miniapp/${relative}.js`),
    '// Generated from TypeScript; run node scripts/sync-media-read-controller.cjs.\n' +
    ts.transpileModule(input, { compilerOptions: { target: ts.ScriptTarget.ES2018, module: ts.ModuleKind.CommonJS } }).outputText);
}
