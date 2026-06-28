/**
 * REQ-0009 视觉验收截图：1440×1024 实现页 Golden Reference
 * 用法：node scripts/capture-tile-spec-visual.mjs
 * 依赖：Docker Compose 已启动（./scripts/docker-up.sh）
 */
import { execSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WEB_URL = process.env.SMOKE_WEB_URL ?? 'http://localhost:3000';
const OUT_DIR = path.join(
  ROOT,
  'issues/requirements/review/REQ-0009-tile-spec-management/prototype/web',
);

function adminPassword() {
  if (process.env.ADMIN_INITIAL_PASSWORD) return process.env.ADMIN_INITIAL_PASSWORD;
  return execSync('docker exec tile-info-platform-backend printenv ADMIN_INITIAL_PASSWORD', {
    encoding: 'utf8',
  }).trim();
}

async function login(page) {
  await page.goto(`${WEB_URL}/admin/login`, { waitUntil: 'networkidle' });
  await page.getByLabel(/用户名|账号/i).fill('admin');
  await page.getByLabel(/密码/i).fill(adminPassword());
  await page.getByRole('button', { name: /登录|Sign in/i }).click();
  await page.waitForURL(/\/admin\/(dashboard|profile|tile-specs|brands|tile-skus)/, {
    timeout: 15000,
  });
}

async function main() {
  mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1024 } });
  const page = await context.newPage();

  await login(page);
  await page.goto(`${WEB_URL}/admin/tile-specs`, { waitUntil: 'networkidle' });
  await page.getByRole('heading', { name: '瓷砖规格' }).waitFor({ timeout: 10000 });
  await page.screenshot({
    path: path.join(OUT_DIR, 'tile-size-management-impl-1440.png'),
    fullPage: false,
  });

  await page.getByRole('button', { name: '＋ 新增瓷砖规格' }).click();
  await page.getByRole('heading', { name: '新增瓷砖规格' }).waitFor({ timeout: 10000 });
  await page.screenshot({
    path: path.join(OUT_DIR, 'tile-size-management-modal-impl-1440.png'),
    fullPage: false,
  });

  await page.keyboard.press('Escape');
  await page.goto(`${WEB_URL}/admin/tile-skus`, { waitUntil: 'networkidle' });
  await page.getByRole('button', { name: /新增SKU|新增 SKU/i }).click();
  await page.getByRole('heading', { name: /新增 SKU/i }).waitFor({ timeout: 10000 });
  await page.getByText('瓷砖规格').waitFor({ timeout: 10000 });
  await page.screenshot({
    path: path.join(OUT_DIR, 'tile-sku-spec-select-impl-1440.png'),
    fullPage: false,
  });

  await browser.close();
  console.log('Captured implementation screenshots to', OUT_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
