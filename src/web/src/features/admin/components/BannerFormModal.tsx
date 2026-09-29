import { useModalReturnFocus } from './use-modal-return-focus';
import { AuthorizedImage } from '@/features/media/authorized-media';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type {
  BannerAdminItem,
  BannerCreateRequest,
  BannerCreateRequestDisplayClient,
  BannerCreateRequestPosition,
} from '@/shared/api/generated';
import { SearchableSelect } from '@/shared/ui/searchable-select';

import { fetchBrands } from '../api/brands-api';
import { fetchTileSku, fetchTileSkus } from '../api/tile-skus-api';
import { createBanner, updateBanner, uploadBannerImage } from '../api/banners-api';
import { fetchTopics } from '../api/topics-api';
import {
  JUMP_TYPE_OPTIONS,
  POSITIONS_BY_CLIENT,
  clearJumpFieldsForType,
  extractSkuMainImage,
  jumpTypeModalTitle,
} from '../lib/banner-display';
import { BannerValidityField } from './BannerValidityField';

import { MediaUploadStatus, type UploadStage } from '@/features/media/media-upload-status';
import type { MediaUploadTask } from '@/features/media/media-upload-controller';
type ImageUploadState = UploadStage | 'uploading';

const MINIAPP_DISPLAY_CLIENT = 'MINIAPP_HOME' satisfies BannerCreateRequestDisplayClient;
const MINIAPP_HOME_POSITION = 'MINIAPP_HOME_CAROUSEL' satisfies BannerCreateRequestPosition;

function buildInternalBannerTitle(params: {
  mode: 'create' | 'edit';
  existingTitle: string;
  position: BannerCreateRequestPosition;
  jumpType: string;
}): string {
  const existingTitle = params.existingTitle.trim();
  if (params.mode === 'edit' && existingTitle) {
    return existingTitle;
  }
  return `internal-${params.position}-${params.jumpType}-${Date.now()}`;
}

function normalizeBannerSaveError(message: string): string {
  if (message.includes('标题')) {
    return 'Banner 内部识别信息保存失败，请稍后重试';
  }
  return message;
}

interface BannerFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  banner: BannerAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

interface SkuOption {
  id: number;
  label: string;
}

interface TopicOption {
  id: number;
  label: string;
}

interface BrandOption {
  id: number;
  label: string;
  logoObjectKey: string | null;
  logoUrl: string | null;
}

function mergeSkuOption(options: SkuOption[], next: SkuOption): SkuOption[] {
  if (options.some((item) => item.id === next.id)) {
    return options;
  }
  return [next, ...options];
}

function mergeTopicOption(options: TopicOption[], next: TopicOption): TopicOption[] {
  if (options.some((item) => item.id === next.id)) {
    return options;
  }
  return [next, ...options];
}

function mergeBrandOption(options: BrandOption[], next: BrandOption): BrandOption[] {
  if (options.some((item) => item.id === next.id)) {
    return options;
  }
  return [next, ...options];
}

