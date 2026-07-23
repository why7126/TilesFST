import { readFileSync } from 'node:fs';
import { join } from 'node:path';

import { describe, expect, it } from 'vitest';

const projectRoot = process.cwd();
const srcRoot = join(projectRoot, 'src');
const readSource = (relativePath: string) => readFileSync(join(srcRoot, relativePath), 'utf8');

const appSource = readSource('app/App.tsx');
const adminHomeCss = readSource('features/admin/styles/admin-home.css');
const userManagementCss = readSource('features/admin/styles/user-management.css');
const tileSkuCss = readSource('features/admin/styles/tile-sku-management.css');
const bannerCss = readSource('features/admin/styles/banner-management.css');
const logAuditCss = readSource('features/admin/styles/log-audit.css');
const tileSkuModalSource = readSource('features/admin/components/TileSkuFormModal.tsx');
const bannerModalSource = readSource('features/admin/components/BannerFormModal.tsx');

describe('REQ-0027 admin mobile adaptation smoke contract', () => {
  it('keeps every implemented admin route in the mobile acceptance matrix', () => {
    [
      '/admin/login',
      '/admin/dashboard',
      '/admin/brands',
      '/admin/banners',
      '/admin/tile-categories',
      '/admin/tile-specs',
      '/admin/tile-skus',
      '/admin/profile',
      '/admin/users',
      '/admin/logs',
      '/admin/api-docs',
      '/admin/settings/:tab',
      '/admin/forbidden',
    ].forEach((route) => {
      expect(appSource).toContain(`path="${route}"`);
    });
  });

  it('keeps the shell and navigation usable on tablet and phone widths', () => {
    expect(adminHomeCss).toContain('@media (max-width: 1023px)');
    expect(adminHomeCss).toContain('grid-template-columns: 1fr;');
    expect(adminHomeCss).toContain('.admin-shell .sidebar-toggle');
    expect(adminHomeCss).toContain('display: none;');
    expect(adminHomeCss).toContain('max-height: 100vh;');
    expect(adminHomeCss).toContain('overflow: auto;');
    expect(adminHomeCss).toContain('@media (max-width: 639px)');
    expect(adminHomeCss).toContain('max-height: 48vh;');
    expect(adminHomeCss).not.toContain('th:nth-child(4)');
    expect(adminHomeCss).not.toContain('td:nth-child(4)');
  });

  it('keeps tables horizontally scrollable inside cards instead of clipping the page', () => {
    expect(userManagementCss).toContain('.admin-shell .table-card');
    expect(userManagementCss).toContain('overflow-x: auto;');
    expect(userManagementCss).toContain('-webkit-overflow-scrolling: touch;');
    expect(userManagementCss).toContain('min-width: 760px;');
    expect(userManagementCss).toContain('.admin-shell .table-card .sku-mgmt-table');
    expect(userManagementCss).toContain('.admin-shell .table-card .banner-mgmt-table');
  });

  it('keeps filters and pagination usable on phone widths without changing the DOM contract', () => {
    expect(userManagementCss).toContain('@media (max-width: 639px)');
    expect(userManagementCss).toContain('.admin-shell .page-summary');
    expect(userManagementCss).toContain('.admin-shell .page-right');
    expect(userManagementCss).toContain('.admin-shell .page-buttons');
    expect(userManagementCss).toContain('.admin-shell .page-size-wrap');
    expect(userManagementCss).toContain('flex-direction: column;');
    expect(userManagementCss).toContain('.admin-shell .sku-filter-grid');
    expect(userManagementCss).toContain('.admin-shell .banner-filter-grid');
    expect(userManagementCss).toContain('.admin-shell .log-audit-filter-grid');
  });

  it('keeps narrow modals scrollable with reachable headers and footer actions', () => {
    expect(userManagementCss).toContain('max-height: calc(100vh - 48px);');
    expect(userManagementCss).toContain('display: flex;');
    expect(userManagementCss).toContain('flex-direction: column;');
    expect(userManagementCss).toContain('.admin-shell .modal-body');
    expect(userManagementCss).toContain('overflow-y: auto;');
    expect(userManagementCss).toContain('max-height: calc(100vh - 24px);');
    expect(userManagementCss).toContain('flex-direction: column-reverse;');
  });

  it('keeps SKU and Banner wide modals dedicated and mobile-constrained', () => {
    expect(tileSkuModalSource).toContain('className="sku-modal-card"');
    expect(tileSkuModalSource).not.toContain('className="modal-card sku-modal-card"');
    expect(bannerModalSource).toContain('className="banner-modal-card"');
    expect(bannerModalSource).not.toContain('className="modal-card banner-modal-card"');
    expect(tileSkuCss).toContain('.admin-shell .sku-modal-card');
    expect(tileSkuCss).toContain('max-height: calc(100vh - 24px);');
    expect(tileSkuCss).toContain('.admin-shell .sku-upload-grid');
    expect(bannerCss).toContain('.admin-shell .banner-modal-card');
    expect(bannerCss).toContain('max-height: calc(100vh - 24px);');
    expect(bannerCss).toContain('.admin-shell .banner-upload-box');
    expect(bannerCss).toContain('height: auto;');
  });

  it('keeps the log detail drawer full-width and scrollable on phone widths', () => {
    expect(logAuditCss).toContain('.admin-shell .log-drawer');
    expect(logAuditCss).toContain('width: 100vw;');
    expect(logAuditCss).toContain('max-width: 100vw;');
    expect(logAuditCss).toContain('.admin-shell .log-drawer-body');
    expect(logAuditCss).toContain('grid-template-columns: 1fr;');
  });
});
