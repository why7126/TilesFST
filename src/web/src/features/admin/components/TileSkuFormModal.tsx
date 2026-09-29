import { useModalReturnFocus } from './use-modal-return-focus';
import { AuthorizedImage, AuthorizedVideo } from '@/features/media/authorized-media';
import { useEffect, useMemo, useRef, useState } from 'react';
import { MediaUploadStatus, type UploadStage } from '@/features/media/media-upload-status';
import { MediaUploadFailure, type MediaUploadTask } from '@/features/media/media-upload-controller';
import { CircleHelp } from 'lucide-react';

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
import { fetchSettingsGroup } from '../api/system-settings-api';
import {
  createTileSku,
  updateTileSku,
  uploadTileImage,
  uploadTileVideo,
} from '../api/tile-skus-api';
import {
  buildAcceptValue,
  DEFAULT_MEDIA_UPLOAD_SETTINGS,
  formatMimeLabels,
  mediaUploadSettingsFromResponse,
} from '../lib/media-upload-settings';

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

export interface ImageDraft {
  previewFile?: File;
  media_id?: number;
  object_key: string;
  url: string;
  thumbnail_url?: string | null;
  display_url?: string | null;
  original_url?: string | null;
  is_main: boolean;
  sort_order: number;
}

export function normalizeImages(drafts: ImageDraft[]): ImageDraft[] {
  if (drafts.length === 0) {
    return [];
  }

  const mainIndex = drafts.findIndex((img) => img.is_main);
  const normalized = drafts.map((img, index) => ({
    ...img,
    is_main: mainIndex >= 0 ? index === mainIndex : index === 0,
  }));
  const selectedMain = normalized.find((img) => img.is_main) ?? normalized[0]!;
  const ordered = [
    selectedMain,
    ...normalized.filter((img) => img.object_key !== selectedMain.object_key),
  ];

  return ordered.map((img, index) => ({
    ...img,
    is_main: index === 0,
    sort_order: index,
  }));
}

export function removeImageDraft(drafts: ImageDraft[], index: number): ImageDraft[] {
  const removing = drafts[index];
  if (!removing) {
    return drafts;
  }
  const remaining = drafts.filter((_, i) => i !== index);
  if (remaining.length === 0) {
    return [];
  }
  if (!removing.is_main) {
    return normalizeImages(remaining);
  }

  const nextMain = drafts[index + 1] ?? remaining[0]!;
  return normalizeImages(remaining.map((img) => ({
    ...img,
    is_main: img.object_key === nextMain.object_key,
  })));
}

interface VideoDraft {
  media_id?: number;
  object_key: string;
  url: string;
  file_name: string;
  file_size_bytes?: number | null;
  duration_seconds?: number | null;
  sort_order: number;
}

type VideoUploadState = UploadStage;

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

