import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/tile-sku-management.css';
import '../styles/user-management.css';

const cssPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '../styles/tile-sku-management.css',
);
const tileSkuCss = readFileSync(cssPath, 'utf8');

const fetchBrandsMock = vi.hoisted(() => vi.fn());
const fetchCategoryTreeMock = vi.hoisted(() => vi.fn());
const fetchTileSpecsMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('../api/brands-api', () => ({
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('../api/tile-categories-api', () => ({
  fetchCategoryTree: (...args: unknown[]) => fetchCategoryTreeMock(...args),
}));

vi.mock('../api/tile-specs-api', () => ({
  fetchTileSpecs: (...args: unknown[]) => fetchTileSpecsMock(...args),
}));

vi.mock('../api/tile-skus-api', () => ({
  createTileSku: vi.fn(),
  updateTileSku: vi.fn(),
  uploadTileImage: vi.fn(),
  uploadTileVideo: vi.fn(),
}));

import { TileSkuFormModal } from './TileSkuFormModal';
import { uploadTileVideo } from '../api/tile-skus-api';

const uploadTileVideoMock = vi.mocked(uploadTileVideo);

function hasSkuModalScrollRule(): boolean {
  return (
    tileSkuCss.includes('.sku-modal-card .modal-body') &&
    tileSkuCss.includes('overflow-y: auto') &&
    tileSkuCss.includes('min-height: 0')
  );
}

function renderModal(props: Partial<React.ComponentProps<typeof TileSkuFormModal>> = {}) {
  const defaultProps = {
    open: true,
    mode: 'create' as const,
    sku: null,
    onClose: vi.fn(),
    onSuccess: vi.fn(),
  };
  return render(
    <div className="admin-shell">
      <TileSkuFormModal {...defaultProps} {...props} />
    </div>,
  );
}

describe('TileSkuFormModal', () => {
  beforeEach(() => {
    fetchBrandsMock.mockResolvedValue({ items: [{ id: 1, name: '测试品牌' }] });
    fetchCategoryTreeMock.mockResolvedValue([{ id: 10, name: '墙砖', children: [] }]);
    fetchTileSpecsMock.mockResolvedValue({
      items: [{ id: 5, display_name: '600×600mm', width_mm: 600, length_mm: 600, status: 'ENABLED' }],
    });
    uploadTileVideoMock.mockReset();
  });

  it('defines scrollable modal body styles for the sku modal card', async () => {
    const { container } = renderModal();
    expect(hasSkuModalScrollRule()).toBe(true);

    await waitFor(() => {
      expect(fetchBrandsMock).toHaveBeenCalled();
    });

    const modalCard = container.querySelector('.sku-modal-card');
    expect(modalCard?.querySelector('.modal-head')).toBeTruthy();
    expect(modalCard?.querySelector('.modal-body')).toBeTruthy();
    expect(modalCard?.querySelector('.modal-footer')).toBeTruthy();
  });

  it('renders create and edit modes with fixed footer actions', async () => {
    const { rerender, container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });
    expect(screen.getByRole('button', { name: '保存草稿' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '创建 SKU' })).toBeInTheDocument();

    rerender(
      <div className="admin-shell">
        <TileSkuFormModal
          open
          mode="edit"
          sku={{
            id: 99,
            name: '测试 SKU',
            sku_code: 'SKU-001',
            brand_id: 1,
            brand_name: '测试品牌',
            category_id: 10,
            category_name: '墙砖',
            spec_id: 5,
            size: '600×600mm',
            surface_finish: '哑光',
            color_family: null,
            reference_price: 268,
            remark: null,
            status: 'DRAFT',
            main_image_url: null,
            image_count: 0,
            video_count: 0,
            has_main_image: false,
            material_completeness: 'missing_main_image',
            images: [],
            videos: [],
            created_at: '2026-06-27T00:00:00Z',
            updated_at: '2026-06-27T00:00:00Z',
          }}
          onClose={vi.fn()}
          onSuccess={vi.fn()}
        />
      </div>,
    );

    expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '保存' })).toBeInTheDocument();
    expect(container.querySelector('.sku-modal-card .modal-body')).toBeTruthy();
  });

  it('uses optional surface finish and required reference price with default zero on create', async () => {
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const labels = Array.from(container.querySelectorAll('.brand-form-item label'));
    const surfaceLabel = labels.find((label) => label.textContent?.includes('表面工艺'));
    const priceLabel = labels.find((label) => label.textContent?.includes('参考价格（元）'));

    expect(surfaceLabel?.querySelector('.req')).toBeNull();
    expect(priceLabel?.querySelector('.req')).toBeTruthy();

    const priceInput = container.querySelector(
      'input[type="number"]',
    ) as HTMLInputElement | null;
    expect(priceInput?.value).toBe('0');
  });

  it('renders modal description with shared admin modal typography', async () => {
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const desc = container.querySelector('.modal-desc');
    expect(desc).toBeTruthy();
    expect(desc).toHaveTextContent('维护 SKU 基础资料、参考价格、图片与视频素材');
    expect(desc).toHaveTextContent('弹窗内不提供状态选择');
  });

  it('shows upload progress and video card after successful upload', async () => {
    uploadTileVideoMock.mockImplementation((_file, _tileId, onProgress) => {
      onProgress?.(42);
      return Promise.resolve({
        object_key: 'tile-videos/demo.mp4',
        url: '/media/tile-videos/demo.mp4',
      });
    });

    const { container } = renderModal();

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const input = container.querySelector(
      'input[accept="video/mp4"]',
    ) as HTMLInputElement | null;
    expect(input).toBeTruthy();

    fireEvent.change(input!, {
      target: { files: [new File(['video'], 'demo.mp4', { type: 'video/mp4' })] },
    });

    await waitFor(() => {
      expect(screen.getByText(/上传中 42%/)).toBeInTheDocument();
    });

    await waitFor(() => {
      const player = container.querySelector('video.sku-video-player') as HTMLVideoElement | null;
      expect(player).toBeTruthy();
      expect(player?.src).toContain('/media/tile-videos/demo.mp4');
      expect(screen.getByText('demo.mp4')).toBeInTheDocument();
      expect(screen.getByText('视频已添加')).toBeInTheDocument();
    });
  });

  it('requires tile spec when creating SKU', async () => {
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const inputs = container.querySelectorAll('.brand-form-item .input');
    fireEvent.change(inputs[0]!, { target: { value: '测试 SKU' } });
    fireEvent.change(inputs[1]!, { target: { value: 'SKU-SPEC-001' } });

    const selects = container.querySelectorAll('.brand-form-item .select');
    fireEvent.change(selects[0]!, { target: { value: '1' } });
    fireEvent.change(selects[1]!, { target: { value: '10' } });

    fireEvent.click(screen.getByRole('button', { name: '创建 SKU' }));

    await waitFor(() => {
      expect(screen.getByText('请选择瓷砖规格')).toBeInTheDocument();
    });
  });

  it('shows form-help hint when editing historical SKU without spec_id', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: {
        id: 100,
        name: '历史 SKU',
        sku_code: 'SKU-LEGACY-001',
        brand_id: 1,
        brand_name: '测试品牌',
        category_id: 10,
        category_name: '墙砖',
        spec_id: null,
        size: '800×800mm',
        surface_finish: '哑光',
        color_family: null,
        reference_price: 100,
        remark: null,
        status: 'DRAFT',
        main_image_url: null,
        image_count: 0,
        video_count: 0,
        has_main_image: false,
        material_completeness: 'missing_main_image',
        images: [],
        videos: [],
        created_at: '2026-06-27T00:00:00Z',
        updated_at: '2026-06-27T00:00:00Z',
      },
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    const hint = container.querySelector('.form-help');
    expect(hint).toBeTruthy();
    expect(hint).toHaveTextContent('历史 SKU 未匹配规格，请手动选择后保存');
    expect(container.querySelector('.form-hint')).toBeNull();
  });

  it('hides spec mismatch hint after selecting a tile spec in edit mode', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: {
        id: 100,
        name: '历史 SKU',
        sku_code: 'SKU-LEGACY-001',
        brand_id: 1,
        brand_name: '测试品牌',
        category_id: 10,
        category_name: '墙砖',
        spec_id: null,
        size: '800×800mm',
        surface_finish: '哑光',
        color_family: null,
        reference_price: 100,
        remark: null,
        status: 'DRAFT',
        main_image_url: null,
        image_count: 0,
        video_count: 0,
        has_main_image: false,
        material_completeness: 'missing_main_image',
        images: [],
        videos: [],
        created_at: '2026-06-27T00:00:00Z',
        updated_at: '2026-06-27T00:00:00Z',
      },
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    const specSelect = container.querySelectorAll('.brand-form-item .select')[2];
    fireEvent.change(specSelect!, { target: { value: '5' } });

    await waitFor(() => {
      expect(container.querySelector('.form-help')).toBeNull();
    });
  });

  it('does not show spec mismatch hint on create mode', async () => {
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    expect(container.querySelector('.form-help')).toBeNull();
    expect(screen.queryByText('历史 SKU 未匹配规格，请手动选择后保存')).toBeNull();
  });

  it('shows video section error when upload fails', async () => {
    uploadTileVideoMock.mockRejectedValue(new Error('network'));

    const { container } = renderModal();

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const input = container.querySelector(
      'input[accept="video/mp4"]',
    ) as HTMLInputElement | null;
    fireEvent.change(input!, {
      target: { files: [new File(['video'], 'bad.mp4', { type: 'video/mp4' })] },
    });

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('视频上传失败');
    });
    expect(container.querySelector('video.sku-video-player')).toBeNull();
  });
});
