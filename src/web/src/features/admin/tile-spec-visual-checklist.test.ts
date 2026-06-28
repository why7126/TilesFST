import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../../..');

const prototypeListHtml = readFileSync(
  path.join(
    repoRoot,
    'issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html',
  ),
  'utf8',
);

const prototypeModalHtml = readFileSync(
  path.join(
    repoRoot,
    'issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.html',
  ),
  'utf8',
);

const pageSource = readFileSync(
  path.join(repoRoot, 'src/web/src/pages/admin/TileSpecManagementPage.tsx'),
  'utf8',
);

const modalSource = readFileSync(
  path.join(repoRoot, 'src/web/src/features/admin/components/TileSpecFormModal.tsx'),
  'utf8',
);

const navSource = readFileSync(
  path.join(repoRoot, 'src/web/src/features/admin/data/admin-nav.ts'),
  'utf8',
);

const skuModalSource = readFileSync(
  path.join(repoRoot, 'src/web/src/features/admin/components/TileSkuFormModal.tsx'),
  'utf8',
);

const cssSource = readFileSync(
  path.join(repoRoot, 'src/web/src/features/admin/styles/tile-spec-management.css'),
  'utf8',
);

/** HTML gate：实现 MUST 对齐 list 原型关键结构，且 MUST NOT 引入规格类型列/筛选 */
describe('REQ-0009 visual checklist (HTML gate)', () => {
  it('1 Shell + Sidebar「瓷砖规格」active route', () => {
    expect(navSource).toContain("label: '瓷砖规格'");
    expect(navSource).toContain("path: '/admin/tile-specs'");
  });

  it('2 4 指标卡（启用/停用）', () => {
    for (const label of ['规格总数', '启用规格', '停用规格', '未关联 SKU']) {
      expect(pageSource).toContain(label);
      expect(prototypeListHtml).toContain(label);
    }
  });

  it('3 状态筛选（非规格类型）', () => {
    expect(pageSource).toContain('全部状态');
    expect(pageSource).toContain('ENABLED');
    expect(pageSource).not.toContain('规格类型');
    expect(prototypeListHtml).not.toContain('全部规格类型');
  });

  it('4 表格状态列 + 启停操作', () => {
    expect(pageSource).toContain('<th>状态</th>');
    expect(pageSource).toContain('启用');
    expect(pageSource).toContain('停用');
    expect(pageSource).not.toContain('规格类型');
  });

  it('5 删除置灰 + tooltip', () => {
    expect(pageSource).toContain('canDeleteTileSpec');
    expect(pageSource).toContain('仅允许删除未关联SKU且已停用的规格');
  });

  it('6 分页左共 x 条', () => {
    expect(pageSource).toContain('共 {total} 条');
    expect(prototypeListHtml).toContain('共 86 条');
  });

  it('7 弹窗 720px 字段网格', () => {
    expect(modalSource).toContain('tile-spec-modal-card');
    expect(cssSource).toMatch(/720px|max-width:\s*720px/);
    expect(modalSource).toContain('tile-spec-form-grid');
  });

  it('8 只读 display_name 实时生成', () => {
    expect(modalSource).toContain('previewName');
    expect(modalSource).toContain('buildDisplayName');
    expect(modalSource).toContain('尺寸名称（只读）');
    expect(prototypeModalHtml).toContain('600×1200mm');
  });

  it('9 无状态/规格类型字段', () => {
    expect(modalSource).not.toMatch(/规格类型|status.*select/i);
    expect(modalSource).not.toContain('ENABLED');
    expect(prototypeModalHtml).toContain('全部规格类型');
    expect(pageSource).not.toContain('规格类型');
  });

  it('10 SKU 弹窗规格 select', () => {
    expect(skuModalSource).toContain('瓷砖规格');
    expect(skuModalSource).toContain('<select');
    expect(skuModalSource).toContain('fetchTileSpecs');
  });

  it('11 无裸 Hex（规格 CSS port）', () => {
    expect(cssSource).not.toMatch(/#[0-9A-Fa-f]{3,8}\b/);
    expect(cssSource).toMatch(/var\(--/);
  });

  it('12 PNG Golden Reference 文件存在', () => {
    const listPng = path.join(
      repoRoot,
      'issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.png',
    );
    const modalPng = path.join(
      repoRoot,
      'issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.png',
    );
    expect(readFileSync(listPng).byteLength).toBeGreaterThan(1000);
    expect(readFileSync(modalPng).byteLength).toBeGreaterThan(1000);
  });
});