export function BannerFormModal({ open, mode, banner, onClose, onSuccess }: BannerFormModalProps) {
  useModalReturnFocus(open);
  const [title, setTitle] = useState('');
  const [displayClient, setDisplayClient] = useState(MINIAPP_DISPLAY_CLIENT);
  const [position, setPosition] = useState<BannerCreateRequestPosition>(MINIAPP_HOME_POSITION);
  const [jumpType, setJumpType] = useState('NO_JUMP');
  const [skuId, setSkuId] = useState<number | null>(null);
  const [externalUrl, setExternalUrl] = useState('');
  const [topicId, setTopicId] = useState<number | null>(null);
  const [brandId, setBrandId] = useState<number | null>(null);
  const [sortOrder, setSortOrder] = useState('10');
  const [validFrom, setValidFrom] = useState('');
  const [validTo, setValidTo] = useState('');
  const [remark, setRemark] = useState('');
  const [imageKey, setImageKey] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [imageSource, setImageSource] = useState('custom_upload');
  const [skuGalleryAssetId, setSkuGalleryAssetId] = useState<number | null>(null);
  const [imageUploadState, setImageUploadState] = useState<ImageUploadState>('idle');
  const task = useRef<MediaUploadTask | null>(null);
  const uploadKey = useRef<string | null>(null);
  const fileRef = useRef<File | undefined>(undefined);
  const epoch = useRef(0);
  const [imageProgress, setImageProgress] = useState(0);
  const [imageError, setImageError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | undefined>();
  const [retryable, setRetryable] = useState(true);
  const [leavePrompt, setLeavePrompt] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const busy = submitting || ['uploading','authorizing','transferring','verifying','processing','saving','cancelling'].includes(imageUploadState);
  const [error, setError] = useState<string | null>(null);
  const [skuOptions, setSkuOptions] = useState<SkuOption[]>([]);
  const [topicOptions, setTopicOptions] = useState<TopicOption[]>([]);
  const [brandOptions, setBrandOptions] = useState<BrandOption[]>([]);

  useEffect(() => () => { epoch.current++; void task.current?.cancel().catch(() => undefined); }, []);
  useEffect(() => {
    const listener = (event: BeforeUnloadEvent) => {
      if (task.current) { event.preventDefault(); event.returnValue = ''; }
    };
    window.addEventListener('beforeunload', listener);
    return () => window.removeEventListener('beforeunload', listener);
  }, []);

  const loadSkuOptions = useCallback(async (keyword?: string) => {
    try {
      const data = await fetchTileSkus({ page: 1, page_size: 20, keyword: keyword || undefined });
      setSkuOptions(
        data.items.map((item) => ({
          id: item.id,
          label: `${item.name} · ${item.sku_code}`,
        })),
      );
    } catch {
      setSkuOptions([]);
    }
  }, []);

  const loadTopicOptions = useCallback(async (keyword?: string) => {
    try {
      const data = await fetchTopics({ keyword: keyword || undefined, status: 'ENABLED' });
      setTopicOptions(data.items.map((item) => ({ id: item.id, label: item.title })));
    } catch {
      setTopicOptions([]);
    }
  }, []);

  const loadBrandOptions = useCallback(async (keyword?: string) => {
    try {
      const data = await fetchBrands({
        page: 1,
        page_size: 20,
        keyword: keyword || undefined,
        status: 'ENABLED',
      });
      setBrandOptions(
        data.items.map((item) => ({
          id: item.id,
          label: item.short_name ? `${item.name} · ${item.short_name}` : item.name,
          logoObjectKey: item.logo_object_key ?? null,
          logoUrl: item.logo_url ?? null,
        })),
      );
    } catch {
      setBrandOptions([]);
    }
  }, []);

  const applySkuMainImage = useCallback(async (id: number) => {
    const token = epoch.current;
    try {
      const sku = await fetchTileSku(id);
      if (token !== epoch.current) return false;
      const { objectKey, url } = extractSkuMainImage(sku);
      if (!objectKey || !url) {
        setError('该 SKU 无主图，请自定义上传');
        return false;
      }
      setImageSource('sku_main_image');
      setSkuGalleryAssetId(null);
      setImageKey(objectKey);
      setImageUrl(url);
      setError(null);
      return true;
    } catch {
      setError('加载 SKU 主图失败');
      return false;
    }
  }, []);

  const applyBrandLogo = useCallback(
    (id: number) => {
      const brand = brandOptions.find((item) => item.id === id);
      if (!brand?.logoObjectKey || !brand.logoUrl) {
        setError('该品牌无 Logo，请自定义上传');
        return false;
      }
      setImageSource('brand_logo');
      setSkuGalleryAssetId(null);
      setImageKey(brand.logoObjectKey);
      setImageUrl(brand.logoUrl);
      setError(null);
      return true;
    },
    [brandOptions],
  );

  useEffect(() => {
    if (!open) return;
    setLeavePrompt(false); setWarning(undefined); setImageError(null); setImageProgress(0);
    setError(null);
    setImageUploadState('idle');
    void loadSkuOptions();
    void loadTopicOptions();
    void loadBrandOptions();

    if (mode === 'edit' && banner) {
      setTitle(banner.title);
      setDisplayClient(MINIAPP_DISPLAY_CLIENT);
      setPosition(
        POSITIONS_BY_CLIENT.MINIAPP_HOME.some((item) => item.value === banner.position)
          ? (banner.position as BannerCreateRequestPosition)
          : MINIAPP_HOME_POSITION,
      );
      setJumpType(banner.jump_type);
      setSkuId(banner.sku_id ?? null);
      setExternalUrl(banner.external_url ?? '');
      setTopicId(banner.topic_id ?? null);
      setBrandId(banner.brand_id ?? null);
      setSortOrder(String(banner.sort_order));
      setValidFrom(banner.valid_from?.slice(0, 16) ?? '');
      setValidTo(banner.valid_to?.slice(0, 16) ?? '');
      setRemark(banner.remark ?? '');
      setImageKey(banner.image_object_key);
      setImageUrl(banner.image_url);
      setImageSource(banner.image_source);
      setSkuGalleryAssetId(banner.sku_gallery_asset_id ?? null);

      if (banner.sku_id) {
        void fetchTileSku(banner.sku_id).then((sku) => {
          setSkuOptions((current) =>
            mergeSkuOption(current, {
              id: sku.id,
              label: `${sku.name} · ${sku.sku_code}`,
            }),
          );
        });
      }
      if (banner.topic_id) {
        void fetchTopics({ status: 'ENABLED' }).then((data) => {
          const topic = data.items.find((item) => item.id === banner.topic_id);
          if (topic) {
            setTopicOptions((current) =>
              mergeTopicOption(current, { id: topic.id, label: topic.title }),
            );
          } else {
            setTopicOptions((current) =>
              mergeTopicOption(current, { id: banner.topic_id!, label: `专题 #${banner.topic_id}` }),
            );
          }
        });
      }
      if (banner.brand_id) {
        void fetchBrands({ page: 1, page_size: 100, status: 'ENABLED' }).then((data) => {
          const brand = data.items.find((item) => item.id === banner.brand_id);
          if (brand) {
            setBrandOptions((current) =>
              mergeBrandOption(current, {
                id: brand.id,
                label: brand.short_name ? `${brand.name} · ${brand.short_name}` : brand.name,
                logoObjectKey: brand.logo_object_key ?? null,
                logoUrl: brand.logo_url ?? null,
              }),
            );
          } else {
            setBrandOptions((current) =>
              mergeBrandOption(current, {
                id: banner.brand_id!,
                label: `品牌 #${banner.brand_id}`,
                logoObjectKey: null,
                logoUrl: null,
              }),
            );
          }
        });
      }
    } else {
      setTitle('');
      setDisplayClient(MINIAPP_DISPLAY_CLIENT);
      setPosition(MINIAPP_HOME_POSITION);
      setJumpType('NO_JUMP');
      setSkuId(null);
      setExternalUrl('');
      setTopicId(null);
      setBrandId(null);
      setSortOrder('10');
      setValidFrom('');
      setValidTo('');
      setRemark('');
      setImageKey('');
      setImageUrl('');
      setImageSource('custom_upload');
      setSkuGalleryAssetId(null);
    }
  }, [open, mode, banner, loadSkuOptions, loadTopicOptions, loadBrandOptions]);

  const handleJumpTypeChange = (value: string) => {
    setJumpType(value);
    const cleared = clearJumpFieldsForType(value);
    setSkuId(cleared.sku_id);
    setExternalUrl(cleared.external_url ?? '');
    setTopicId(cleared.topic_id);
    setBrandId(cleared.brand_id);
    setSkuGalleryAssetId(cleared.sku_gallery_asset_id);
    setImageSource(cleared.image_source);
    if (value !== 'SKU_DETAIL' && value !== 'BRAND_DETAIL') {
      setImageKey('');
      setImageUrl('');
    }
  };

  const handleSkuSelect = async (value: string | null) => {
    const id = value ? Number.parseInt(value, 10) : null;
    setSkuId(id);
    if (!id) return;
    setImageSource('sku_main_image');
    await applySkuMainImage(id);
  };

  const handleBrandSelect = (value: string | null) => {
    const id = value ? Number.parseInt(value, 10) : null;
    setBrandId(id);
    if (!id) return;
    setImageSource('brand_logo');
    applyBrandLogo(id);
  };

  const cancelUpload = async () => {
    if (submitting) return false;
    epoch.current++; setImageUploadState('cancelling');
    try {
      await task.current?.cancel(); task.current = null; fileRef.current = undefined; uploadKey.current = null;
      setImageKey(banner?.image_object_key ?? ''); setImageUrl(banner?.image_url ?? '');
      setImageSource(banner?.image_source ?? 'custom_upload');
      setImageUploadState('cancelled'); setImageError(null); setWarning(undefined);
      return true;
    } catch {
      setImageUploadState('failed'); setImageError('取消未成功，请重试取消'); setRetryable(false);
      return false;
    }
  };
  const close = () => { if (submitting) return; if (task.current || busy) setLeavePrompt(true); else onClose(); };
  const handleCustomUpload = async (file: File | undefined, retry = false) => {
    if (!file || busy) return;
    if (!retry && task.current && !await cancelUpload()) return;
    const token = ++epoch.current; fileRef.current = file;
    setError(null); setImageError(null); setWarning(undefined); setRetryable(true);
    setImageUploadState('uploading'); setImageProgress(0);
    try {
      const result = await uploadBannerImage(file, progress => {
        if (token === epoch.current) {
          setImageProgress(progress);
          if (progress > 0) setImageUploadState(value => value === 'uploading' ? 'transferring' : value);
        }
      }, {
        bannerId: mode === 'edit' ? banner?.id : undefined,
        task: retry ? task.current ?? undefined : undefined,
        onTask: value => { task.current = value; },
        onUpdate: value => {
          if (token !== epoch.current) return;
          setImageUploadState(value.stage); setRetryable(value.retryable ?? false);
          setImageError(value.error ?? null); setWarning(value.warning);
        },
      });
      if (token !== epoch.current) return;
      uploadKey.current = result.object_key;
      setImageKey(result.object_key); setImageUrl(result.display_url ?? result.url);
      setImageSource('custom_upload'); setSkuGalleryAssetId(null); setImageUploadState('uploaded');
    } catch (err) {
      if (token !== epoch.current) return;
      setImageUploadState('failed'); setImageError(getErrorMessage(err, '图片上传失败'));
    }
  };

  const handleSubmit = async () => {
    if (busy || imageUploadState === 'failed') {
      setError('图片上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);

    const sort = Number.parseInt(sortOrder, 10);
    if (!Number.isFinite(sort) || sort < 1) {
      setError('排序必须为正整数');
      setSubmitting(false);
      return;
    }
    if (!imageKey.trim()) {
      setError('请配置 Banner 图片');
      setSubmitting(false);
      return;
    }
    const internalTitle = buildInternalBannerTitle({
      mode,
      existingTitle: title,
      position,
      jumpType,
    });

    const payload = {
      title: internalTitle,
      display_client: MINIAPP_DISPLAY_CLIENT,
      position,
      image_object_key: imageKey,
      image_source: imageSource,
      sku_gallery_asset_id: skuGalleryAssetId,
      jump_type: jumpType,
      sku_id: skuId,
      external_url: externalUrl.trim() || null,
      topic_id: topicId,
      brand_id: brandId,
      sort_order: sort,
      valid_from: validFrom ? `${validFrom}:00+00:00` : null,
      valid_to: validTo ? `${validTo}:59+00:00` : null,
      remark: remark.trim() || null,
    } satisfies BannerCreateRequest;

    try {
      if (task.current && (imageSource !== 'custom_upload' || uploadKey.current !== imageKey)) {
        await task.current.cancel(); task.current = null; uploadKey.current = null;
        setImageUploadState('idle');
      }
      if (mode === 'create') {
        await createBanner(payload);
        onSuccess('Banner 已创建');
      } else if (banner) {
        await updateBanner(banner.id, payload);
        onSuccess('Banner 已更新');
      }
      task.current?.markSaved?.();
      task.current = null; fileRef.current = undefined; uploadKey.current = null;
      onClose();
    } catch (err) {
      setError(normalizeBannerSaveError(getErrorMessage(err, '保存失败')));
    } finally {
      setSubmitting(false);
    }
  };

  const skuSelectOptions = useMemo(
    () => skuOptions.map((sku) => ({ value: String(sku.id), label: sku.label })),
    [skuOptions],
  );

  const topicSelectOptions = useMemo(
    () => topicOptions.map((topic) => ({ value: String(topic.id), label: topic.label })),
    [topicOptions],
  );

  const brandSelectOptions = useMemo(
    () => brandOptions.map((brand) => ({ value: String(brand.id), label: brand.label })),
    [brandOptions],
  );

  if (!open) return null;

  const modalTitle =
    mode === 'edit'
      ? `编辑 Banner · ${JUMP_TYPE_OPTIONS.find((o) => o.value === jumpType)?.label ?? ''}`
      : jumpTypeModalTitle(jumpType);
  const positions = POSITIONS_BY_CLIENT[displayClient] ?? POSITIONS_BY_CLIENT.MINIAPP_HOME;
  const isImageUploading = busy;
  const uploadButtonLabel = isImageUploading ? '上传中' : imageUrl ? '更换' : '选择';

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        className="banner-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="banner-form-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <span id="banner-form-title" className="modal-title">
            {modalTitle}
          </span>
          <button type="button" className="modal-close" aria-label="关闭" onClick={close}>
            ×
          </button>
        </div>
        <div className="modal-body">
          {error ? <p className="page-desc text-[var(--admin-danger)]">{error}</p> : null}
          <div className="banner-form-grid">
            <label className="banner-form-row">
              <span className="field-label">
                展示端<span className="banner-form-required">*</span>
              </span>
              <select
                aria-label="展示端"
                className="select banner-display-client-select"
                value={MINIAPP_DISPLAY_CLIENT}
                disabled
              >
                <option value={MINIAPP_DISPLAY_CLIENT}>小程序</option>
              </select>
            </label>

            <label className="banner-form-row">
              <span className="field-label">
                展示位置<span className="banner-form-required">*</span>
              </span>
              <select
                disabled={busy}
                aria-label="展示位置"
                className="select"
                value={position}
                onChange={(e) => setPosition(e.target.value as BannerCreateRequestPosition)}
              >
                {positions.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </label>

            <div className="banner-form-row full">
              <span className="field-label">
                Banner 图片<span className="banner-form-required">*</span>
              </span>
              <div className="banner-upload-box">
                <div className="banner-upload-preview">
                  {imageUrl ? <AuthorizedImage file={imageSource === 'custom_upload' && uploadKey.current === imageKey ? fileRef.current : undefined} reference={imageSource === 'custom_upload' && uploadKey.current === imageKey && task.current?.sessionId ? {resource_type: 'upload_session', resource_id: task.current.sessionId, variant: 'display'} : (imageSource === 'sku_main_image' || imageSource === 'sku_gallery_image') && skuId ? {resource_type: 'sku_image', resource_id: String(skuId), media_id: skuGalleryAssetId ?? undefined, variant: 'display'} : imageSource === 'brand_logo' && brandId ? {resource_type: 'brand_logo', resource_id: String(brandId), variant: 'display'} : banner ? {resource_type: 'banner_image', resource_id: String(banner.id), variant: 'display'} : undefined} src={imageUrl} alt="" /> : null}
                </div>
                <div>
                  <div className="banner-upload-desc">
                    {jumpType === 'SKU_DETAIL'
                      ? '默认从关联 SKU 图库选择主图；也支持自定义上传运营图。'
                      : jumpType === 'BRAND_DETAIL'
                        ? '默认从关联品牌 Logo 取图；也支持自定义上传运营图。'
                        : '请上传 Banner 运营图，建议 16:6 比例。'}
                  </div>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {jumpType === 'SKU_DETAIL' ? (
                      <button
                        type="button"
                        className="btn subtle"
                        disabled={!skuId || busy}
                        onClick={() => skuId && void applySkuMainImage(skuId)}
                      >
                        使用 SKU 主图
                      </button>
                    ) : null}
                    {jumpType === 'BRAND_DETAIL' ? (
                      <button
                        type="button"
                        className="btn subtle"
                        disabled={!brandId || busy}
                        onClick={() => brandId && applyBrandLogo(brandId)}
                      >
                        使用品牌 Logo
                      </button>
                    ) : null}
                    <label
                      className={`btn${isImageUploading ? ' disabled' : ''}`}
                      aria-disabled={isImageUploading}
                    >
                      {uploadButtonLabel}
                      <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        disabled={isImageUploading}
                        hidden
                        onChange={(event) => {
                          const input = event.currentTarget;
                          void handleCustomUpload(input.files?.[0]).finally(() => {
                            input.value = '';
                          });
                        }}
                      />
                    </label>
                  </div>
                </div>
              </div>
              <MediaUploadStatus mediaKind="image" stage={imageUploadState === 'uploading' ? 'authorizing' : imageUploadState}
                progress={imageProgress} fileName={fileRef.current?.name} error={imageError}
                onCancel={() => void cancelUpload()}
                onRetry={retryable ? () => void handleCustomUpload(fileRef.current, true) : undefined} />
              {warning ? <p className="text-brand-gold">{warning}</p> : null}
            </div>

            <label className="banner-form-row">
              <span className="field-label">
                跳转类型<span className="banner-form-required">*</span>
              </span>
              <select className="select" value={jumpType} onChange={(e) => handleJumpTypeChange(e.target.value)}>
                {JUMP_TYPE_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </label>

            {jumpType === 'SKU_DETAIL' ? (
              <label className="banner-form-row">
                <span className="field-label">
                  关联 SKU<span className="banner-form-required">*</span>
                </span>
                <SearchableSelect
                  disabled={busy}
                  value={skuId != null ? String(skuId) : null}
                  options={skuSelectOptions}
                  onChange={(value) => void handleSkuSelect(value)}
                  onSearch={(keyword) => void loadSkuOptions(keyword)}
                  placeholder="搜索 SKU 名称或编码"
                  aria-label="关联 SKU"
                />
              </label>
            ) : null}

            {jumpType === 'BRAND_DETAIL' ? (
              <label className="banner-form-row">
                <span className="field-label">
                  关联品牌<span className="banner-form-required">*</span>
                </span>
                <SearchableSelect
                  disabled={busy}
                  value={brandId != null ? String(brandId) : null}
                  options={brandSelectOptions}
                  onChange={handleBrandSelect}
                  onSearch={(keyword) => void loadBrandOptions(keyword)}
                  placeholder="搜索品牌名称或简称"
                  aria-label="关联品牌"
                />
              </label>
            ) : null}

            {jumpType === 'EXTERNAL_LINK' ? (
              <label className="banner-form-row">
                <span className="field-label">
                  外部链接<span className="banner-form-required">*</span>
                </span>
                <input
                  className="input"
                  value={externalUrl}
                  onChange={(e) => setExternalUrl(e.target.value)}
                  placeholder="https://"
                />
              </label>
            ) : null}

            {jumpType === 'TOPIC_PAGE' ? (
              <label className="banner-form-row">
                <span className="field-label">
                  关联专题<span className="banner-form-required">*</span>
                </span>
                <SearchableSelect
                  disabled={busy}
                  value={topicId != null ? String(topicId) : null}
                  options={topicSelectOptions}
                  onChange={(value) =>
                    setTopicId(value ? Number.parseInt(value, 10) : null)
                  }
                  onSearch={(keyword) => void loadTopicOptions(keyword)}
                  placeholder="搜索专题名称"
                  aria-label="关联专题"
                />
              </label>
            ) : null}

            {jumpType === 'NO_JUMP' ? (
              <div className="banner-form-row">
                <span className="field-label">跳转目标</span>
                <div className="banner-jump-disabled">无需配置跳转目标</div>
              </div>
            ) : null}

            <label className="banner-form-row">
              <span className="field-label">
                排序<span className="banner-form-required">*</span>
              </span>
              <input
                className="input"
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
                placeholder="数字越小越靠前"
              />
            </label>

            <label className="banner-form-row full">
              <span className="field-label">有效期</span>
              <BannerValidityField
                validFrom={validFrom}
                validTo={validTo}
                onValidFromChange={setValidFrom}
                onValidToChange={setValidTo}
              />
            </label>

            <label className="banner-form-row full">
              <span className="field-label">运营备注</span>
              <textarea
                className="textarea banner-remark-textarea"
                value={remark}
                onChange={(e) => setRemark(e.target.value)}
                placeholder="请输入备注，不在前台展示"
              />
            </label>
          </div>
        </div>
        {leavePrompt ? <div role="alertdialog" aria-label="离开上传" className="modal-body">
          <p>离开将取消未保存的图片上传。</p>
          <button type="button" className="btn" onClick={() => setLeavePrompt(false)}>继续编辑</button>
          <button type="button" className="btn" disabled={imageUploadState === 'cancelling'}
            onClick={() => void cancelUpload().then(ok => { if (ok) onClose(); })}>取消上传并离开</button>
        </div> : null}
        <div className="modal-footer">
          <button type="button" className="btn" onClick={close}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting || isImageUploading || imageUploadState === 'failed'}
            onClick={() => void handleSubmit()}
          >
            {submitting ? '保存中…' : '保存 Banner'}
          </button>
        </div>
      </div>
    </div>
  );
}
