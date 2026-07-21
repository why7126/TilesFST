import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/user-management.css';
import '../styles/banner-management.css';
import '../styles/system-settings.css';

const stylesDir = path.join(path.dirname(fileURLToPath(import.meta.url)), '../styles');

function readCss(filename: string): string {
  return readFileSync(path.join(stylesDir, filename), 'utf8');
}

const userManagementCss = readCss('user-management.css');
const systemSettingsCss = readCss('system-settings.css');
const bannerManagementCss = readCss('banner-management.css');

const fetchTileSkusMock = vi.fn();
const fetchTileSkuMock = vi.fn();
const fetchTopicsMock = vi.fn();
const fetchBrandsMock = vi.fn();
const createBannerMock = vi.fn();
const uploadBannerImageMock = vi.fn();

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/admin/api/tile-skus-api', () => ({
  fetchTileSkus: (...args: unknown[]) => fetchTileSkusMock(...args),
  fetchTileSku: (...args: unknown[]) => fetchTileSkuMock(...args),
}));

vi.mock('@/features/admin/api/topics-api', () => ({
  fetchTopics: (...args: unknown[]) => fetchTopicsMock(...args),
}));

vi.mock('@/features/admin/api/brands-api', () => ({
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('@/features/admin/api/banners-api', () => ({
  createBanner: (...args: unknown[]) => createBannerMock(...args),
  updateBanner: vi.fn(),
  uploadBannerImage: (...args: unknown[]) => uploadBannerImageMock(...args),
}));

import { BannerFormModal } from './BannerFormModal';

function renderBannerModal() {
  return render(
    <div className="admin-shell">
      <BannerFormModal
        open
        mode="create"
        banner={null}
        onClose={() => undefined}
        onSuccess={() => undefined}
      />
    </div>,
  );
}

describe('BannerFormModal', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchTileSkusMock.mockResolvedValue({
      items: [
        {
          id: 7,
          name: '测试 SKU',
          sku_code: 'SKU-007',
          images: [],
          main_image_url: '/media/demo.webp',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
    });
    fetchTileSkuMock.mockResolvedValue({
      id: 7,
      name: '测试 SKU',
      sku_code: 'SKU-007',
      images: [{ id: 1, object_key: 'images/default/sku/main.webp', url: '/media/main.webp', is_main: true }],
      main_image_url: '/media/main.webp',
    });
    fetchTopicsMock.mockResolvedValue({ items: [] });
    fetchBrandsMock.mockResolvedValue({
      items: [
        {
          id: 3,
          name: '马可波罗',
          short_name: 'MK',
          logo_object_key: 'images/default/brands/logos/mk.webp',
          logo_url: '/media/images/default/brands/logos/mk.webp',
        },
      ],
    });
    createBannerMock.mockResolvedValue({ id: 1 });
  });

  it('shows 选择 upload label and applies SKU main image via detail fetch', async () => {
    render(
      <BannerFormModal
        open
        mode="create"
        banner={null}
        onClose={() => undefined}
        onSuccess={() => undefined}
      />,
    );

    expect(screen.getByText('选择')).toBeInTheDocument();
    expect(screen.queryByText('自定义上传')).toBeNull();

    fireEvent.change(screen.getByLabelText(/跳转类型/), { target: { value: 'SKU_DETAIL' } });

    const skuInput = await screen.findByRole('combobox', { name: '关联 SKU' });
    fireEvent.focus(skuInput);

    await waitFor(() => {
      expect(screen.getByRole('option', { name: '测试 SKU · SKU-007' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('option', { name: '测试 SKU · SKU-007' }));

    await waitFor(() => {
      expect(fetchTileSkuMock).toHaveBeenCalledWith(7);
    });

    fetchTileSkuMock.mockClear();
    fireEvent.click(screen.getByRole('button', { name: '使用 SKU 主图' }));

    await waitFor(() => {
      expect(fetchTileSkuMock).toHaveBeenCalledWith(7);
    });
  });

  it('renders single validity field instead of datetime-local inputs', () => {
    render(
      <BannerFormModal
        open
        mode="create"
        banner={null}
        onClose={() => undefined}
        onSuccess={() => undefined}
      />,
    );

    expect(screen.getByText('有效期')).toBeInTheDocument();
    expect(screen.getByText('至')).toBeInTheDocument();
    expect(document.querySelector('input[type="datetime-local"]')).toBeNull();
  });

  it('defaults to miniapp and only exposes the two supported positions', () => {
    renderBannerModal();

    const displayClientSelect = screen.getByRole('combobox', { name: '展示端' }) as HTMLSelectElement;
    expect(displayClientSelect).toBeDisabled();
    expect(displayClientSelect.value).toBe('MINIAPP_HOME');
    expect(Array.from(displayClientSelect.options).map((option) => option.textContent)).toEqual(['小程序']);
    const positionSelect = screen.getByRole('combobox', { name: '展示位置' }) as HTMLSelectElement;
    expect(Array.from(positionSelect.options).map((option) => option.textContent)).toEqual([
      '首页轮播',
      '品牌列表页轮播',
    ]);
    expect(positionSelect.value).toBe('MINIAPP_HOME_CAROUSEL');
    expect(screen.queryByText('Web 首页')).toBeNull();
  });

  it('adds brand detail jump with brand logo behavior like sku detail', async () => {
    const { container } = renderBannerModal();

    fireEvent.change(screen.getByLabelText(/Banner 标题/), { target: { value: '品牌轮播' } });
    fireEvent.change(screen.getByLabelText(/跳转类型/), { target: { value: 'BRAND_DETAIL' } });

    const brandInput = await screen.findByRole('combobox', { name: '关联品牌' });
    fireEvent.focus(brandInput);

    await waitFor(() => {
      expect(screen.getByRole('option', { name: '马可波罗 · MK' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('option', { name: '马可波罗 · MK' }));

    await waitFor(() => {
      expect(container.querySelector('.banner-upload-preview img')).toHaveAttribute(
        'src',
        '/media/images/default/brands/logos/mk.webp',
      );
    });

    fireEvent.click(screen.getByRole('button', { name: '保存 Banner' }));

    await waitFor(() => {
      expect(createBannerMock).toHaveBeenCalledWith(
        expect.objectContaining({
          jump_type: 'BRAND_DETAIL',
          brand_id: 3,
          image_source: 'brand_logo',
          image_object_key: 'images/default/brands/logos/mk.webp',
          sku_id: null,
          topic_id: null,
        }),
      );
    });
  });

  it('uses banner-modal-card only so admin modal-card 520px cascade cannot override 880px', () => {
    expect(userManagementCss).toMatch(/\.admin-shell \.modal-card\s*\{[^}]*width:\s*520px/);
    expect(systemSettingsCss).toMatch(/\.admin-shell \.modal-card\s*\{[^}]*width:\s*520px/);
    expect(bannerManagementCss).toMatch(/\.admin-shell \.banner-modal-card\s*\{[^}]*width:\s*880px/);

    const { container } = renderBannerModal();

    const modalCard = container.querySelector('.banner-modal-card');
    expect(modalCard).toBeTruthy();
    expect(modalCard?.classList.contains('modal-card')).toBe(false);
    expect(modalCard?.querySelector('.modal-body')).toBeTruthy();
    expect(modalCard?.querySelector('.modal-footer')).toBeTruthy();
  });

  it('keeps disabled display client select text visually centered', () => {
    expect(bannerManagementCss).toMatch(
      /\.admin-shell \.banner-display-client-select:disabled\s*\{[^}]*opacity:\s*1;[^}]*line-height:\s*40px;/s,
    );
  });
});
