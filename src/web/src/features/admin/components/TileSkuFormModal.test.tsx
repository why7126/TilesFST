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
const fetchSettingsGroupMock = vi.hoisted(() => vi.fn());

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

vi.mock('../api/system-settings-api', () => ({
  fetchSettingsGroup: (...args: unknown[]) => fetchSettingsGroupMock(...args),
}));

vi.mock('../api/tile-skus-api', () => ({
  createTileSku: vi.fn(),
  updateTileSku: vi.fn(),
  uploadTileImage: vi.fn(),
  uploadTileVideo: vi.fn(),
}));

import { removeImageDraft, TileSkuFormModal } from './TileSkuFormModal';
import { createTileSku, updateTileSku, uploadTileImage, uploadTileVideo } from '../api/tile-skus-api';

const uploadTileImageMock = vi.mocked(uploadTileImage);
const uploadTileVideoMock = vi.mocked(uploadTileVideo);
const createTileSkuMock = vi.mocked(createTileSku);
const updateTileSkuMock = vi.mocked(updateTileSku);

function editableSku(images: Array<{ object_key: string; url: string; is_main: boolean; sort_order?: number }>) {
  return {
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
    main_image_url: images.find((img) => img.is_main)?.url ?? null,
    image_count: images.length,
    video_count: 0,
    has_main_image: images.some((img) => img.is_main),
    material_completeness: images.some((img) => img.is_main) ? 'complete' : 'missing_main_image',
    images,
    videos: [],
    created_at: '2026-06-27T00:00:00Z',
    updated_at: '2026-06-27T00:00:00Z',
  };
}

function imageSources(container: HTMLElement): string[] {
  return Array.from(container.querySelectorAll('.sku-image-tile img')).map((img) =>
    (img as HTMLImageElement).getAttribute('src') ?? '',
  );
}

function hasSkuModalScrollRule(): boolean {
  return (
    tileSkuCss.includes('.sku-modal-card .modal-body') &&
    tileSkuCss.includes('overflow-y: auto') &&
    tileSkuCss.includes('min-height: 0')
  );
}

