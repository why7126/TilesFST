import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const createBrandMock = vi.hoisted(() => vi.fn());
const updateBrandMock = vi.hoisted(() => vi.fn());
const uploadBrandLogoMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('../api/brands-api', () => ({
  createBrand: (...args: unknown[]) => createBrandMock(...args),
  updateBrand: (...args: unknown[]) => updateBrandMock(...args),
  uploadBrandLogo: (...args: unknown[]) => uploadBrandLogoMock(...args),
}));

import { BrandFormModal } from './BrandFormModal';

describe('BrandFormModal', () => {
  beforeEach(() => {
    createBrandMock.mockReset();
    updateBrandMock.mockReset();
    uploadBrandLogoMock.mockReset();
  });

  it('uses a compact logo upload control and keeps uploaded logo key on submit', async () => {
    uploadBrandLogoMock.mockResolvedValue({
      object_key: 'brands/logo/demo.webp',
      url: 'https://cdn.example.test/demo.webp',
    });
    createBrandMock.mockResolvedValue(undefined);

    const onSuccess = vi.fn();
    const { container } = render(
      <BrandFormModal
        open
        mode="create"
        brand={null}
        onClose={vi.fn()}
        onSuccess={onSuccess}
      />,
    );

    expect(screen.getByText('品牌Logo', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.getByText('品牌 Logo')).toBeInTheDocument();
    expect(screen.getByText('支持 JPG / PNG / WebP，建议 1:1 方形图')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-upload')).toBeInTheDocument();
    expect(container.querySelector('.brand-upload')).not.toBeInTheDocument();

    const input = screen.getByLabelText('选择 Logo') as HTMLInputElement;
    expect(input.hidden).toBe(true);

    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandLogoMock).toHaveBeenCalledWith(file, expect.any(Function));
    });
    expect(await screen.findByText('已上传 Logo')).toBeInTheDocument();
    expect(screen.getByText('更换 Logo')).toBeInTheDocument();
    expect(screen.getByText('Logo 已更新')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/品牌名称/), { target: { value: '岩板品牌' } });
    fireEvent.click(screen.getByRole('button', { name: '保存品牌' }));

    await waitFor(() => {
      expect(createBrandMock).toHaveBeenCalledWith(
        expect.objectContaining({
          name: '岩板品牌',
          logo_object_key: 'brands/logo/demo.webp',
        }),
      );
    });
    expect(onSuccess).toHaveBeenCalledWith('品牌已创建');
  });

  it('previews an existing logo in edit mode and updates preview after replacement', async () => {
    uploadBrandLogoMock.mockResolvedValue({
      object_key: 'original/default/brands/logos/new.webp',
      url: '/media/original/default/brands/logos/new.webp',
    });

    const { container } = render(
      <BrandFormModal
        open
        mode="edit"
        brand={{
          id: 1,
          name: '岩板品牌',
          short_name: null,
          english_name: null,
          description: null,
          logo_object_key: 'original/default/brands/logos/old.webp',
          logo_url: '/media/original/default/brands/logos/old.webp',
          sort_order: 10,
          sku_count: 0,
          status: 'ENABLED',
          updated_at: '2026-06-20T00:00:00Z',
        }}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/old.webp',
    );

    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(screen.getByLabelText('更换 Logo'), { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandLogoMock).toHaveBeenCalledWith(file, expect.any(Function));
    });
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/new.webp',
    );
  });

  it('shows upload progress while a brand logo is uploading', async () => {
    let resolveUpload: (() => void) | undefined;
    uploadBrandLogoMock.mockImplementation(
      (_file: File, onProgress?: (progress: number) => void) => {
        onProgress?.(42);
        return new Promise((resolve) => {
          resolveUpload = () => {
            resolve({
              object_key: 'brands/logo/progress.webp',
              url: 'https://cdn.example.test/progress.webp',
            });
          };
        });
      },
    );

    const { container } = render(
      <BrandFormModal
        open
        mode="create"
        brand={null}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    const input = screen.getByLabelText('选择 Logo') as HTMLInputElement;
    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(input, { target: { files: [file] } });

    const progressbar = await screen.findByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuenow', '42');
    expect(screen.getByText('上传中 42%')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '保存品牌' })).toBeDisabled();
    expect(input.value).toBe('');

    await act(async () => {
      resolveUpload?.();
    });

    expect(await screen.findByText('Logo 已更新')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      'https://cdn.example.test/progress.webp',
    );
  });

  it('keeps the previous logo after upload failure and allows retrying the same file', async () => {
    uploadBrandLogoMock
      .mockRejectedValueOnce(new Error('upload failed'))
      .mockResolvedValueOnce({
        object_key: 'original/default/brands/logos/retry.webp',
        url: '/media/original/default/brands/logos/retry.webp',
      });

    const { container } = render(
      <BrandFormModal
        open
        mode="edit"
        brand={{
          id: 1,
          name: '岩板品牌',
          short_name: null,
          english_name: null,
          description: null,
          logo_object_key: 'original/default/brands/logos/old.webp',
          logo_url: '/media/original/default/brands/logos/old.webp',
          sort_order: 10,
          sku_count: 0,
          status: 'ENABLED',
          updated_at: '2026-06-20T00:00:00Z',
        }}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    const input = screen.getByLabelText('更换 Logo') as HTMLInputElement;
    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(input, { target: { files: [file] } });

    expect(await screen.findByRole('alert')).toHaveTextContent('Logo 上传失败');
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/old.webp',
    );
    expect(input.value).toBe('');

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandLogoMock).toHaveBeenCalledTimes(2);
    });
    expect(await screen.findByText('Logo 已更新')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/retry.webp',
    );
  });
});
