import type { ImgHTMLAttributes } from 'react';
// Form tests verify stable business values; authorization/blob lifecycle has independent tests.
vi.mock('@/features/media/authorized-media', () => ({
  AuthorizedImage: ({reference: _reference, file: _file, ...props}: ImgHTMLAttributes<HTMLImageElement> & {reference?: unknown; file?: File}) => <img {...props} />,
}));
import { readFileSync } from 'node:fs';
import path from 'node:path';
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

const brandManagementCss = readFileSync(
  path.join(process.cwd(), 'src/features/admin/styles/brand-management.css'),
  'utf8',
);

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

    expect(screen.getByText('Logo', { selector: '.field-label' })).toBeInTheDocument();
    expect(screen.queryByText('品牌Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌 Logo')).not.toBeInTheDocument();
    expect(screen.getByText('支持 JPG / PNG / WebP，建议 1:1 方形图')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-upload')).toBeInTheDocument();
    expect(container.querySelector('.brand-upload')).not.toBeInTheDocument();

    const input = screen.getByLabelText('选择 Logo') as HTMLInputElement;
    expect(input.hidden).toBe(true);

    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandLogoMock).toHaveBeenCalledWith(file, expect.any(Function), expect.any(Object));
    });
    expect(screen.queryByText('已上传 Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌 Logo')).not.toBeInTheDocument();
    expect(screen.getByText('更换 Logo')).toBeInTheDocument();
    expect(screen.getByText('图片已添加')).toBeInTheDocument();

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

  it('keeps the logo preview top aligned with the upload format hint', () => {
    expect(brandManagementCss).toMatch(
      /\.admin-shell \.brand-logo-meta \{[\s\S]*?align-items:\s*flex-start;/,
    );
    expect(brandManagementCss).toMatch(
      /\.admin-shell \.brand-logo-preview \{[\s\S]*?margin-top:\s*8px;/,
    );
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
          created_at: '2026-06-20T00:00:00Z',
          updated_at: '2026-06-20T00:00:00Z',
        }}
        onClose={vi.fn()}
        onSuccess={vi.fn()}
      />,
    );

    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/old.webp',
    );
    expect(screen.queryByText('已上传 Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌 Logo')).not.toBeInTheDocument();

    const file = new File(['logo'], 'logo.webp', { type: 'image/webp' });
    fireEvent.change(screen.getByLabelText('更换 Logo'), { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandLogoMock).toHaveBeenCalledWith(file, expect.any(Function), expect.any(Object));
    });
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/new.webp',
    );
    expect(screen.queryByText('已上传 Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌Logo')).not.toBeInTheDocument();
    expect(screen.queryByText('品牌 Logo')).not.toBeInTheDocument();
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

    expect(await screen.findByText('图片已添加')).toBeInTheDocument();
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
          created_at: '2026-06-20T00:00:00Z',
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
    expect(await screen.findByText('图片已添加')).toBeInTheDocument();
    expect(container.querySelector('.brand-logo-preview img')?.getAttribute('src')).toBe(
      '/media/original/default/brands/logos/retry.webp',
    );
  });
});

it('blocks saving during processing and cancels before leaving, fencing a late result', async () => {
  createBrandMock.mockReset(); uploadBrandLogoMock.mockReset();
  const cancel = vi.fn().mockResolvedValue(undefined);
  let finish: ((value: unknown) => void) | undefined;
  uploadBrandLogoMock.mockImplementation((_file, _progress, options) => {
    options.onTask({ cancel });
    options.onUpdate({ stage: 'processing', progress: 100 });
    return new Promise(resolve => { finish = resolve; });
  });
  const onClose = vi.fn();
  render(<BrandFormModal open mode="create" brand={null} onClose={onClose} onSuccess={vi.fn()} />);
  fireEvent.change(screen.getByLabelText('选择 Logo'), {
    target: { files: [new File(['logo'], 'logo.png', { type: 'image/png' })] },
  });
  expect(await screen.findByText('正在生成图片展示版本')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: '保存品牌' })).toBeDisabled();
  fireEvent.click(screen.getByRole('button', { name: '关闭' }));
  expect(screen.getByRole('alertdialog')).toBeInTheDocument();
  expect(cancel).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: '取消上传并离开' }));
  await waitFor(() => expect(onClose).toHaveBeenCalledOnce());
  expect(cancel).toHaveBeenCalledOnce();
  await act(async () => finish?.({ object_key: 'late', url: '/media/late' }));
  expect(screen.queryByText('图片已添加')).not.toBeInTheDocument();
  expect(createBrandMock).not.toHaveBeenCalled();
});
