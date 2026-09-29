import { useModalReturnFocus } from './use-modal-return-focus';
import { AuthorizedImage } from '@/features/media/authorized-media';
import { useEffect, useRef, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BrandAdminItem } from '@/shared/api/generated';

import { createBrand, updateBrand, uploadBrandLogo } from '../api/brands-api';

import { MediaUploadStatus, type UploadStage } from '@/features/media/media-upload-status';
import type { MediaUploadTask } from '@/features/media/media-upload-controller';

type LogoUploadState = UploadStage | 'uploading';

interface BrandFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  brand: BrandAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function BrandFormModal({ open, mode, brand, onClose, onSuccess }: BrandFormModalProps) {
  useModalReturnFocus(open);
  const [name, setName] = useState('');
  const [sortOrder, setSortOrder] = useState('10');
  const [shortName, setShortName] = useState('');
  const [englishName, setEnglishName] = useState('');
  const [description, setDescription] = useState('');
  const [logoKey, setLogoKey] = useState<string | null>(null);
  const [logoUrl, setLogoUrl] = useState<string | null>(null);
  const [logoUploadState, setLogoUploadState] = useState<LogoUploadState>('idle');
  const [logoUploadProgress, setLogoUploadProgress] = useState(0);
  const [logoUploadError, setLogoUploadError] = useState<string | null>(null);
  const task = useRef<MediaUploadTask | null>(null);
  const fileRef = useRef<File | undefined>(undefined);
  const epoch = useRef(0);
  const [leavePrompt, setLeavePrompt] = useState(false);
  const [warning, setWarning] = useState<string | undefined>();
  const [retryable, setRetryable] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setLeavePrompt(false); setWarning(undefined);
    setLogoUploadState('idle');
    setLogoUploadProgress(0);
    setLogoUploadError(null);
    if (mode === 'edit' && brand) {
      setName(brand.name);
      setSortOrder(String(brand.sort_order));
      setShortName(brand.short_name ?? '');
      setEnglishName(brand.english_name ?? '');
      setDescription(brand.description ?? '');
      setLogoKey(brand.logo_object_key ?? null);
      setLogoUrl(brand.logo_url ?? null);
    } else {
      setName('');
      setSortOrder('10');
      setShortName('');
      setEnglishName('');
      setDescription('');
      setLogoKey(null);
      setLogoUrl(null);
    }
  }, [open, mode, brand]);

  useEffect(() => () => {
    epoch.current++;
    void task.current?.cancel().catch(() => undefined);
  }, []);

  useEffect(() => {
    const beforeUnload = (event: BeforeUnloadEvent) => {
      if (task.current) { event.preventDefault(); event.returnValue = ''; }
    };
    window.addEventListener('beforeunload', beforeUnload);
    return () => window.removeEventListener('beforeunload', beforeUnload);
  }, []);

  const busy = submitting || ['uploading', 'authorizing', 'transferring', 'verifying', 'processing', 'saving', 'cancelling'].includes(logoUploadState);
  const cancelUpload = async () => {
    if (submitting) return false;
    epoch.current++; setLogoUploadState('cancelling');
    try {
      await task.current?.cancel(); task.current = null; fileRef.current = undefined;
      setLogoKey(brand?.logo_object_key ?? null); setLogoUrl(brand?.logo_url ?? null);
      setLogoUploadState('cancelled'); setLogoUploadError(null); setWarning(undefined);
      return true;
    } catch {
      setLogoUploadState('failed'); setLogoUploadError('取消未成功，请重试取消'); setRetryable(false);
      return false;
    }
  };
  const close = () => { if (submitting) return; if (task.current || busy) setLeavePrompt(true); else onClose(); };
  const handleLogoChange = async (file: File | undefined, retry = false) => {
    if (!file || busy) return;
    if (!retry && task.current && !await cancelUpload()) return;
    const token = ++epoch.current;
    fileRef.current = file;
    setError(null); setLogoUploadError(null); setWarning(undefined); setRetryable(true);
    setLogoUploadState('uploading'); setLogoUploadProgress(0);
    try {
      const result = await uploadBrandLogo(file, progress => {
        if (token === epoch.current) {
          setLogoUploadProgress(progress);
          if (progress > 0) setLogoUploadState(value => value === 'uploading' ? 'transferring' : value);
        }
      }, {
        brandId: mode === 'edit' ? brand?.id : undefined,
        task: retry ? task.current ?? undefined : undefined,
        onTask: value => { task.current = value; },
        onUpdate: value => {
          if (token !== epoch.current) return;
          setLogoUploadState(value.stage); setRetryable(value.retryable ?? false);
          setLogoUploadError(value.error ?? null); setWarning(value.warning);
        },
      });
      if (token !== epoch.current) return;
      setLogoKey(result.object_key); setLogoUrl(result.thumbnail_url ?? result.url);
      setLogoUploadProgress(100); setLogoUploadState('uploaded');
    } catch (err) {
      if (token !== epoch.current) return;
      setLogoUploadState('failed'); setLogoUploadError(getErrorMessage(err, 'Logo 上传失败'));
    }
  };

  if (!open) return null;

  const handleSubmit = async () => {
    if (busy || logoUploadState === 'failed') {
      setError('Logo 上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);
    const sort = Number.parseInt(sortOrder, 10);
    if (!name.trim()) {
      setError('品牌名称不能为空');
      setSubmitting(false);
      return;
    }
    if (!Number.isFinite(sort) || sort < 1) {
      setError('品牌排序必须为正整数');
      setSubmitting(false);
      return;
    }

    const payload = {
      name: name.trim(),
      sort_order: sort,
      short_name: shortName.trim() || null,
      english_name: englishName.trim() || null,
      logo_object_key: logoKey,
      description: description.trim() || null,
    };

    try {
      if (mode === 'create') {
        await createBrand(payload);
        onSuccess('品牌已创建');
      } else if (brand) {
        await updateBrand(brand.id, payload);
        onSuccess('品牌已更新');
      }
      task.current?.markSaved?.();
      task.current = null; fileRef.current = undefined;
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const isLogoUploading = busy;

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        className="brand-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="brand-form-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <div>
            <span id="brand-form-title" className="modal-title">
              {mode === 'create' ? '新增品牌' : '编辑品牌'}
            </span>
            <p className="modal-desc">维护品牌基础资料、展示排序、Logo 与品牌介绍。</p>
          </div>
          <button type="button" className="modal-close" aria-label="关闭" onClick={close}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <div className="brand-form-grid">
            <div className="brand-form-item">
              <label htmlFor="brand-name">
                品牌名称 <span className="req">*</span>
              </label>
              <input
                id="brand-name"
                className="input"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label htmlFor="brand-sort">
                品牌排序 <span className="req">*</span>
              </label>
              <input
                id="brand-sort"
                className="input"
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
              />
              <p className="form-help">请输入正整数</p>
            </div>
            <div className="brand-form-item">
              <label htmlFor="brand-short">品牌简称</label>
              <input
                id="brand-short"
                className="input"
                value={shortName}
                onChange={(e) => setShortName(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label htmlFor="brand-en">英文名称</label>
              <input
                id="brand-en"
                className="input"
                value={englishName}
                onChange={(e) => setEnglishName(e.target.value)}
              />
            </div>
            <div className="brand-form-item brand-form-full">
              <span className="field-label">Logo</span>
              <div className="avatar-upload brand-logo-upload">
                <div className="brand-logo-meta">
                  <span className="brand-logo-preview">
                    {logoUrl ? (
                      <AuthorizedImage file={logoUploadState === 'failed' ? undefined : fileRef.current} reference={logoUploadState !== 'failed' && task.current?.sessionId ? {resource_type: 'upload_session', resource_id: task.current.sessionId, variant: 'display'} : brand && logoKey === brand.logo_object_key ? {resource_type: 'brand_logo', resource_id: String(brand.id), variant: 'display'} : undefined}
                        src={logoUrl}
                        alt=""
                        onError={(event) => {
                          event.currentTarget
                            .closest('.brand-logo-preview')
                            ?.classList.add('is-fallback');
                        }}
                        onLoad={(event) => {
                          event.currentTarget
                            .closest('.brand-logo-preview')
                            ?.classList.remove('is-fallback');
                        }}
                      />
                    ) : null}
                    <span className="brand-logo-fallback">LOGO</span>
                  </span>
                  <span>
                    <span className="user-sub">支持 JPG / PNG / WebP，建议 1:1 方形图</span>

                  </span>
                </div>
                <label
                  className={`btn${isLogoUploading ? ' disabled' : ''}`}
                  aria-disabled={isLogoUploading}
                >
                  {isLogoUploading ? '上传中' : logoUrl ? '更换 Logo' : '选择 Logo'}
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    disabled={isLogoUploading}
                    hidden
                    onChange={(e) => {
                      const input = e.currentTarget;
                      void handleLogoChange(input.files?.[0]).finally(() => {
                        input.value = '';
                      });
                    }}
                  />
                </label>
              </div>
              <MediaUploadStatus mediaKind="image" stage={logoUploadState === 'uploading' ? 'authorizing' : logoUploadState}
                progress={logoUploadProgress} fileName={fileRef.current?.name} error={logoUploadError}
                onCancel={() => void cancelUpload()}
                onRetry={retryable ? () => void handleLogoChange(fileRef.current, true) : undefined} />
              {warning ? <p className="text-brand-gold">{warning}</p> : null}
            </div>
            <div className="brand-form-item brand-form-full">
              <label htmlFor="brand-desc">品牌介绍</label>
              <textarea
                id="brand-desc"
                className="brand-textarea"
                maxLength={500}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              <p className="form-help">
                {description.length} / 500
              </p>
            </div>
          </div>
          {error ? <p className="form-error">{error}</p> : null}
        </div>
        {leavePrompt ? <div role="alertdialog" aria-label="离开上传" className="modal-body">
          <p>离开将取消未保存的 Logo 上传。</p>
          <button type="button" className="btn" onClick={() => setLeavePrompt(false)}>继续编辑</button>
          <button type="button" className="btn" disabled={logoUploadState === 'cancelling'}
            onClick={() => void cancelUpload().then(ok => { if (ok) onClose(); })}>取消上传并离开</button>
        </div> : null}
        <div className="modal-footer">
          <button type="button" className="btn" onClick={close} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={() => void handleSubmit()}
            disabled={submitting || isLogoUploading || logoUploadState === 'failed'}
          >
            保存品牌
          </button>
        </div>
      </div>
    </div>
  );
}
