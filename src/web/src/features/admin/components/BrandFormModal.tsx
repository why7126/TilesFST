import { useEffect, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BrandAdminItem } from '@/shared/api/generated';

import { createBrand, updateBrand, uploadBrandLogo } from '../api/brands-api';

type LogoUploadState = 'idle' | 'uploading' | 'uploaded' | 'failed';

interface BrandFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  brand: BrandAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function BrandFormModal({ open, mode, brand, onClose, onSuccess }: BrandFormModalProps) {
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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
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

  if (!open) return null;

  const handleLogoChange = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setLogoUploadError(null);
    setLogoUploadState('uploading');
    setLogoUploadProgress(8);
    try {
      const result = await uploadBrandLogo(file, (progress) => {
        setLogoUploadProgress(progress);
      });
      setLogoKey(result.object_key);
      setLogoUrl(result.url);
      setLogoUploadProgress(100);
      setLogoUploadState('uploaded');
    } catch (err) {
      const message = getErrorMessage(err, 'Logo 上传失败');
      setLogoUploadState('failed');
      setLogoUploadProgress(0);
      setLogoUploadError(message);
      setError(message);
    }
  };

  const handleSubmit = async () => {
    if (logoUploadState === 'uploading') {
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
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const isLogoUploading = logoUploadState === 'uploading';

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
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
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
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
              <span className="field-label">品牌Logo</span>
              <div className="avatar-upload brand-logo-upload">
                <div className="brand-logo-meta">
                  <span className="brand-logo-preview">
                    {logoUrl ? (
                      <img
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
                    <span className="user-main">
                      {logoUrl ? '已上传 Logo' : '品牌 Logo'}
                    </span>
                    <span className="user-sub">支持 JPG / PNG / WebP，建议 1:1 方形图</span>
                    {isLogoUploading ? (
                      <span className="brand-logo-status">
                        <span
                          className="brand-logo-progress"
                          role="progressbar"
                          aria-valuemin={0}
                          aria-valuemax={100}
                          aria-valuenow={logoUploadProgress}
                        >
                          <span
                            className="brand-logo-progress-bar"
                            style={{ width: `${logoUploadProgress}%` }}
                          />
                        </span>
                        <span className="brand-logo-progress-text">
                          上传中 {logoUploadProgress}%
                        </span>
                      </span>
                    ) : null}
                    {logoUploadState === 'uploaded' ? (
                      <span className="brand-logo-upload-success">Logo 已更新</span>
                    ) : null}
                    {logoUploadState === 'failed' && logoUploadError ? (
                      <span className="brand-logo-upload-error" role="alert">
                        {logoUploadError}
                      </span>
                    ) : null}
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
        <div className="modal-footer">
          <button type="button" className="btn" onClick={onClose} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={() => void handleSubmit()}
            disabled={submitting || isLogoUploading}
          >
            保存品牌
          </button>
        </div>
      </div>
    </div>
  );
}
