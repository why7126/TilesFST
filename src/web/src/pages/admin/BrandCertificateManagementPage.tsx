import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import { useAuthStore } from '@/features/auth/store/auth-store';
import {
  createBrandCertificate,
  deleteBrandCertificate,
  fetchBrandCertificates,
  hideBrandCertificate,
  showBrandCertificate,
  updateBrandCertificate,
  uploadBrandCertificateFile,
} from '@/features/admin/api/brand-certificates-api';
import { fetchBrands } from '@/features/admin/api/brands-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import {
  CERTIFICATE_DISPLAY_OPTIONS,
  CERTIFICATE_TYPE_OPTIONS,
  CERTIFICATE_VALIDITY_OPTIONS,
  certificateTypeLabel,
  displayStatusLabel,
  formatCertificateDateTime,
  formatValidityRange,
  isPdfCertificate,
  validityBadgeClass,
  validityStatusLabel,
} from '@/features/admin/lib/brand-certificate-display';
import { AdminListPage } from '@/shared/templates';
import { cn } from '@/shared/lib/cn';
import type {
  BrandAdminItem,
  BrandCertificateCreateRequest,
  BrandCertificateFile,
  BrandCertificateItem,
  BrandCertificateListData,
} from '@/shared/api/generated';

import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/brand-management.css';
import '@/features/admin/styles/brand-certificate-management.css';

type UploadState = 'idle' | 'uploading' | 'done' | 'failed';
type ConfirmAction = 'show' | 'hide' | 'delete';

interface CertificateFormState {
  brandId: string;
  name: string;
  sortOrder: string;
  type: string;
  certificateNo: string;
  issuer: string;
  file: BrandCertificateFile | null;
  isPermanent: boolean;
  effectiveDate: string;
  expiryDate: string;
  isVisible: boolean;
  remark: string;
}

interface CertificateFormErrors {
  brandId?: string;
  name?: string;
  sortOrder?: string;
  type?: string;
  file?: string;
  expiryDate?: string;
}

const emptyForm: CertificateFormState = {
  brandId: '',
  name: '',
  sortOrder: '10',
  type: 'QUALITY',
  certificateNo: '',
  issuer: '',
  file: null,
  isPermanent: false,
  effectiveDate: '',
  expiryDate: '',
  isVisible: true,
  remark: '',
};

function toForm(item: BrandCertificateItem | null): CertificateFormState {
  if (!item) return emptyForm;
  return {
    brandId: String(item.brand_id),
    name: item.name,
    sortOrder: String(item.sort_order),
    type: item.type,
    certificateNo: item.certificate_no ?? '',
    issuer: item.issuer ?? '',
    file: {
      file_url: item.file_url,
      file_key: item.file_key,
      file_name: item.file_name,
      file_mime_type: item.file_mime_type,
      file_size_bytes: item.file_size_bytes,
    },
    isPermanent: item.is_permanent,
    effectiveDate: item.effective_date ?? '',
    expiryDate: item.expiry_date ?? '',
    isVisible: item.is_visible,
    remark: item.remark ?? '',
  };
}

function fileToRequest(file: BrandCertificateFile): BrandCertificateFile {
  return {
    file_url: file.file_url,
    file_key: file.file_key,
    file_name: file.file_name,
    file_mime_type: file.file_mime_type,
    file_size_bytes: file.file_size_bytes,
  };
}

