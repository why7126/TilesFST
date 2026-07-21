import { useCallback, useEffect, useMemo, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BannerAdminItem } from '@/shared/api/generated';
import { SearchableSelect } from '@/shared/ui/searchable-select';

import { fetchBrands } from '../api/brands-api';
import { fetchTileSku, fetchTileSkus } from '../api/tile-skus-api';
import { createBanner, updateBanner, uploadBannerImage } from '../api/banners-api';
import { fetchTopics } from '../api/topics-api';
import {
  DEFAULT_POSITION,
  JUMP_TYPE_OPTIONS,
  POSITIONS_BY_CLIENT,
  clearJumpFieldsForType,
  extractSkuMainImage,
  jumpTypeModalTitle,
} from '../lib/banner-display';
import { BannerValidityField } from './BannerValidityField';

type ImageUploadState = 'idle' | 'uploading' | 'uploaded' | 'failed';

const MINIAPP_DISPLAY_CLIENT = 'MINIAPP_HOME';

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
  const [title, setTitle] = useState('');
  const [displayClient, setDisplayClient] = useState(MINIAPP_DISPLAY_CLIENT);
  const [position, setPosition] = useState(DEFAULT_POSITION.MINIAPP_HOME!);
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
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [skuOptions, setSkuOptions] = useState<SkuOption[]>([]);
  const [topicOptions, setTopicOptions] = useState<TopicOption[]>([]);
  const [brandOptions, setBrandOptions] = useState<BrandOption[]>([]);

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
    try {
      const sku = await fetchTileSku(id);
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
          ? banner.position
          : DEFAULT_POSITION.MINIAPP_HOME!,
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
      setPosition(DEFAULT_POSITION.MINIAPP_HOME!);
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

  const handleCustomUpload = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setImageUploadState('uploading');
    try {
      const result = await uploadBannerImage(file);
      setImageKey(result.object_key);
      setImageUrl(result.url);
      setImageSource('custom_upload');
      setSkuGalleryAssetId(null);
      setImageUploadState('uploaded');
    } catch (err) {
      setImageUploadState('failed');
      setError(getErrorMessage(err, '图片上传失败'));
    }
  };

  const handleSubmit = async () => {
    if (imageUploadState === 'uploading') {
      setError('图片上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);

    const sort = Number.parseInt(sortOrder, 10);
    if (!title.trim()) {
      setError('Banner 标题不能为空');
      setSubmitting(false);
      return;
    }
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

    const payload = {
      title: title.trim(),
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
    };

    try {
      if (mode === 'create') {
        await createBanner(payload);
        onSuccess('Banner 已创建');
      } else if (banner) {
        await updateBanner(banner.id, payload);
        onSuccess('Banner 已更新');
      }
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
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
  const isImageUploading = imageUploadState === 'uploading';
  const uploadButtonLabel = isImageUploading ? '上传中' : imageUrl ? '更换' : '选择';

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
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
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          {error ? <p className="page-desc text-[var(--admin-danger)]">{error}</p> : null}
          <div className="banner-form-grid">
            <label className="banner-form-row full">
              <span className="field-label">
                Banner 标题<span className="banner-form-required">*</span>
              </span>
              <input
                className="input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="请输入 Banner 标题"
              />
              <div className="banner-form-help">同一展示端 + 展示位置下标题不可重复，建议 2-30 个字符。</div>
            </label>

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
                aria-label="展示位置"
                className="select"
                value={position}
                onChange={(e) => setPosition(e.target.value)}
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
                  {imageUrl ? <img src={imageUrl} alt="" /> : null}
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
                        disabled={!skuId}
                        onClick={() => skuId && void applySkuMainImage(skuId)}
                      >
                        使用 SKU 主图
                      </button>
                    ) : null}
                    {jumpType === 'BRAND_DETAIL' ? (
                      <button
                        type="button"
                        className="btn subtle"
                        disabled={!brandId}
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
        <div className="modal-footer">
          <button type="button" className="btn" onClick={onClose}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting || isImageUploading}
            onClick={() => void handleSubmit()}
          >
            {submitting ? '保存中…' : '保存 Banner'}
          </button>
        </div>
      </div>
    </div>
  );
}