function hasLargeVideoTileRule(): boolean {
  return (
    tileSkuCss.includes('.sku-video-grid') &&
    tileSkuCss.includes('grid-template-columns: repeat(2, minmax(0, 1fr))') &&
    tileSkuCss.includes('align-items: stretch') &&
    tileSkuCss.includes('.sku-video-grid .sku-add-tile') &&
    tileSkuCss.includes('min-height: 280px') &&
    tileSkuCss.includes('.sku-video-player-wrap') &&
    tileSkuCss.includes('aspect-ratio: 16 / 9')
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
    fetchSettingsGroupMock.mockResolvedValue({
      max_image_size_mb: 50,
      max_video_size_mb: 200,
      allowed_image_types: 'image/jpeg,image/png,image/webp,image/gif',
      allowed_video_types: 'video/mp4,video/quicktime,video/webm',
    });
    uploadTileImageMock.mockReset();
    uploadTileVideoMock.mockReset();
    createTileSkuMock.mockReset();
    updateTileSkuMock.mockReset();
    createTileSkuMock.mockResolvedValue({ id: 1 });
    updateTileSkuMock.mockResolvedValue({ id: 99 });
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

  it('keeps video cards and add-video tile in the original large layout', async () => {
    renderModal();

    await waitFor(() => {
      expect(fetchBrandsMock).toHaveBeenCalled();
    });

    expect(hasLargeVideoTileRule()).toBe(true);
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
    expect(screen.queryByText('SKU 编码')).not.toBeInTheDocument();
    expect(screen.queryByDisplayValue('SKU-001')).not.toBeInTheDocument();
    expect(container.querySelector('.sku-modal-card .modal-body')).toBeTruthy();
  });

  it('uses required reference price before optional surface finish with default zero on create', async () => {
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    const labels = Array.from(container.querySelectorAll('.brand-form-item label'));
    const surfaceLabel = labels.find((label) => label.textContent?.includes('表面工艺'));
    const priceLabel = labels.find((label) => label.textContent?.includes('参考价格（元）'));

    expect(surfaceLabel?.querySelector('.req')).toBeNull();
    expect(priceLabel?.querySelector('.req')).toBeTruthy();
    expect(labels.indexOf(priceLabel!)).toBeLessThan(labels.indexOf(surfaceLabel!));

    const priceInput = container.querySelector(
      'input[type="number"]',
    ) as HTMLInputElement | null;
    expect(priceInput?.value).toBe('0');
  });

  it('shows upload type, size and multi-upload hints for images and videos', async () => {
    renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(
        screen.getByText('支持 JPG、PNG、WebP、GIF，单张最大 50MB；可上传多张，并指定一张主图'),
      ).toBeInTheDocument();
    });
    expect(screen.getByText('支持 MP4、MOV、WebM，单个视频最大 200MB；可上传多个视频')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /继续添加图片/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /继续添加视频/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '上传视频' })).not.toBeInTheDocument();
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

    let input: HTMLInputElement | null = null;
    await waitFor(() => {
      input = container.querySelector(
        'input[accept="video/mp4,video/quicktime,video/webm"]',
      ) as HTMLInputElement | null;
      expect(input).toBeTruthy();
    });

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

    const selects = container.querySelectorAll('.brand-form-item .select');
    fireEvent.change(selects[0]!, { target: { value: '1' } });
    fireEvent.change(selects[1]!, { target: { value: '10' } });

    fireEvent.click(screen.getByRole('button', { name: '创建 SKU' }));

    await waitFor(() => {
      expect(screen.getByText('请选择瓷砖规格')).toBeInTheDocument();
    });
  });

  it('does not require or submit manual SKU code on create', async () => {
    const onSuccess = vi.fn();
    const { container } = renderModal({ mode: 'create', onSuccess });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    expect(screen.getByText('商品名称')).toBeInTheDocument();
    expect(screen.queryByText('SKU 名称')).not.toBeInTheDocument();
    expect(screen.queryByText('SKU 编码')).not.toBeInTheDocument();

    const nameInput = container.querySelector('.brand-form-item .input') as HTMLInputElement;
    fireEvent.change(nameInput, { target: { value: '测试商品' } });

    const selects = container.querySelectorAll('.brand-form-item .select');
    fireEvent.change(selects[0]!, { target: { value: '1' } });
    fireEvent.change(selects[1]!, { target: { value: '10' } });
    fireEvent.change(selects[2]!, { target: { value: '5' } });

    fireEvent.click(screen.getByRole('button', { name: '创建 SKU' }));

    await waitFor(() => {
      expect(createTileSkuMock).toHaveBeenCalled();
    });
    expect(createTileSkuMock.mock.calls[0]?.[0]).toMatchObject({
      name: '测试商品',
      save_mode: 'create',
    });
    expect(createTileSkuMock.mock.calls[0]?.[0]).not.toHaveProperty('sku_code');
    expect(onSuccess).toHaveBeenCalledWith('SKU 创建成功，已保存为草稿');
  });

  it('removes a non-main image while keeping the current main image first in payload', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: editableSku([
        { object_key: 'img-a', url: '/media/img-a.webp', is_main: true, sort_order: 0 },
        { object_key: 'img-b', url: '/media/img-b.webp', is_main: false, sort_order: 1 },
        { object_key: 'img-c', url: '/media/img-c.webp', is_main: false, sort_order: 2 },
      ]),
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '移除图片 2' }));

    expect(imageSources(container)).toEqual(['/media/img-a.webp', '/media/img-c.webp']);
    expect(screen.getByText('主图')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(updateTileSkuMock).toHaveBeenCalled();
    });
    expect(updateTileSkuMock.mock.calls[0]?.[1]).toMatchObject({
      images: [
        { object_key: 'img-a', is_main: true, sort_order: 0 },
        { object_key: 'img-c', is_main: false, sort_order: 1 },
      ],
    });
  });

  it('moves a selected main image to the first position and submits it with sort_order zero', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: editableSku([
        { object_key: 'img-a', url: '/media/img-a.webp', is_main: true, sort_order: 0 },
        { object_key: 'img-b', url: '/media/img-b.webp', is_main: false, sort_order: 1 },
        { object_key: 'img-c', url: '/media/img-c.webp', is_main: false, sort_order: 2 },
      ]),
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getAllByRole('button', { name: '设为主图' })[1]!);

    expect(imageSources(container)).toEqual([
      '/media/img-c.webp',
      '/media/img-a.webp',
      '/media/img-b.webp',
    ]);

    fireEvent.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(updateTileSkuMock).toHaveBeenCalled();
    });
    expect(updateTileSkuMock.mock.calls[0]?.[1]).toMatchObject({
      images: [
        { object_key: 'img-c', is_main: true, sort_order: 0 },
        { object_key: 'img-a', is_main: false, sort_order: 1 },
        { object_key: 'img-b', is_main: false, sort_order: 2 },
      ],
    });
  });

  it('promotes the next image when removing the current main image', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: editableSku([
        { object_key: 'img-a', url: '/media/img-a.webp', is_main: true, sort_order: 0 },
        { object_key: 'img-b', url: '/media/img-b.webp', is_main: false, sort_order: 1 },
        { object_key: 'img-c', url: '/media/img-c.webp', is_main: false, sort_order: 2 },
      ]),
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '移除图片 1' }));

    expect(imageSources(container)).toEqual(['/media/img-b.webp', '/media/img-c.webp']);

    fireEvent.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(updateTileSkuMock).toHaveBeenCalled();
    });
    expect(updateTileSkuMock.mock.calls[0]?.[1]).toMatchObject({
      images: [
        { object_key: 'img-b', is_main: true, sort_order: 0 },
        { object_key: 'img-c', is_main: false, sort_order: 1 },
      ],
    });
  });

  it('falls back to the remaining first image when removing a last-position main image', () => {
    expect(
      removeImageDraft(
        [
          { object_key: 'img-a', url: '/media/img-a.webp', is_main: false, sort_order: 0 },
          { object_key: 'img-b', url: '/media/img-b.webp', is_main: false, sort_order: 1 },
          { object_key: 'img-c', url: '/media/img-c.webp', is_main: true, sort_order: 2 },
        ],
        2,
      ),
    ).toEqual([
      { object_key: 'img-a', url: '/media/img-a.webp', is_main: true, sort_order: 0 },
      { object_key: 'img-b', url: '/media/img-b.webp', is_main: false, sort_order: 1 },
    ]);
  });

  it('submits an empty image list after removing all images and keeps the add image entry visible', async () => {
    const { container } = renderModal({
      mode: 'edit',
      sku: editableSku([
        { object_key: 'img-a', url: '/media/img-a.webp', is_main: true, sort_order: 0 },
      ]),
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '编辑 SKU' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '移除图片 1' }));

    expect(container.querySelector('.sku-image-tile')).toBeNull();
    expect(screen.queryByText('主图')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /继续添加图片/ })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(updateTileSkuMock).toHaveBeenCalled();
    });
    expect(updateTileSkuMock.mock.calls[0]?.[1]).toMatchObject({ images: [] });
  });

  it('keeps newly uploaded images visible and removable without changing the upload API', async () => {
    uploadTileImageMock.mockResolvedValue({
      object_key: 'img-new',
      url: '/media/img-new.webp',
    });
    const { container } = renderModal({ mode: 'create' });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /新增 SKU/i })).toBeInTheDocument();
    });

    let input: HTMLInputElement | null = null;
    await waitFor(() => {
      input = container.querySelector(
        'input[accept="image/jpeg,image/png,image/webp,image/gif"]',
      ) as HTMLInputElement | null;
      expect(input).toBeTruthy();
    });
    fireEvent.change(input!, {
      target: { files: [new File(['image'], 'new.webp', { type: 'image/webp' })] },
    });

    await waitFor(() => {
      expect(imageSources(container)).toEqual(['/media/img-new.webp']);
    });
    expect(screen.getByRole('button', { name: '移除图片 1' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '移除图片 1' }));
    expect(container.querySelector('.sku-image-tile')).toBeNull();
    expect(screen.getByRole('button', { name: /继续添加图片/ })).toBeInTheDocument();
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

    expect(screen.getByText('历史 SKU 未匹配规格，请手动选择后保存')).toBeInTheDocument();
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
      expect(screen.queryByText('历史 SKU 未匹配规格，请手动选择后保存')).toBeNull();
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

    let input: HTMLInputElement | null = null;
    await waitFor(() => {
      input = container.querySelector(
        'input[accept="video/mp4,video/quicktime,video/webm"]',
      ) as HTMLInputElement | null;
      expect(input).toBeTruthy();
    });
    fireEvent.change(input!, {
      target: { files: [new File(['video'], 'bad.mp4', { type: 'video/mp4' })] },
    });

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('视频上传失败');
    });
    expect(container.querySelector('video.sku-video-player')).toBeNull();
  });
});