function validateForm(form: CertificateFormState): {
  payload: BrandCertificateCreateRequest | null;
  errors: CertificateFormErrors;
} {
  const brandId = Number.parseInt(form.brandId, 10);
  const sortOrder = Number.parseInt(form.sortOrder, 10);
  const errors: CertificateFormErrors = {};

  if (!Number.isFinite(brandId) || brandId < 1) errors.brandId = '请选择所属品牌';
  if (!form.name.trim()) errors.name = '证书名称不能为空';
  if (!Number.isFinite(sortOrder) || sortOrder < 1) {
    errors.sortOrder = '证书排序必须为正整数';
  }
  if (!form.type) errors.type = '请选择证书类型';
  if (!form.file) errors.file = '请先上传证书文件';
  if (!form.isPermanent && !form.expiryDate) {
    errors.expiryDate = '非长期有效证书必须填写到期日期';
  }
  if (!form.isPermanent && form.effectiveDate && form.expiryDate < form.effectiveDate) {
    errors.expiryDate = '到期日期不能早于生效日期';
  }

  if (Object.keys(errors).length > 0) {
    return { payload: null, errors };
  }

  return {
    payload: {
      brand_id: brandId,
      name: form.name.trim(),
      sort_order: sortOrder,
      type: form.type as BrandCertificateCreateRequest['type'],
      certificate_no: form.certificateNo.trim() || null,
      issuer: form.issuer.trim() || null,
      file: fileToRequest(form.file!),
      is_permanent: form.isPermanent,
      effective_date: form.isPermanent ? null : form.effectiveDate || null,
      expiry_date: form.isPermanent ? null : form.expiryDate || null,
      is_visible: form.isVisible,
      remark: form.remark.trim() || null,
    },
    errors,
  };
}

