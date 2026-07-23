import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import {
  CertificateFileCard,
  CertificateListIdentity,
  CertificatePreviewAction,
  CertificateValidityBadge,
  CertificateValidityText,
  CertificateVisibilityBadge,
  getCertificatePreviewTarget,
} from './BrandCertificateComponents';
import type { BrandCertificateFile, BrandCertificateItem } from '@/shared/api/generated';

const certificate = {
  id: 7,
  brand_id: 1,
  brand_name: '岩板品牌',
  name: 'ISO 9001 质量管理体系认证',
  sort_order: 10,
  type: 'QUALITY',
  certificate_no: 'ISO-001',
  issuer: '认证机构',
  file_url: '/media/files/default/brand-certificates/iso.pdf',
  file_key: 'files/default/brand-certificates/iso.pdf',
  file_name: 'iso.pdf',
  file_mime_type: 'application/pdf',
  file_size_bytes: 128,
  is_permanent: false,
  effective_date: '2026-01-01',
  expiry_date: '2026-12-31',
  validity_status: 'VALID',
  is_visible: true,
  display_status: 'VISIBLE',
  remark: null,
  created_at: '2026-07-15T00:00:00Z',
  updated_at: '2026-07-15T00:00:00Z',
} as BrandCertificateItem;

const file = {
  file_url: '/media/files/default/brand-certificates/iso.pdf',
  file_key: 'files/default/brand-certificates/iso.pdf',
  file_name: 'iso.pdf',
  file_mime_type: 'application/pdf',
  file_size_bytes: 2048,
} as BrandCertificateFile;

describe('BrandCertificateComponents', () => {
  it('renders certificate identity with pdf placeholder and summary fallback', () => {
    render(
      <CertificateListIdentity
        certificate={{
          ...certificate,
          certificate_no: null,
        }}
      />,
    );

    expect(screen.getByText('PDF')).toBeInTheDocument();
    expect(screen.getByText('ISO 9001 质量管理体系认证')).toBeInTheDocument();
    expect(screen.getByText('iso.pdf')).toBeInTheDocument();
  });

  it('falls back to original validity status and visibility labels', () => {
    render(
      <>
        <CertificateValidityText
          certificate={{
            ...certificate,
            is_permanent: false,
            effective_date: null,
            expiry_date: '2026-12-31',
          }}
        />
        <CertificateValidityBadge status="UNKNOWN_STATUS" />
        <CertificateVisibilityBadge certificate={{ is_visible: false }} />
      </>,
    );

    expect(screen.getByText('至 2026-12-31')).toBeInTheDocument();
    expect(screen.getByText('UNKNOWN_STATUS')).toBeInTheDocument();
    expect(screen.getByText('隐藏')).toBeInTheDocument();
  });

  it('returns preview target or unavailable reason without opening storage URLs itself', () => {
    expect(getCertificatePreviewTarget('/media/file.pdf')).toEqual({
      ok: true,
      url: '/media/file.pdf',
    });
    expect(getCertificatePreviewTarget(null)).toEqual({
      ok: false,
      reason: '证书文件暂时无法预览',
    });

    const onPreview = vi.fn();
    const onUnavailable = vi.fn();
    render(
      <CertificatePreviewAction
        fileUrl={null}
        onPreview={onPreview}
        onUnavailable={onUnavailable}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: '预览' }));

    expect(onPreview).not.toHaveBeenCalled();
    expect(onUnavailable).toHaveBeenCalledWith('证书文件暂时无法预览');
  });

  it('renders file card states and delegates file selection callbacks', () => {
    const onSelectFile = vi.fn();
    const onRemove = vi.fn();
    const { rerender } = render(
      <CertificateFileCard
        file={null}
        state="idle"
        onSelectFile={onSelectFile}
        onRemove={onRemove}
      />,
    );

    expect(screen.getByText('未上传证书文件')).toBeInTheDocument();
    expect(screen.getByText('支持 JPG / PNG / WebP / PDF，单文件最大 25MB')).toBeInTheDocument();
    expect(screen.getByText('选择文件')).toBeInTheDocument();

    const selected = new File(['pdf'], 'new.pdf', { type: 'application/pdf' });
    fireEvent.change(document.querySelector('input[type="file"]') as HTMLInputElement, {
      target: { files: [selected] },
    });
    expect(onSelectFile).toHaveBeenCalledWith(selected);

    rerender(
      <CertificateFileCard
        file={file}
        state="uploading"
        progress={42}
        onSelectFile={onSelectFile}
        onRemove={onRemove}
      />,
    );
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '42');
    expect(screen.getByText('上传中 42%')).toBeInTheDocument();

    rerender(
      <CertificateFileCard
        file={file}
        state="done"
        onSelectFile={onSelectFile}
        onRemove={onRemove}
      />,
    );
    expect(screen.getByText('证书文件已就绪')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '移除' }));
    expect(onRemove).toHaveBeenCalled();

    rerender(
      <CertificateFileCard
        file={file}
        state="failed"
        error="证书文件上传失败"
        onSelectFile={onSelectFile}
        onRemove={onRemove}
      />,
    );
    expect(screen.getByRole('alert')).toHaveTextContent('证书文件上传失败');
    expect(within(screen.getByText('iso.pdf').closest('.certificate-file-card')!).getByText('PDF')).toBeInTheDocument();
  });
});
