import { useEffect, useRef, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BrandAdminItem, TileCategoryTreeNode, TileSkuAdminItem } from '@/shared/api/generated';

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
  file_name: string;
  file_size_bytes?: number | null;
  duration_seconds?: number | null;
  sort_order: number;
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
  const [size, setSize] = useState('');
  const [surfaceFinish, setSurfaceFinish] = useState('');
  const [colorFamily, setColorFamily] = useState('');
  const [referencePrice, setReferencePrice] = useState('');
  const [remark, setRemark] = useState('');
  const [images, setImages] = useState<ImageDraft[]>([]);
  const [videos, setVideos] = useState<VideoDraft[]>([]);
  const [brands, setBrands] = useState<BrandAdminItem[]>([]);
  const [categories, setCategories] = useState<CategoryOption[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!open) return;
    void Promise.all([
      fetchBrands({ page: 1, page_size: 100, status: 'ENABLED' }),
      fetchCategoryTree(),
    ]).then(([brandData, tree]) => {
      setBrands(brandData.items);
      setCategories(buildCategoryOptions(tree));
    });
  }, [open]);

  useEffect(() => {
    if (!open) return;
    setError(null);
    if (mode === 'edit' && sku) {
      setName(sku.name);
      setSkuCode(sku.sku_code);
      setBrandId(String(sku.brand_id));
      setCategoryId(String(sku.category_id));
      setSize(sku.size);
      setSurfaceFinish(sku.surface_finish);
      setColorFamily(sku.color_family ?? '');
      setReferencePrice(sku.reference_price != null ? String(sku.reference_price) : '');
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
      setSize('');
      setSurfaceFinish('');
      setColorFamily('');
      setReferencePrice('');
      setRemark('');
      setImages([]);
      setVideos([]);
    }
  }, [open, mode, sku]);

  if (!open) return null;

  const validateCreateFields = (): boolean => {
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
    if (!size.trim()) {
      setError('规格尺寸不能为空');
      return false;
    }
    if (!surfaceFinish.trim()) {
      setError('表面工艺不能为空');
      return false;
    }
    return true;
  };

  const buildPayload = () => {
    const price = referencePrice.trim() ? Number.parseFloat(referencePrice) : null;
    return {
      name: name.trim(),
      sku_code: skuCode.trim() || undefined,
      brand_id: brandId ? Number.parseInt(brandId, 10) : undefined,
      category_id: categoryId ? Number.parseInt(categoryId, 10) : undefined,
      size: size.trim() || undefined,
      surface_finish: surfaceFinish.trim() || undefined,
      color_family: colorFamily.trim() || null,
      reference_price: Number.isFinite(price!) ? price : null,
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
    setSubmitting(true);
    setError(null);
    if (saveMode === 'draft' && !name.trim()) {
      setError('SKU 名称不能为空');
      setSubmitting(false);
      return;
    }
    if (saveMode === 'create' && !validateCreateFields()) {
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
    try {
      const result = await uploadTileVideo(file, sku?.id);
      setVideos((prev) => [
        ...prev,
        {
          object_key: result.object_key,
          file_name: file.name,
          file_size_bytes: file.size,
          sort_order: prev.length,
        },
      ]);
    } catch (err) {
      setError(getErrorMessage(err, '视频上传失败'));
    }
  };

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
            <p className="modal-subtitle">
              录入基础资料、价格、图片和视频素材；弹窗内不提供状态选择
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
                规格尺寸 <span className="req">*</span>
              </label>
              <input className="input" value={size} onChange={(e) => setSize(e.target.value)} />
            </div>
            <div className="brand-form-item">
              <label>
                表面工艺 <span className="req">*</span>
              </label>
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
              <label>参考价格（元）</label>
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
            <div className="sku-form-full">
              <div className="sku-video-list">
                {videos.map((vid) => (
                  <div key={vid.object_key} className="sku-video-card">
                    <div className="sku-video-icon">MP4</div>
                    <div>
                      <span className="sku-video-name">{vid.file_name}</span>
                      <span className="sku-video-meta">
                        {vid.file_size_bytes
                          ? `${Math.round(vid.file_size_bytes / 1024)} KB`
                          : '—'}
                      </span>
                    </div>
                    <button
                      type="button"
                      className="sku-remove"
                      onClick={() =>
                        setVideos((prev) => prev.filter((v) => v.object_key !== vid.object_key))
                      }
                    >
                      移除
                    </button>
                  </div>
                ))}
              </div>
              <button
                type="button"
                className="btn"
                style={{ marginTop: 10 }}
                onClick={() => videoInputRef.current?.click()}
              >
                上传视频
              </button>
              <input
                ref={videoInputRef}
                type="file"
                accept="video/mp4"
                hidden
                onChange={(e) => void handleVideoUpload(e.target.files?.[0])}
              />
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button type="button" className="btn" onClick={onClose} disabled={submitting}>
            取消
          </button>
          {mode === 'create' ? (
            <>
              <button
                type="button"
                className="btn"
                disabled={submitting}
                onClick={() => void handleSave('draft')}
              >
                保存草稿
              </button>
              <button
                type="button"
                className="btn primary"
                disabled={submitting}
                onClick={() => void handleSave('create')}
              >
                创建 SKU
              </button>
            </>
          ) : (
            <button
              type="button"
              className="btn primary"
              disabled={submitting}
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