function CertificateFormModal({
  open,
  mode,
  certificate,
  brands,
  initialBrandId,
  onClose,
  onSuccess,
}: {
  open: boolean;
  mode: 'create' | 'edit';
  certificate: BrandCertificateItem | null;
  brands: BrandAdminItem[];
  initialBrandId: string;
  onClose: () => void;
  onSuccess: (message: string) => void;
}) {
  const [form, setForm] = useState<CertificateFormState>(emptyForm);
  const [uploadState, setUploadState] = useState<UploadState>('idle');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<CertificateFormErrors>({});

  useEffect(() => {
    if (!open) return;
    const nextForm = toForm(certificate);
    setForm({
      ...nextForm,
      brandId: nextForm.brandId || initialBrandId || '',
    });
    setUploadState(certificate?.file_url ? 'done' : 'idle');
    setUploadProgress(0);
    setUploadError(null);
    setError(null);
    setFieldErrors({});
    setSubmitting(false);
  }, [open, certificate, initialBrandId]);

  if (!open) return null;

  const updateForm = (patch: Partial<CertificateFormState>) => {
    setForm((current) => ({ ...current, ...patch }));
    setFieldErrors((current) => {
      const next = { ...current };
      for (const key of Object.keys(patch) as Array<keyof CertificateFormState>) {
        if (key === 'brandId') delete next.brandId;
        if (key === 'name') delete next.name;
        if (key === 'sortOrder') delete next.sortOrder;
        if (key === 'type') delete next.type;
        if (key === 'file') delete next.file;
        if (key === 'expiryDate' || key === 'effectiveDate' || key === 'isPermanent') {
          delete next.expiryDate;
        }
      }
      return next;
    });
  };

  const handleFileChange = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setFieldErrors((current) => ({ ...current, file: undefined }));
    setUploadError(null);
    setUploadState('uploading');
    setUploadProgress(8);
    try {
      const result = await uploadBrandCertificateFile(file, setUploadProgress);
      updateForm({
        file: {
          file_url: result.file_url ?? result.url,
          file_key: result.file_key ?? result.object_key,
          file_name: result.file_name ?? file.name,
          file_mime_type: result.mime_type ?? file.type,
          file_size_bytes: result.size ?? file.size,
        },
      });
      setUploadProgress(100);
      setUploadState('done');
    } catch (err) {
      const message = getErrorMessage(err, '证书文件上传失败');
      setUploadState('failed');
      setUploadProgress(0);
      setUploadError(message);
      setFieldErrors((current) => ({ ...current, file: message }));
    }
  };

  const handleSubmit = async () => {
    if (uploadState === 'uploading') {
      setError(null);
      setFieldErrors((current) => ({ ...current, file: '证书文件上传中，请稍后保存' }));
      return;
    }
    const { payload, errors } = validateForm(form);
    setFieldErrors(errors);
    setError(null);
    if (!payload) {
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      if (mode === 'create') {
        await createBrandCertificate(payload);
        onSuccess('证书已创建');
      } else if (certificate) {
        await updateBrandCertificate(certificate.id, payload);
        onSuccess('证书已更新');
      }
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存证书失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const file = form.file;
  const isUploading = uploadState === 'uploading';

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="certificate-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="certificate-form-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-head">
          <div>
            <span id="certificate-form-title" className="modal-title">
              {mode === 'create' ? '新增证书' : '编辑证书'}
            </span>
            <p className="modal-desc">维护证书文件、有效期、展示状态与品牌归属。</p>
          </div>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body certificate-modal-body">
          <div className="certificate-form-grid">
            <div className="brand-form-item">
              <label htmlFor="certificate-brand">
                所属品牌 <span className="req">*</span>
              </label>
              <select
                id="certificate-brand"
                className="select"
                aria-invalid={Boolean(fieldErrors.brandId)}
                value={form.brandId}
                onChange={(event) => updateForm({ brandId: event.target.value })}
              >
                <option value="">请选择品牌</option>
                {brands.map((brand) => (
                  <option key={brand.id} value={brand.id}>
                    {brand.name}
                  </option>
                ))}
              </select>
              {fieldErrors.brandId ? (
                <p className="field-error" role="alert">
                  {fieldErrors.brandId}
                </p>
              ) : null}
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-type">
                证书类型 <span className="req">*</span>
              </label>
              <select
                id="certificate-type"
                className="select"
                aria-invalid={Boolean(fieldErrors.type)}
                value={form.type}
                onChange={(event) => updateForm({ type: event.target.value })}
              >
                {CERTIFICATE_TYPE_OPTIONS.filter((item) => item.value).map((item) => (
                  <option key={item.value} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
              {fieldErrors.type ? (
                <p className="field-error" role="alert">
                  {fieldErrors.type}
                </p>
              ) : null}
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-name">
                证书名称 <span className="req">*</span>
              </label>
              <input
                id="certificate-name"
                className="input"
                aria-invalid={Boolean(fieldErrors.name)}
                value={form.name}
                onChange={(event) => updateForm({ name: event.target.value })}
              />
              {fieldErrors.name ? (
                <p className="field-error" role="alert">
                  {fieldErrors.name}
                </p>
              ) : null}
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-sort">
                证书排序 <span className="req">*</span>
              </label>
              <input
                id="certificate-sort"
                className="input"
                aria-invalid={Boolean(fieldErrors.sortOrder)}
                value={form.sortOrder}
                onChange={(event) => updateForm({ sortOrder: event.target.value })}
              />
              {fieldErrors.sortOrder ? (
                <p className="field-error" role="alert">
                  {fieldErrors.sortOrder}
                </p>
              ) : null}
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-no">证书编号</label>
              <input
                id="certificate-no"
                className="input"
                value={form.certificateNo}
                onChange={(event) => updateForm({ certificateNo: event.target.value })}
              />
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-issuer">发证机构</label>
              <input
                id="certificate-issuer"
                className="input"
                value={form.issuer}
                onChange={(event) => updateForm({ issuer: event.target.value })}
              />
            </div>

            <div className="brand-form-item brand-form-full">
              <span className="field-label">
                证书文件 <span className="req">*</span>
              </span>
              <div className={cn('certificate-upload', uploadState === 'failed' && 'is-failed')}>
                <div className="certificate-file-card">
                  <span className={cn('certificate-file-thumb', file && 'has-file')}>
                    {file && file.file_mime_type !== 'application/pdf' ? (
                      <img src={file.file_url} alt="" />
                    ) : (
                      <span>{file?.file_mime_type === 'application/pdf' ? 'PDF' : 'FILE'}</span>
                    )}
                  </span>
                  <span className="certificate-file-meta">
                    <span className="user-main">{file ? file.file_name : '未上传证书文件'}</span>
                    <span className="user-sub">支持 JPG / PNG / WebP / PDF，单文件最大 20MB</span>
                    {isUploading ? (
                      <span className="brand-logo-status">
                        <span
                          className="brand-logo-progress"
                          role="progressbar"
                          aria-valuemin={0}
                          aria-valuemax={100}
                          aria-valuenow={uploadProgress}
                        >
                          <span
                            className="brand-logo-progress-bar"
                            style={{ width: `${uploadProgress}%` }}
                          />
                        </span>
                        <span className="brand-logo-progress-text">上传中 {uploadProgress}%</span>
                      </span>
                    ) : null}
                    {uploadState === 'done' && file ? (
                      <span className="brand-logo-upload-success">证书文件已就绪</span>
                    ) : null}
                    {uploadState === 'failed' && uploadError ? (
                      <span className="brand-logo-upload-error" role="alert">
                        {uploadError}
                      </span>
                    ) : null}
                  </span>
                </div>
                <div className="certificate-upload-actions">
                  {file ? (
                    <button type="button" className="btn" onClick={() => updateForm({ file: null })}>
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
                      onChange={(event) => {
                        const input = event.currentTarget;
                        void handleFileChange(input.files?.[0]).finally(() => {
                          input.value = '';
                        });
                      }}
                    />
                  </label>
                </div>
              </div>
              {fieldErrors.file ? (
                <p className="field-error" role="alert">
                  {fieldErrors.file}
                </p>
              ) : null}
            </div>

            <label className="certificate-check">
              <input
                type="checkbox"
                checked={form.isPermanent}
                onChange={(event) => {
                  updateForm({
                    isPermanent: event.target.checked,
                    effectiveDate: event.target.checked ? '' : form.effectiveDate,
                    expiryDate: event.target.checked ? '' : form.expiryDate,
                  });
                }}
              />
              长期有效
            </label>
            <label className="certificate-check">
              <input
                type="checkbox"
                checked={form.isVisible}
                onChange={(event) => updateForm({ isVisible: event.target.checked })}
              />
              前台展示
            </label>
            <div className="brand-form-item">
              <label htmlFor="certificate-effective">生效日期</label>
              <input
                id="certificate-effective"
                className="input"
                type="date"
                value={form.effectiveDate}
                disabled={form.isPermanent}
                onChange={(event) => updateForm({ effectiveDate: event.target.value })}
              />
            </div>
            <div className="brand-form-item">
              <label htmlFor="certificate-expiry">
                到期日期 {!form.isPermanent ? <span className="req">*</span> : null}
              </label>
              <input
                id="certificate-expiry"
                className="input"
                type="date"
                aria-invalid={Boolean(fieldErrors.expiryDate)}
                value={form.expiryDate}
                disabled={form.isPermanent}
                onChange={(event) => updateForm({ expiryDate: event.target.value })}
              />
              {fieldErrors.expiryDate ? (
                <p className="field-error" role="alert">
                  {fieldErrors.expiryDate}
                </p>
              ) : null}
            </div>
            <div className="brand-form-item brand-form-full">
              <label htmlFor="certificate-remark">备注</label>
              <textarea
                id="certificate-remark"
                className="brand-textarea certificate-remark"
                maxLength={500}
                value={form.remark}
                onChange={(event) => updateForm({ remark: event.target.value })}
              />
              <p className="form-help">{form.remark.length} / 500</p>
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
            disabled={submitting || isUploading}
            onClick={() => void handleSubmit()}
          >
            保存证书
          </button>
        </div>
      </div>
    </div>
  );
}

function CertificateConfirmDialog({
  action,
  target,
  onCancel,
  onConfirm,
}: {
  action: ConfirmAction;
  target: BrandCertificateItem;
  onCancel: () => void;
  onConfirm: () => void;
}) {
  const title = action === 'delete' ? '删除证书' : action === 'show' ? '显示证书' : '隐藏证书';
  const confirmLabel = action === 'delete' ? '删除证书' : action === 'show' ? '确认显示' : '确认隐藏';
  return (
    <div className="modal-backdrop" role="presentation" onClick={onCancel}>
      <div
        className="modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="certificate-confirm-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-head">
          <span id="certificate-confirm-title" className="modal-title">
            {title}
          </span>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onCancel}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <p className="page-desc">
            {action === 'delete'
              ? `确认删除证书「${target.name}」？删除后不再进入店主端展示数据。`
              : action === 'show'
                ? `确认显示证书「${target.name}」？`
                : `确认隐藏证书「${target.name}」？隐藏后前台不再展示。`}
          </p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn" onClick={onCancel}>
            取消
          </button>
          <button type="button" className="btn primary" onClick={onConfirm}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

export function BrandCertificateManagementPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const user = useAuthStore((state) => state.user);
  const canMutate = user?.role === 'admin';

  const [keywordInput, setKeywordInput] = useState(searchParams.get('keyword') ?? '');
  const [keyword, setKeyword] = useState(searchParams.get('keyword') ?? '');
  const [brandId, setBrandId] = useState(searchParams.get('brand_id') ?? '');
  const [type, setType] = useState(searchParams.get('type') ?? '');
  const [validityStatus, setValidityStatus] = useState(searchParams.get('validity_status') ?? '');
  const [displayStatus, setDisplayStatus] = useState(searchParams.get('display_status') ?? '');
  const [page, setPage] = useState(Number(searchParams.get('page') ?? '1') || 1);
  const [pageSize, setPageSize] = useState(Number(searchParams.get('page_size') ?? '20') || 20);
  const [data, setData] = useState<BrandCertificateListData | null>(null);
  const [brands, setBrands] = useState<BrandAdminItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingCertificate, setEditingCertificate] = useState<BrandCertificateItem | null>(null);
  const [confirmTarget, setConfirmTarget] = useState<{
    action: ConfirmAction;
    item: BrandCertificateItem;
  } | null>(null);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setKeyword(keywordInput.trim());
      setPage(1);
    }, 300);
    return () => window.clearTimeout(timer);
  }, [keywordInput]);

  useEffect(() => {
    const next = new URLSearchParams();
    if (keyword) next.set('keyword', keyword);
    if (brandId) next.set('brand_id', brandId);
    if (type) next.set('type', type);
    if (validityStatus) next.set('validity_status', validityStatus);
    if (displayStatus) next.set('display_status', displayStatus);
    if (page > 1) next.set('page', String(page));
    if (pageSize !== 20) next.set('page_size', String(pageSize));
    setSearchParams(next, { replace: true });
  }, [keyword, brandId, type, validityStatus, displayStatus, page, pageSize, setSearchParams]);

  const loadCertificates = useCallback(async () => {
    setLoading(true);
    try {
      const result = await fetchBrandCertificates({
        page,
        page_size: pageSize,
        keyword: keyword || undefined,
        brand_id: brandId ? Number(brandId) : undefined,
        type: type || undefined,
        validity_status: validityStatus || undefined,
        display_status: displayStatus || undefined,
      });
      setData(result);
    } catch (err) {
      setNotice(getErrorMessage(err, '加载品牌证书失败'));
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, keyword, brandId, type, validityStatus, displayStatus]);

  useEffect(() => {
    void loadCertificates();
  }, [loadCertificates]);

  useEffect(() => {
    void fetchBrands({ page: 1, page_size: 100 }).then((result) => setBrands(result.items));
  }, []);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const resetFilters = () => {
    setKeywordInput('');
    setKeyword('');
    setBrandId('');
    setType('');
    setValidityStatus('');
    setDisplayStatus('');
    setPage(1);
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingCertificate(null);
    setFormOpen(true);
  };

  const openEdit = (item: BrandCertificateItem) => {
    setFormMode('edit');
    setEditingCertificate(item);
    setFormOpen(true);
  };

  const handleConfirm = async () => {
    if (!confirmTarget) return;
    try {
      if (confirmTarget.action === 'show') {
        await showBrandCertificate(confirmTarget.item.id);
        setNotice('证书已显示');
      } else if (confirmTarget.action === 'hide') {
        await hideBrandCertificate(confirmTarget.item.id);
        setNotice('证书已隐藏');
      } else {
        await deleteBrandCertificate(confirmTarget.item.id);
        setNotice('证书已删除');
      }
      setConfirmTarget(null);
      void loadCertificates();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const rows = data?.items ?? [];
  const selectedBrandName = useMemo(
    () => brands.find((brand) => String(brand.id) === brandId)?.name,
    [brands, brandId],
  );

  return (
    <AdminListPage
      className="brand-certificate-page"
      content={{
        eyebrow: 'MASTER DATA',
        title: '品牌证书',
        description: selectedBrandName
          ? `当前筛选品牌：${selectedBrandName}`
          : '维护品牌质量体系、检测报告、绿色建材与荣誉资质证书。',
        primaryActionLabel: '＋ 新增证书',
        metrics: [
          {
            label: '证书总数',
            value: data?.summary.total,
            description: '全部未删除证书',
          },
          {
            label: '有效证书',
            value: data?.summary.valid_count,
            description: '长期有效或有效期内',
          },
          {
            label: '即将到期',
            value: data?.summary.expiring_soon_count,
            description: '30 天内到期',
            dangerDescription: (data?.summary.expiring_soon_count ?? 0) > 0,
          },
          {
            label: '已过期',
            value: data?.summary.expired_count,
            description: '需要复核更新',
            dangerDescription: (data?.summary.expired_count ?? 0) > 0,
          },
        ].map((metric, index) => ({
          ...metric,
          description:
            index === 1 ? (
              <button
                type="button"
                className="metric-filter-link"
                onClick={() => {
                  setValidityStatus('VALID');
                  setPage(1);
                }}
              >
                {metric.description}
              </button>
            ) : index === 2 ? (
              <button
                type="button"
                className="metric-filter-link"
                onClick={() => {
                  setValidityStatus('EXPIRING_SOON');
                  setPage(1);
                }}
              >
                {metric.description}
              </button>
            ) : index === 3 ? (
              <button
                type="button"
                className="metric-filter-link"
                onClick={() => {
                  setValidityStatus('EXPIRED');
                  setPage(1);
                }}
              >
                {metric.description}
              </button>
            ) : (
              metric.description
            ),
        })),
        filters: [
          {
            id: 'certificate-filter-keyword',
            label: '关键词',
            control: (
              <input
                id="certificate-filter-keyword"
                className="input"
                placeholder="搜索证书名称 / 编号 / 发证机构"
                value={keywordInput}
                onChange={(event) => setKeywordInput(event.target.value)}
              />
            ),
          },
          {
            id: 'certificate-filter-brand',
            label: '所属品牌',
            control: (
              <select
                id="certificate-filter-brand"
                className="select"
                value={brandId}
                onChange={(event) => {
                  setBrandId(event.target.value);
                  setPage(1);
                }}
              >
                <option value="">全部品牌</option>
                {brands.map((brand) => (
                  <option key={brand.id} value={brand.id}>
                    {brand.name}
                  </option>
                ))}
              </select>
            ),
          },
          {
            id: 'certificate-filter-type',
            label: '证书类型',
            control: (
              <select
                id="certificate-filter-type"
                className="select"
                value={type}
                onChange={(event) => {
                  setType(event.target.value);
                  setPage(1);
                }}
              >
                {CERTIFICATE_TYPE_OPTIONS.map((option) => (
                  <option key={option.label} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ),
          },
          {
            id: 'certificate-filter-validity',
            label: '有效状态',
            control: (
              <select
                id="certificate-filter-validity"
                className="select"
                value={validityStatus}
                onChange={(event) => {
                  setValidityStatus(event.target.value);
                  setPage(1);
                }}
              >
                {CERTIFICATE_VALIDITY_OPTIONS.map((option) => (
                  <option key={option.label} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ),
          },
          {
            id: 'certificate-filter-display',
            label: '展示状态',
            control: (
              <select
                id="certificate-filter-display"
                className="select"
                value={displayStatus}
                onChange={(event) => {
                  setDisplayStatus(event.target.value);
                  setPage(1);
                }}
              >
                {CERTIFICATE_DISPLAY_OPTIONS.map((option) => (
                  <option key={option.label} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ),
          },
        ],
        columns: [
          {
            key: 'certificate',
            header: '证书',
            render: (item) => (
              <div className="certificate-cell">
                <span className="certificate-thumb">
                  {isPdfCertificate(item) ? (
                    'PDF'
                  ) : (
                    <img
                      src={item.file_url}
                      alt=""
                      onError={(event) => {
                        event.currentTarget.closest('.certificate-thumb')?.classList.add('is-fallback');
                      }}
                    />
                  )}
                  <span className="certificate-thumb-fallback">FILE</span>
                </span>
                <span>
                  <span className="brand-name">{item.name}</span>
                  <span className="brand-sub">{item.certificate_no || item.file_name}</span>
                </span>
              </div>
            ),
          },
          { key: 'brand_name', header: '所属品牌' },
          { key: 'type', header: '证书类型', render: (item) => certificateTypeLabel(item.type) },
          { key: 'issuer', header: '发证机构', render: (item) => item.issuer || '—' },
          { key: 'validity', header: '有效期', render: (item) => formatValidityRange(item) },
          {
            key: 'validity_status',
            header: '有效状态',
            render: (item) => (
              <span className={validityBadgeClass(item.validity_status)}>
                {validityStatusLabel(item.validity_status)}
              </span>
            ),
          },
          {
            key: 'display_status',
            header: '前台展示',
            render: (item) => (
              <span className={item.is_visible ? 'badge enabled' : 'badge disabled'}>
                {displayStatusLabel(item)}
              </span>
            ),
          },
          { key: 'sort_order', header: '排序', className: 'sort-num' },
          {
            key: 'updated_at',
            header: '更新时间',
            render: (item) => formatCertificateDateTime(item.updated_at),
          },
          {
            key: 'actions',
            header: '操作',
            stickyAction: true,
            render: (item) => (
              <div className="brand-actions">
                <button
                  type="button"
                  className="link-btn"
                  onClick={() => {
                    const url = item.file_url;
                    if (isPdfCertificate(item)) {
                      window.open(url, '_blank', 'noopener,noreferrer');
                    } else {
                      window.open(url, '_blank', 'noopener,noreferrer');
                    }
                  }}
                >
                  预览
                </button>
                {canMutate ? (
                  <>
                    <button type="button" className="link-btn" onClick={() => openEdit(item)}>
                      编辑
                    </button>
                    <button
                      type="button"
                      className="link-btn muted"
                      onClick={() =>
                        setConfirmTarget({ action: item.is_visible ? 'hide' : 'show', item })
                      }
                    >
                      {item.is_visible ? '隐藏' : '显示'}
                    </button>
                    <button
                      type="button"
                      className="link-btn danger"
                      onClick={() => setConfirmTarget({ action: 'delete', item })}
                    >
                      删除
                    </button>
                  </>
                ) : null}
              </div>
            ),
          },
        ],
        rows,
        pagination: {
          page,
          total: data?.total ?? 0,
          pageSize,
          itemLabel: '证书',
        },
        state: {
          emptyText: keyword || brandId || type || validityStatus || displayStatus
            ? '没有符合筛选条件的证书'
            : '暂无品牌证书数据',
          loadingText: '证书数据加载中…',
        },
      }}
      onCreate={canMutate ? openCreate : undefined}
      onReset={resetFilters}
      onPageChange={setPage}
      onPageSizeChange={(nextPageSize) => {
        setPageSize(nextPageSize);
        setPage(1);
      }}
      loading={loading}
      tableClassName="brand-mgmt-table certificate-mgmt-table"
      feedback={<AdminToast message={notice} />}
      confirmDialog={
        <>
          <CertificateFormModal
            open={formOpen}
            mode={formMode}
            certificate={editingCertificate}
            brands={brands}
            initialBrandId={brandId}
            onClose={() => setFormOpen(false)}
            onSuccess={(message) => {
              setNotice(message);
              void loadCertificates();
            }}
          />
          {confirmTarget ? (
            <CertificateConfirmDialog
              action={confirmTarget.action}
              target={confirmTarget.item}
              onCancel={() => setConfirmTarget(null)}
              onConfirm={() => void handleConfirm()}
            />
          ) : null}
        </>
      }
    />
  );
}
