import { useState, type ChangeEvent } from 'react';

import {
  displayStatusLabel,
  formatValidityRange,
  isPdfFile,
  validityBadgeClass,
  validityStatusLabel,
} from '@/features/admin/lib/brand-certificate-display';
import { cn } from '@/shared/lib/cn';
import type { BrandCertificateFile, BrandCertificateItem } from '@/shared/api/generated';

type CertificateFileLike = Pick<
  BrandCertificateFile,
  'file_url' | 'file_name' | 'file_mime_type' | 'file_size_bytes'
>;

type CertificateSummaryLike = Pick<
  BrandCertificateItem,
  'name' | 'certificate_no' | 'file_name'
> & {
  brand_name?: string | null;
};

type CertificateValidityLike = Pick<
  BrandCertificateItem,
  'is_permanent' | 'effective_date' | 'expiry_date' | 'validity_status'
>;

type CertificateVisibilityLike = Pick<BrandCertificateItem, 'is_visible'>;

export type CertificateFileCardState = 'idle' | 'uploading' | 'done' | 'failed';

export const CERTIFICATE_PREVIEW_UNAVAILABLE_REASON = '证书文件暂时无法预览';

export function getCertificatePreviewTarget(fileUrl?: string | null) {
  if (!fileUrl) {
    return {
      ok: false as const,
      reason: CERTIFICATE_PREVIEW_UNAVAILABLE_REASON,
    };
  }

  return {
    ok: true as const,
    url: fileUrl,
  };
}

export function CertificateThumb({
  fileUrl,
  fileName,
  fileMimeType,
  className,
}: {
  fileUrl?: string | null;
  fileName?: string | null;
  fileMimeType?: string | null;
  className?: string;
}) {
  const [failed, setFailed] = useState(false);
  const isPdf = isPdfFile(fileMimeType, fileName);
  const canRenderImage = Boolean(fileUrl) && !isPdf && !failed;

  return (
    <span
      className={cn(
        'certificate-thumb',
        (!fileUrl || failed) && 'is-fallback',
        isPdf && 'is-pdf',
        className,
      )}
    >
      {canRenderImage ? (
        <img src={fileUrl!} alt="" onError={() => setFailed(true)} />
      ) : (
        <span>{isPdf ? 'PDF' : 'FILE'}</span>
      )}
    </span>
  );
}

export function CertificateSummary({
  certificate,
  showBrand = false,
}: {
  certificate: CertificateSummaryLike;
  showBrand?: boolean;
}) {
  return (
    <span className="certificate-summary">
      <span className="brand-name" title={certificate.name}>
        {certificate.name}
      </span>
      <span className="brand-sub" title={certificate.certificate_no || certificate.file_name}>
        {certificate.certificate_no || certificate.file_name}
      </span>
      {showBrand && certificate.brand_name ? (
        <span className="brand-sub" title={certificate.brand_name}>
          {certificate.brand_name}
        </span>
      ) : null}
    </span>
  );
}

export function CertificateListIdentity({
  certificate,
}: {
  certificate: CertificateSummaryLike &
    Pick<BrandCertificateItem, 'file_url' | 'file_mime_type'>;
}) {
  return (
    <div className="certificate-cell">
      <CertificateThumb
        fileUrl={certificate.file_url}
        fileName={certificate.file_name}
        fileMimeType={certificate.file_mime_type}
      />
      <CertificateSummary certificate={certificate} />
    </div>
  );
}

export function CertificateValidityText({ certificate }: { certificate: CertificateValidityLike }) {
  return <>{formatValidityRange(certificate)}</>;
}

export function CertificateValidityBadge({
  status,
}: {
  status: BrandCertificateItem['validity_status'] | string;
}) {
  return <span className={validityBadgeClass(status)}>{validityStatusLabel(status)}</span>;
}

export function CertificateVisibilityBadge({ certificate }: { certificate: CertificateVisibilityLike }) {
  return (
    <span className={certificate.is_visible ? 'badge enabled' : 'badge disabled'}>
      {displayStatusLabel(certificate)}
    </span>
  );
}

export function CertificatePreviewAction({
  fileUrl,
  onPreview,
  onUnavailable,
}: {
  fileUrl?: string | null;
  onPreview: (url: string) => void;
  onUnavailable?: (reason: string) => void;
}) {
  return (
    <button
      type="button"
      className="link-btn"
      onClick={() => {
        const target = getCertificatePreviewTarget(fileUrl);
        if (target.ok) {
          onPreview(target.url);
          return;
        }
        onUnavailable?.(target.reason);
      }}
    >
      预览
    </button>
  );
}

export function CertificateFileCard({
  file,
  state,
  progress = 0,
  error,
  onSelectFile,
  onRemove,
  maxFileSizeMb = 25,
}: {
  file: CertificateFileLike | null;
  state: CertificateFileCardState;
  progress?: number;
  error?: string | null;
  onSelectFile: (file: File) => void;
  onRemove: () => void;
  maxFileSizeMb?: number;
}) {
  const isUploading = state === 'uploading';
  const normalizedProgress = Math.min(100, Math.max(0, Math.round(progress)));

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const input = event.currentTarget;
    const selected = input.files?.[0];
    if (selected) {
      onSelectFile(selected);
    }
    input.value = '';
  };

  return (
    <div className={cn('certificate-upload', state === 'failed' && 'is-failed')}>
      <div className="certificate-file-card">
        <CertificateThumb
          className="certificate-file-thumb"
          fileUrl={file?.file_url}
          fileName={file?.file_name}
          fileMimeType={file?.file_mime_type}
        />
        <span className="certificate-file-meta">
          <span className="user-main">{file ? file.file_name : '未上传证书文件'}</span>
          <span className="user-sub">
            {file?.file_size_bytes ? `${Math.ceil(file.file_size_bytes / 1024)} KB` : `支持 JPG / PNG / WebP / PDF，单文件最大 ${maxFileSizeMb}MB`}
          </span>
          {isUploading ? (
            <span className="brand-logo-status">
              <span
                className="brand-logo-progress"
                role="progressbar"
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={normalizedProgress}
              >
                <span
                  className="brand-logo-progress-bar"
                  style={{ width: `${normalizedProgress}%` }}
                />
              </span>
              <span className="brand-logo-progress-text">上传中 {normalizedProgress}%</span>
            </span>
          ) : null}
          {state === 'done' && file ? (
            <span className="brand-logo-upload-success">证书文件已就绪</span>
          ) : null}
          {state === 'failed' && error ? (
            <span className="brand-logo-upload-error" role="alert">
              {error}
            </span>
          ) : null}
        </span>
      </div>
      <div className="certificate-upload-actions">
        {file ? (
          <button type="button" className="btn" onClick={onRemove}>
            移除
          </button>
        ) : null}
        <label className={cn('btn', isUploading && 'disabled')} aria-disabled={isUploading}>
          {isUploading ? '上传中' : file ? '重新上传' : '选择文件'}
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp,application/pdf"
            disabled={isUploading}
            hidden
            onChange={handleInputChange}
          />
        </label>
      </div>
    </div>
  );
}