function toDatetimeLocalValue(value?: string | null): string {
  if (!value) {
    return '';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return '';
  }
  const pad = (part: number) => String(part).padStart(2, '0');
  return [
    date.getFullYear(),
    pad(date.getMonth() + 1),
    pad(date.getDate()),
  ].join('-') + `T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

interface TileSkuFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  sku: TileSkuAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function TileSkuFormModal({ open, mode, sku, onClose, onSuccess }: TileSkuFormModalProps) {
  useModalReturnFocus(open);
  const [name, setName] = useState('');
  const [brandId, setBrandId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [specId, setSpecId] = useState('');
  const [size, setSize] = useState('');
  const [surfaceFinish, setSurfaceFinish] = useState('');
  const [colorFamily, setColorFamily] = useState('');
  const [referencePrice, setReferencePrice] = useState('');
  const [recallPinSortOrder, setRecallPinSortOrder] = useState('9999');
  const [recallPinStartsAt, setRecallPinStartsAt] = useState('');
  const [recallPinEndsAt, setRecallPinEndsAt] = useState('');
  const [remark, setRemark] = useState('');
  const [images, setImages] = useState<ImageDraft[]>([]);
  const [videos, setVideos] = useState<VideoDraft[]>([]);
  const [brands, setBrands] = useState<BrandAdminItem[]>([]);
  const [categories, setCategories] = useState<CategoryOption[]>([]);
  const [tileSpecs, setTileSpecs] = useState<TileSpecAdminItem[]>([]);
  const [mediaSettings, setMediaSettings] = useState(DEFAULT_MEDIA_UPLOAD_SETTINGS);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recallPinSortOrderError, setRecallPinSortOrderError] = useState<string | null>(null);
  const [imageUploadState, setImageUploadState] = useState<UploadStage | 'uploading'>('idle');
  const [imageUploadError, setImageUploadError] = useState<string | null>(null);
  const [videoUploadState, setVideoUploadState] = useState<VideoUploadState>('idle');
  const [videoUploadProgress, setVideoUploadProgress] = useState(0);
  const [videoUploadError, setVideoUploadError] = useState<string | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);
  const videoListRef = useRef<HTMLDivElement>(null);
  const imageTask = useRef<MediaUploadTask | null>(null);
  const imageFile = useRef<File | undefined>(undefined);
  const imageEpoch = useRef(0);
  const [imageUploadProgress, setImageUploadProgress] = useState(0);
  const [imageRetryable, setImageRetryable] = useState(true);
  const [imageWarning, setImageWarning] = useState<string | undefined>();
  const videoTask = useRef<MediaUploadTask | null>(null);
  const unboundMediaTasks = useRef(new Map<string, MediaUploadTask>());
  const videoFile = useRef<File | undefined>(undefined);
  const uploadEpoch = useRef(0);
  const localVideoUrls = useRef(new Set<string>());
  const [videoRetryable, setVideoRetryable] = useState(true);
  const [leaveUploadPrompt, setLeaveUploadPrompt] = useState(false);

  useEffect(() => {
    if (!open) return;
    return () => {
      uploadEpoch.current++; imageEpoch.current++;
      const tasks = new Set(unboundMediaTasks.current.values());
      if (videoTask.current) tasks.add(videoTask.current);
      if (imageTask.current) tasks.add(imageTask.current);
      for (const task of tasks) void task.cancel().catch(() => {});
      unboundMediaTasks.current.clear();
      videoTask.current = null; imageTask.current = null;
      for (const url of localVideoUrls.current) URL.revokeObjectURL(url);
      localVideoUrls.current.clear();
    };
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const warn = (event: BeforeUnloadEvent) => {
      if (unboundMediaTasks.current.size || ['authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling', 'failed'].includes(videoUploadState) || ['uploading', 'authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling', 'failed'].includes(imageUploadState)) {
        event.preventDefault(); event.returnValue = '';
      }
    };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [open, videoUploadState, imageUploadState]);


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
    void fetchSettingsGroup('media')
      .then((data) => setMediaSettings(mediaUploadSettingsFromResponse(data)))
      .catch(() => setMediaSettings(DEFAULT_MEDIA_UPLOAD_SETTINGS));
  }, [open]);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setRecallPinSortOrderError(null);
    setImageUploadState('idle');
    setImageUploadError(null);
    setImageUploadProgress(0);
    setImageWarning(undefined);
    setImageRetryable(true);
    setVideoUploadState('idle');
    setVideoUploadProgress(0);
    setVideoUploadError(null);
    setLeaveUploadPrompt(false);
    setVideoRetryable(true);
    if (mode === 'edit' && sku) {
      setName(sku.name);
      setBrandId(String(sku.brand_id));
      setCategoryId(String(sku.category_id));
      setSpecId(sku.spec_id != null ? String(sku.spec_id) : '');
      setSize(sku.size);
      setSurfaceFinish(sku.surface_finish);
      setColorFamily(sku.color_family ?? '');
      setReferencePrice(
        sku.reference_price != null ? String(sku.reference_price) : '0',
      );
      setRecallPinSortOrder(String(sku.recall_pin_sort_order ?? 9999));
      setRecallPinStartsAt(toDatetimeLocalValue(sku.recall_pin_starts_at));
      setRecallPinEndsAt(toDatetimeLocalValue(sku.recall_pin_ends_at));
      setRemark(sku.remark ?? '');
      setImages(
        normalizeImages((sku.images ?? []).map((img, idx) => ({
          media_id: img.id,
          object_key: img.object_key,
          url: img.url,
          thumbnail_url: img.thumbnail_url,
          display_url: img.display_url,
          original_url: img.original_url,
          is_main: img.is_main,
          sort_order: img.sort_order ?? idx,
        }))),
      );
      setVideos(
        (sku.videos ?? []).map((vid, idx) => ({
          media_id: vid.id,
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
      setBrandId('');
      setCategoryId('');
      setSpecId('');
      setSize('');
      setSurfaceFinish('');
      setColorFamily('');
      setReferencePrice('0');
      setRecallPinSortOrder('9999');
      setRecallPinStartsAt('');
      setRecallPinEndsAt('');
      setRemark('');
      setImages([]);
      setVideos([]);
    }
  }, [open, mode, sku]);

  const imageAccept = useMemo(
    () => buildAcceptValue(mediaSettings.allowedImageTypes),
    [mediaSettings.allowedImageTypes],
  );
  const videoAccept = useMemo(
    () => buildAcceptValue(mediaSettings.allowedVideoTypes),
    [mediaSettings.allowedVideoTypes],
  );
  const imageUploadHint = useMemo(
    () =>
      `支持 ${formatMimeLabels(mediaSettings.allowedImageTypes)}，单张最大 ${mediaSettings.maxImageSizeMb}MB；可上传多张，并指定一张主图`,
    [mediaSettings.allowedImageTypes, mediaSettings.maxImageSizeMb],
  );
  const videoUploadHint = useMemo(
    () =>
      `支持 ${formatMimeLabels(mediaSettings.allowedVideoTypes)}，单个视频最大 ${mediaSettings.maxVideoSizeMb}MB；可上传多个视频`,
    [mediaSettings.allowedVideoTypes, mediaSettings.maxVideoSizeMb],
  );

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

  const parseRecallPinSortOrder = (): number | null => {
    const trimmed = recallPinSortOrder.trim();
    if (!trimmed) {
      return 9999;
    }
    const order = Number.parseInt(trimmed, 10);
    if (!Number.isInteger(order) || String(order) !== trimmed || order <= 0) {
      return null;
    }
    return order;
  };

  const validateSubmitFields = (): boolean => {
    setRecallPinSortOrderError(null);
    if (!name.trim()) {
      setError('商品名称不能为空');
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
    if (parseRecallPinSortOrder() === null) {
      setRecallPinSortOrderError('排序值必须为正整数');
      return false;
    }
    if (recallPinStartsAt && recallPinEndsAt && recallPinStartsAt > recallPinEndsAt) {
      setError('召回置顶开始时间不能晚于结束时间');
      return false;
    }
    return true;
  };

  const buildPayload = () => {
    const price = parseReferencePrice() ?? 0;
    const normalizedImages = normalizeImages(images);
    return {
      name: name.trim(),
      brand_id: brandId ? Number.parseInt(brandId, 10) : undefined,
      category_id: categoryId ? Number.parseInt(categoryId, 10) : undefined,
      spec_id: specId ? Number.parseInt(specId, 10) : undefined,
      size: size.trim() || undefined,
      surface_finish: surfaceFinish.trim() || undefined,
      color_family: colorFamily.trim() || null,
      reference_price: price,
      remark: remark.trim() || null,
      recall_pin_sort_order: parseRecallPinSortOrder() ?? 9999,
      recall_pin_starts_at: recallPinStartsAt ? new Date(recallPinStartsAt).toISOString() : null,
      recall_pin_ends_at: recallPinEndsAt ? new Date(recallPinEndsAt).toISOString() : null,
      images: normalizedImages.map((img, idx) => ({
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
    if (['uploading', 'authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling', 'failed'].includes(imageUploadState)) {
      setError('图片上传中，请稍后保存');
      return;
    }
    if (['authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling', 'failed'].includes(videoUploadState)) {
      setError('视频上传中，请稍后保存');
      return;
    }
    setSubmitting(true);
    setError(null);
    if (saveMode === 'draft' && !name.trim()) {
      setError('商品名称不能为空');
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
      let successMessage = '';
      if (mode === 'create') {
        await createTileSku({ ...buildPayload(), save_mode: saveMode });
        successMessage = saveMode === 'draft' ? '草稿已保存' : 'SKU 创建成功，已保存为草稿';
      } else if (sku) {
        await updateTileSku(sku.id, buildPayload());
        successMessage = 'SKU 已更新';
      }
      for (const task of unboundMediaTasks.current.values()) task.markSaved?.();
      unboundMediaTasks.current.clear();
      videoTask.current = null; imageTask.current = null;
      onSuccess(successMessage);
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleImageUpload = async (file: File | undefined, retry = false) => {
    if (!file || submitting || isVideoUploading || isImageUploading) return;
    const epoch = ++imageEpoch.current;
    imageFile.current = file;
    setImageRetryable(true); setImageUploadProgress(0); setImageWarning(undefined);
    setImageUploadState('uploading');
    setImageUploadError(null);
    try {
      const result = await uploadTileImage(file, sku?.id, {
        task: retry ? imageTask.current ?? undefined : undefined,
        onTask: task => { imageTask.current = task; },
        onUpdate: value => {
          if (imageEpoch.current !== epoch) return;
          setImageUploadState(value.stage); setImageUploadProgress(value.progress); setImageWarning(value.warning);
          if (value.error) setImageUploadError(value.error);
          if (value.retryable !== undefined) setImageRetryable(value.retryable);
        },
      });
      if (imageEpoch.current !== epoch) return;
      if (imageTask.current) unboundMediaTasks.current.set(result.object_key, imageTask.current);
      setImages((prev) =>
        normalizeImages([
          ...prev,
          {
            previewFile: file,
            object_key: result.object_key,
            url: result.url,
            thumbnail_url: result.thumbnail_url,
            display_url: result.display_url,
            original_url: result.original_url,
            is_main: prev.length === 0,
            sort_order: prev.length,
          },
        ]),
      );
      setImageUploadState('uploaded');
    } catch (err) {
      if (imageEpoch.current !== epoch) return;
      if (err instanceof MediaUploadFailure) setImageRetryable(err.retryable);
      const message = getErrorMessage(err, '图片上传失败');
      setImageUploadState('failed');
      setImageUploadError(message);
    }
  };

  const handleVideoUpload = async (file: File | undefined, retry = false) => {
    if (!file || submitting || isImageUploading || ['authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling'].includes(videoUploadState)) return;
    const epoch = ++uploadEpoch.current;
    videoFile.current = file;
    setVideoUploadError(null);
    setVideoUploadState('authorizing');
    if (!retry) setVideoUploadProgress(0);
    try {
      const result = await uploadTileVideo(file, sku?.id, progress => {
        if (epoch !== uploadEpoch.current) return;
        const normalized = Math.min(99, Math.max(0, progress));
        setVideoUploadProgress(normalized);
        setVideoUploadState(normalized >= 99 ? 'saving' : 'transferring');
      }, {
        task: retry ? videoTask.current ?? undefined : undefined,
        onTask: task => { videoTask.current = task; },
        onUpdate: snapshot => {
          if (epoch !== uploadEpoch.current) return;
          setVideoUploadState(snapshot.stage);
          setVideoUploadProgress(snapshot.progress);
          setVideoUploadError(snapshot.error ?? null);
          setVideoRetryable(snapshot.retryable ?? true);
        },
      });
      if (epoch !== uploadEpoch.current) return;
      let previewUrl = result.url;
      if (typeof URL.createObjectURL === 'function') {
        previewUrl = URL.createObjectURL(file);
        localVideoUrls.current.add(previewUrl);
      }
      if (videoTask.current) unboundMediaTasks.current.set(result.object_key, videoTask.current);
      setVideos(prev => [...prev, {
        object_key: result.object_key, url: previewUrl, file_name: file.name,
        file_size_bytes: result.size ?? file.size, sort_order: prev.length,
      }]);
      setVideoUploadProgress(100);
      setVideoUploadState('uploaded');
      requestAnimationFrame(() => {
        const card = videoListRef.current?.lastElementChild;
        if (typeof card?.scrollIntoView === 'function') card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      });
    } catch (err) {
      if (epoch !== uploadEpoch.current) return;
      setVideoUploadState('failed');
      setVideoUploadError(err instanceof MediaUploadFailure ? err.message : getErrorMessage(err, '视频上传失败'));
      setVideoRetryable(err instanceof MediaUploadFailure ? err.retryable : true);
    }
  };

  const isVideoUploading = ['authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling'].includes(videoUploadState);
  const hasUnfinishedVideo = isVideoUploading || videoUploadState === 'failed';
  const isImageUploading = ['uploading', 'authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling'].includes(imageUploadState);
  const hasUnfinishedImage = isImageUploading || imageUploadState === 'failed';

  const cancelCurrentVideo = async () => {
    uploadEpoch.current++;
    setVideoUploadState('cancelling');
    try {
      await videoTask.current?.cancel();
      setVideoUploadState('cancelled');
      setVideoUploadError(null);
      setVideoRetryable(false);
    } catch {
      setVideoUploadState('failed');
      setVideoUploadError('取消未成功，请重试取消');
      setVideoRetryable(false);
    }
  };

  const requestClose = () => {
    if (submitting || (isImageUploading && !imageTask.current)) return;
    if (hasUnfinishedVideo || hasUnfinishedImage || unboundMediaTasks.current.size) setLeaveUploadPrompt(true);
    else onClose();
  };

  const discardUploadsAndClose = async () => {
    uploadEpoch.current++; imageEpoch.current++;
    setVideoUploadState('cancelling');
    try {
      const tasks = new Set(unboundMediaTasks.current.values());
      if (videoTask.current) tasks.add(videoTask.current);
      if (imageTask.current) tasks.add(imageTask.current);
      await Promise.all([...tasks].map(task => task.cancel()));
      unboundMediaTasks.current.clear(); videoTask.current = null; imageTask.current = null;
      onClose();
    } catch {
      setVideoUploadState('failed');
      setVideoUploadError('取消未成功，请重试后离开');
    }
  };

  const removeVideo = async (video: VideoDraft) => {
    if (submitting) return;
    try {
      await unboundMediaTasks.current.get(video.object_key)?.cancel();
      unboundMediaTasks.current.delete(video.object_key);
      setVideos(prev => prev.filter(item => item.object_key !== video.object_key));
      if (localVideoUrls.current.delete(video.url)) URL.revokeObjectURL(video.url);
    } catch {
      setVideoUploadError('移除未成功，请重试');
      setVideoUploadState('failed');
    }
  };

  const setMainImage = (index: number) => {
    if (submitting) return;
    setImages((prev) => normalizeImages(prev.map((img, i) => ({ ...img, is_main: i === index }))));
  };

  const removeImage = async (index: number) => {
    if (submitting) return;
    const image = images[index];
    try {
      const task = unboundMediaTasks.current.get(image.object_key);
      if (task) await task.cancel();
      unboundMediaTasks.current.delete(image.object_key);
      setImages(prev => normalizeImages(prev.filter(item => item.object_key !== image.object_key)));
    } catch { setImageUploadError('移除未成功，请重试'); setImageUploadState('failed'); }
  };

  const cancelCurrentImage = async () => {
    if (submitting) return;
    imageEpoch.current++; setImageUploadState('cancelling');
    try {
      await imageTask.current?.cancel();
      setImageUploadState('cancelled'); setImageUploadError(null);
    } catch { setImageUploadState('failed'); setImageUploadError('取消未成功，请重试取消'); }
    setImageRetryable(false);
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={event => { if (event.target === event.currentTarget) requestClose(); }}>
      <div
        className="sku-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="tile-sku-modal-title"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={event => { if (event.key === 'Escape') { event.stopPropagation(); requestClose(); } }}
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
          <button type="button" className="modal-close" aria-label="关闭" onClick={requestClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          {error ? <p className="admin-notice">{error}</p> : null}
          {leaveUploadPrompt ? (
            <div className="media-upload-status" role="alert" data-testid="upload-leave-prompt">
              <p>文件尚未保存至商品。离开会取消本次未保存的上传。</p>
              <button type="button" className="media-upload-status__action" onClick={() => setLeaveUploadPrompt(false)}>继续编辑</button>
              <button type="button" className="media-upload-status__action" disabled={videoUploadState === 'cancelling'} onClick={() => void discardUploadsAndClose()}>取消上传并离开</button>
            </div>
          ) : null}
          <div className="sku-form-grid">
            <div className="brand-form-item">
              <label>
                商品名称 <span className="req">*</span>
              </label>
              <input className="input" value={name} onChange={(e) => setName(e.target.value)} />
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
            <div className="brand-form-item">
              <label className="sku-label-with-help">
                <span>
                  排序 <span className="req">*</span>
                </span>
                <span
                  className="sku-help-icon"
                  title="默认 9999；只能填写正整数。数值越低，小程序普通商品列表和搜索 SKU 结果越靠前。"
                  aria-label="排序字段说明：默认 9999；只能填写正整数。数值越低，小程序普通商品列表和搜索 SKU 结果越靠前。"
                  role="img"
                >
                  <CircleHelp aria-hidden="true" size={14} strokeWidth={1.8} />
                </span>
              </label>
              <input
                className="input"
                type="number"
                step="1"
                min="1"
                value={recallPinSortOrder}
                aria-invalid={recallPinSortOrderError ? 'true' : undefined}
                aria-describedby={recallPinSortOrderError ? 'recall-pin-sort-order-error' : undefined}
                onChange={(e) => {
                  setRecallPinSortOrder(e.target.value);
                  setRecallPinSortOrderError(null);
                }}
              />
              {recallPinSortOrderError ? (
                <p id="recall-pin-sort-order-error" className="sku-field-error">
                  {recallPinSortOrderError}
                </p>
              ) : null}
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
              <label>表面工艺</label>
              <input
                className="input"
                value={surfaceFinish}
                onChange={(e) => setSurfaceFinish(e.target.value)}
              />
            </div>
            <p className="sku-section-label">运营配置</p>
            <div className="brand-form-item">
              <label>生效开始时间</label>
              <input
                className="input"
                type="datetime-local"
                value={recallPinStartsAt}
                onChange={(e) => setRecallPinStartsAt(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label>生效结束时间</label>
              <input
                className="input"
                type="datetime-local"
                value={recallPinEndsAt}
                onChange={(e) => setRecallPinEndsAt(e.target.value)}
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
                    <AuthorizedImage file={img.previewFile} reference={img.media_id && sku ? {resource_type: 'sku_image', resource_id: String(sku.id), media_id: img.media_id, variant: 'display'} : unboundMediaTasks.current.get(img.object_key)?.sessionId ? {resource_type: 'upload_session', resource_id: unboundMediaTasks.current.get(img.object_key)!.sessionId!, variant: 'display'} : undefined} src={img.display_url || img.thumbnail_url || img.url} alt="" />
                    {img.is_main ? <span className="sku-main-flag">主图</span> : null}
                    {!img.is_main ? (
                      <button
                        type="button"
                        className="sku-set-main"
                        disabled={submitting}
                        onClick={() => setMainImage(index)}
                      >
                        设为主图
                      </button>
                    ) : null}
                    <button
                      type="button"
                      className="sku-remove-image"
                      disabled={submitting}
                      aria-label={`移除图片 ${index + 1}`}
                      onClick={() => removeImage(index)}
                    >
                      移除
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  className={`sku-add-tile${isImageUploading ? ' disabled' : ''}`}
                  aria-disabled={isImageUploading || isVideoUploading}
                  disabled={isImageUploading || isVideoUploading}
                  onClick={() => imageInputRef.current?.click()}
                >
                  <span style={{ fontSize: 20 }}>＋</span>
                  {isImageUploading ? '上传中' : '继续添加图片'}
                </button>
              </div>
              {imageUploadState === 'uploading' ? <span className="sku-image-upload-status">图片上传中，请稍候</span> : (
                <MediaUploadStatus mediaKind="image" stage={imageUploadState} progress={imageUploadProgress}
                  fileName={imageUploadState === 'uploaded' ? undefined : imageFile.current?.name} error={imageUploadError}
                  onCancel={imageUploadState === 'idle' ? undefined : () => void cancelCurrentImage()}
                  onRetry={imageRetryable ? () => void handleImageUpload(imageFile.current, true) : undefined} />
              )}
              {imageWarning ? <p role="status" className="text-brand-gold">{imageWarning}</p> : null}
              <p className="sku-help">{imageUploadHint}</p>
              <input
                ref={imageInputRef}
                type="file"
                accept={imageAccept}
                hidden
                disabled={isImageUploading || isVideoUploading}
                onChange={(e) => {
                  const input = e.currentTarget;
                  void handleImageUpload(input.files?.[0]).finally(() => {
                    input.value = '';
                  });
                }}
              />
            </div>

            <p className="sku-section-label">商品视频</p>
            <div className="sku-form-full sku-video-section">
              <div className="sku-upload-grid sku-video-grid" ref={videoListRef}>
                {videos.map((vid) => (
                  <div key={vid.object_key} className="sku-video-card">
                    <div className="sku-video-player-wrap">
                      <AuthorizedVideo reference={vid.media_id && sku ? {resource_type: 'sku_video', resource_id: String(sku.id), media_id: vid.media_id, variant: 'original'} : unboundMediaTasks.current.get(vid.object_key)?.sessionId ? {resource_type: 'upload_session', resource_id: unboundMediaTasks.current.get(vid.object_key)!.sessionId!, variant: 'original'} : undefined}
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
                        disabled={submitting}
                        onClick={() => void removeVideo(vid)}
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
                <button
                  type="button"
                  className={`sku-add-tile${isVideoUploading ? ' disabled' : ''}`}
                  aria-disabled={isVideoUploading || isImageUploading}
                  disabled={isVideoUploading || isImageUploading}
                  onClick={() => videoInputRef.current?.click()}
                >
                  <span style={{ fontSize: 20 }}>＋</span>
                  {videoUploadState === 'saving' ? '保存中' : isVideoUploading ? '上传中' : '继续添加视频'}
                </button>
              </div>
              <MediaUploadStatus stage={videoUploadState} progress={videoUploadProgress}
                fileName={videoUploadState === 'uploaded' ? undefined : videoFile.current?.name} error={videoUploadError}
                onCancel={videoTask.current ? () => void cancelCurrentVideo() : undefined}
                onRetry={videoRetryable ? () => void handleVideoUpload(videoFile.current, true) : undefined} />
              <p className="sku-help">{videoUploadHint}</p>
              <input
                ref={videoInputRef}
                type="file"
                accept={videoAccept}
                hidden
                disabled={isVideoUploading || isImageUploading}
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
            onClick={requestClose}
            disabled={submitting || (isImageUploading && !imageTask.current)}
          >
            取消
          </button>
          {mode === 'create' ? (
            <>
              <button
                type="button"
                className="btn"
                disabled={submitting || hasUnfinishedImage || hasUnfinishedVideo}
                onClick={() => void handleSave('draft')}
              >
                保存草稿
              </button>
              <button
                type="button"
                className="btn primary"
                disabled={submitting || hasUnfinishedImage || hasUnfinishedVideo}
                onClick={() => void handleSave('create')}
              >
                创建 SKU
              </button>
            </>
          ) : (
            <button
              type="button"
              className="btn primary"
              disabled={submitting || hasUnfinishedImage || hasUnfinishedVideo}
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
