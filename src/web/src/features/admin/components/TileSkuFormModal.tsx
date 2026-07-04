import { useEffect, useRef, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type {
  BrandAdminItem,
  TileCategoryTreeNode,
  TileSkuAdminItem,
  TileSpecAdminItem,
} from '@/shared/api/generated';

import { fetchTileSpecs } from '../api/tile-specs-api';
import { fetchBrands } from '../api/brands-api';
import { fetchCategoryTree } from '../api/tile-categories-api';
import {
  createTileSku,
  updateTileSku,
  uploadTileImage,
  uploadTileVideo,
} from '../api/tile-skus-api';

interface CategoryOption {
  id: number;
  label: string;
}

function buildCategoryOptions(tree: TileCategoryTreeNode[]): CategoryOption[] {
  const options: CategoryOption[] = [];
  const walk = (nodes: TileCategoryTreeNode[], prefix: string) => {
    for (const node of nodes) {
      const label = prefix ? `${prefix} / ${node.name}` : node.name;
      options.push({ id: node.id, label });
      if (node.children?.length) {
        walk(node.children, label);
      }
    }
  };
  walk(tree, '');
  return options;
}

interface ImageDraft {
  object_key: string;
  url: string;
  is_main: boolean;
  sort_order: number;
}

interface VideoDraft {
  object_key: string;
  url: string;
  file_name: string;
  file_size_bytes?: number | null;
  duration_seconds?: number | null;
  sort_order: number;
}

type VideoUploadState = 'idle' | 'uploading' | 'uploaded' | 'failed';

function resolveVideoUrl(video: Pick<VideoDraft, 'object_key' | 'url'>): string {
  return video.url || `/media/${video.object_key}`;
}

function formatVideoSize(bytes?: number | null): string {
  if (!bytes) {
    return '—';
  }
  if (bytes >= 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }
  return `${Math.round(bytes / 1024)} KB`;
}

interface TileSkuFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  sku: TileSkuAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function TileSkuFormModal({ open, mode, sku, onClose, onSuccess }: TileSkuFormModalProps) {
  const [name, setName] = useState('');
  const [skuCode, setSkuCode] = useState('');
  const [brandId, setBrandId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [specId, setSpecId] = useState('');
  const [size, setSize] = useState('');
  const [surfaceFinish, setSurfaceFinish] = useState('');
  const [colorFamily, setColorFamily] = useState('');
  const [referencePrice, setReferencePrice] = useState('');
  const [remark, setRemark] = useState('');
  const [images, setImages] = useState<ImageDraft[]>([]);
  const [videos, setVideos] = useState<VideoDraft[]>([]);
  const [brands, setBrands] = useState<BrandAdminItem[]>([]);
  const [categories, setCategories] = useState<CategoryOption[]>([]);
  const [tileSpecs, setTileSpecs] = useState<TileSpecAdminItem[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [videoUploadState, setVideoUploadState] = useState<VideoUploadState>('idle');
  const [videoUploadProgress, setVideoUploadProgress] = useState(0);
  const [videoUploadError, setVideoUploadError] = useState<string | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);
  const videoListRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    void Promise.all([
      fetchBrands({ page: 1, page_size: 100, status: 'ENABLED' }),
      fetchCategoryTree(),
      fetchTileSpecs({ page: 1, page_size: 100, status: 'ENABLED' }),
    ]).then(([brandData, tree, specData]) => {
      setBrands(brandData.items);
      setCategories(buildCategoryOptions(tree));
      setTileSpecs(specData.items);
    });
  }, [open]);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setVideoUploadState('idle');
    setVideoUploadProgress(0);
    setVideoUploadError(null);
    if (mode === 'edit' && sku) {
      setName(sku.name);
      setSkuCode(sku.sku_code);
      setBrandId(String(sku.brand_id));
      setCategoryId(String(sku.category_id));
      setSpecId(sku.spec_id != null ? String(sku.spec_id) : '');
      setSize(sku.size);
      setSurfaceFinish(sku.surface_finish);
      setColorFamily(sku.color_family ?? '');
      setReferencePrice(
        sku.reference_price != null ? String(sku.reference_price) : '0',
      );
      setRemark(sku.remark ?? '');
      setImages(
        (sku.images ?? []).map((img, idx) => ({
          object_key: img.object_key,
          url: img.url,
          is_main: img.is_main,
          sort_order: img.sort_order ?? idx,
        })),
      );
      setVideos(
        (sku.videos ?? []).map((vid, idx) => ({
          object_key: vid.object_key,
          url: vid.url,
          file_name: vid.file_name,
          file_size_bytes: vid.file_size_bytes,
          duration_seconds: vid.duration_seconds,
          sort_order: vid.sort_order ?? idx,
        })),
      );
    } else {
      setName('');
      setSkuCode('');
      setBrandId('');
      setCategoryId('');
      setSpecId('');
      setSize('');
      setSurfaceFinish('');
      setColorFamily('');
      setReferencePrice('0');
      setRemark('');
      setImages([]);
      setVideos([]);
    }
  }, [open, mode, sku]);

  if (!open) return null;

  const parseReferencePrice = (): number | null => {
    const trimmed = referencePrice.trim();
    if (!trimmed) {
      return null;
    }
    const price = Number.parseFloat(trimmed);
    if (!Number.isFinite(price) || price < 0) {
      return null;
    }
    return price;
  };

  const validateSubmitFields = (): boolean => {
    if (!name.trim()) {
      setError('SKU 名称不能为空');
      return false;
    }
    if (!skuCode.trim()) {
      setError('SKU 编码不能为空');
      return false;
    }
    if (!brandId) {
      setError('请选择品牌');
      return false;
    }
    if (!categoryId) {
      setError('请选择类目');
      return false;
    }
    if (!specId) {
      setError('请选择瓷砖规格');
      return false;
    }
    if (parseReferencePrice() === null) {
      setError('参考价格不能为空');
      return false;
    }
    return true;
  };

  const buildPayload = () => {
    const price = parseReferencePrice() ?? 0;
    return {
      name: name.trim(),
      sku_code: skuCode.trim() || undefined,
      brand_id: brandId ? Number.parseInt(brandId, 10) : undefined,
      category_id: categoryId ? Number.parseInt(categoryId, 10) : undefined,
      spec_id: specId ? Number.parseInt(specId, 10) : undefined,
      size: size.trim() || undefined,
      surface_finish: surfaceFinish.trim() || undefined,
      color_family: colorFamily.trim() || null,
      reference_price: price,
      remark: remark.trim() || null,
      images: images.map((img, idx) => ({
        object_key: img.object_key,
        url: img.url,
        is_main: img.is_main,
        sort_order: idx,
      })),
      videos: videos.map((vid, idx) => ({
        object_key: vid.object_key,
        file_name: vid.file_name,
        file_size_bytes: vid.file_size_bytes ?? null,
        duration_seconds: vid.duration_seconds ?? null,
        sort_order: idx,
      })),
    };
  };

  const handleSave = async (saveMode: 'draft' | 'create') => {
    if (videoUploadState === 'uploading') {
      setError('视频上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);
    if (saveMode === 'draft' && !name.trim()) {
      setError('SKU 名称不能为空');
      setSubmitting(false);
      return;
    }
    if (saveMode === 'create' && !validateSubmitFields()) {
      setSubmitting(false);
      return;
    }
    if (mode === 'edit' && !validateSubmitFields()) {
      setSubmitting(false);
      return;
    }

    try {
      if (mode === 'create') {
        await createTileSku({ ...buildPayload(), save_mode: saveMode });
        onSuccess(saveMode === 'draft' ? '草稿已保存' : 'SKU 创建成功，已保存为草稿');
      } else if (sku) {
        await updateTileSku(sku.id, buildPayload());
        onSuccess('SKU 已更新');
      }
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleImageUpload = async (file: File | undefined) => {
    if (!file) return;
    try {
      const result = await uploadTileImage(file, sku?.id);
      setImages((prev) => [
        ...prev,
        {
          object_key: result.object_key,
          url: result.url,
          is_main: prev.length === 0,
          sort_order: prev.length,
        },
      ]);
    } catch (err) {
      setError(getErrorMessage(err, '图片上传失败'));
    }
  };

  const handleVideoUpload = async (file: File | undefined) => {
    if (!file) return;
    setVideoUploadError(null);
    setVideoUploadState('uploading');
    setVideoUploadProgress(8);
    try {
      const result = await uploadTileVideo(file, sku?.id, (progress) => {
        setVideoUploadProgress(progress);
      });
      setVideos((prev) => [
        ...prev,
        {
          object_key: result.object_key,
          url: result.url,
          file_name: file.name,
          file_size_bytes: file.size,
          sort_order: prev.length,
        },
      ]);
      setVideoUploadProgress(100);
      setVideoUploadState('uploaded');
      requestAnimationFrame(() => {
        const lastVideoCard = videoListRef.current?.lastElementChild;
        if (typeof lastVideoCard?.scrollIntoView !== 'function') return;
        lastVideoCard.scrollIntoView({
          block: 'nearest',
          behavior: 'smooth',
        });
      });
    } catch (err) {
      const message = getErrorMessage(err, '视频上传失败');
      setVideoUploadState('failed');
      setVideoUploadProgress(0);
      setVideoUploadError(message);
    }
  };

  const isVideoUploading = videoUploadState === 'uploading';

  const setMainImage = (index: number) => {
    setImages((prev) => prev.map((img, i) => ({ ...img, is_main: i === index })));
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="sku-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="tile-sku-modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <div>
            <h2 id="tile-sku-modal-title" className="modal-title">
              {mode === 'create' ? (
                <>
                  新增 SKU{' '}
                  <span className="default-note">创建后默认草稿</span>
                </>
              ) : (
                '编辑 SKU'
              )}
            </h2>
            <p className="modal-desc">
              维护 SKU 基础资料、参考价格、图片与视频素材；弹窗内不提供状态选择。
            </p>
          </div>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          {error ? <p className="admin-notice">{error}</p> : null}
          <div className="sku-form-grid">
            <div className="brand-form-item">
              <label>
                SKU 名称 <span className="req">*</span>
              </label>
              <input className="input" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="brand-form-item">
              <label>
                SKU 编码 <span className="req">*</span>
              </label>
              <input className="input" value={skuCode} onChange={(e) => setSkuCode(e.target.value)} />
            </div>
            <div className="brand-form-item">
              <label>
                品牌 <span className="req">*</span>
              </label>
              <select className="select" value={brandId} onChange={(e) => setBrandId(e.target.value)}>
                <option value="">请选择品牌</option>
                {brands.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="brand-form-item">
              <label>
                类目 <span className="req">*</span>
              </label>
              <select
                className="select"
                value={categoryId}
                onChange={(e) => setCategoryId(e.target.value)}
              >
                <option value="">请选择类目</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="brand-form-item">
              <label>
                瓷砖规格 <span className="req">*</span>
              </label>
              <select
                className="select"
                value={specId}
                onChange={(e) => {
                  const nextId = e.target.value;
                  setSpecId(nextId);
                  const selected = tileSpecs.find((item) => String(item.id) === nextId);
                  setSize(selected?.display_name ?? '');
                }}
              >
                <option value="">请选择规格</option>
                {tileSpecs.map((spec) => (
                  <option key={spec.id} value={spec.id}>
                    {spec.display_name}
                  </option>
                ))}
                {mode === 'edit' && specId && !tileSpecs.some((item) => String(item.id) === specId) ? (
                  <option value={specId}>{size || `规格 #${specId}`}</option>
                ) : null}
              </select>
              {!specId && mode === 'edit' && sku && !sku.spec_id ? (
                <p className="form-help">历史 SKU 未匹配规格，请手动选择后保存</p>
              ) : null}
            </div>
            <div className="brand-form-item">
              <label>表面工艺</label>
              <input
                className="input"
                value={surfaceFinish}
                onChange={(e) => setSurfaceFinish(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label>主色系</label>
              <input
                className="input"
                value={colorFamily}
                onChange={(e) => setColorFamily(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label>
                参考价格（元） <span className="req">*</span>
              </label>
              <input
                className="input"
                type="number"
                step="0.01"
                min="0"
                value={referencePrice}
                onChange={(e) => setReferencePrice(e.target.value)}
              />
            </div>
            <div className="brand-form-item sku-form-full">
              <label>备注说明</label>
              <textarea
                className="brand-textarea"
                style={{ height: 76 }}
                value={remark}
                onChange={(e) => setRemark(e.target.value)}
              />
            </div>

            <p className="sku-section-label">商品图片</p>
            <div className="sku-form-full">
              <div className="sku-upload-grid">
                {images.map((img, index) => (
                  <div key={img.object_key} className="sku-image-tile">
                    <img src={img.url} alt="" />
                    {img.is_main ? <span className="sku-main-flag">主图</span> : null}
                    {!img.is_main ? (
                      <button
                        type="button"
                        className="sku-set-main"
                        onClick={() => setMainImage(index)}
                      >
                        设为主图
                      </button>
                    ) : null}
                  </div>
                ))}
                <button
                  type="button"
                  className="sku-add-tile"
                  onClick={() => imageInputRef.current?.click()}
                >
                  <span style={{ fontSize: 20 }}>＋</span>
                  继续添加图片
                </button>
              </div>
              <p className="sku-help">支持 JPG、PNG、WebP；可上传多张并指定一张主图</p>
              <input
                ref={imageInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                hidden
                onChange={(e) => void handleImageUpload(e.target.files?.[0])}
              />
            </div>

            <p className="sku-section-label">商品视频</p>
            <div className="sku-form-full sku-video-section">
              <div className="sku-video-list" ref={videoListRef}>
                {videos.map((vid) => (
                  <div key={vid.object_key} className="sku-video-card">
                    <div className="sku-video-player-wrap">
                      <video
                        className="sku-video-player"
                        src={resolveVideoUrl(vid)}
                        controls
                        preload="metadata"
                        playsInline
                        aria-label={vid.file_name}
                      />
                      <button
                        type="button"
                        className="sku-video-remove"
                        onClick={() =>
                          setVideos((prev) => prev.filter((v) => v.object_key !== vid.object_key))
                        }
                      >
                        移除
                      </button>
                    </div>
                    <div className="sku-video-caption">
                      <span className="sku-video-name">{vid.file_name}</span>
                      <span className="sku-video-meta">
                        {formatVideoSize(vid.file_size_bytes)}
                        {vid.duration_seconds != null
                          ? ` · ${Math.round(vid.duration_seconds)}s`
                          : ''}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
              {isVideoUploading ? (
                <div className="sku-video-upload-status">
                  <span
                    className="sku-video-progress"
                    role="progressbar"
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={videoUploadProgress}
                  >
                    <span
                      className="sku-video-progress-bar"
                      style={{ width: `${videoUploadProgress}%` }}
                    />
                  </span>
                  <span className="sku-video-progress-text">
                    上传中 {videoUploadProgress}%
                  </span>
                </div>
              ) : null}
              {videoUploadState === 'uploaded' ? (
                <span className="sku-video-upload-success">视频已添加</span>
              ) : null}
              {videoUploadState === 'failed' && videoUploadError ? (
                <span className="sku-video-upload-error" role="alert">
                  {videoUploadError}
                </span>
              ) : null}
              <button
                type="button"
                className={`btn sku-video-upload-btn${isVideoUploading ? ' disabled' : ''}`}
                aria-disabled={isVideoUploading}
                disabled={isVideoUploading}
                onClick={() => videoInputRef.current?.click()}
              >
                {isVideoUploading ? '上传中' : '上传视频'}
              </button>
              <input
                ref={videoInputRef}
                type="file"
                accept="video/mp4"
                hidden
                disabled={isVideoUploading}
                onChange={(e) => {
                  const input = e.currentTarget;
                  void handleVideoUpload(input.files?.[0]).finally(() => {
                    input.value = '';
                  });
                }}
              />
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button
            type="button"
            className="btn"
            onClick={onClose}
            disabled={submitting || isVideoUploading}
          >
            取消
          </button>
          {mode === 'create' ? (
            <>
              <button
                type="button"
                className="btn"
                disabled={submitting || isVideoUploading}
                onClick={() => void handleSave('draft')}
              >
                保存草稿
              </button>
              <button
                type="button"
                className="btn primary"
                disabled={submitting || isVideoUploading}
                onClick={() => void handleSave('create')}
              >
                创建 SKU
              </button>
            </>
          ) : (
            <button
              type="button"
              className="btn primary"
              disabled={submitting || isVideoUploading}
              onClick={() => void handleSave('create')}
            >
              保存
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
