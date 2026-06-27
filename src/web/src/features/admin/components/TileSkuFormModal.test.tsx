import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import '../styles/tile-sku-management.css';

const cssPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '../styles/tile-sku-management.css',
);
const tileSkuCss = readFileSync(cssPath, 'utf8');

const fetchBrandsMock = vi.hoisted(() => vi.fn());
const fetchCategoryTreeMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('../api/brands-api', () => ({
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('../api/tile-categories-api', () => ({
  fetchCategoryTree: (...args: unknown[]) => fetchCategoryTreeMock(...args),
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
            size: '600×600',
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
