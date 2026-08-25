import { request, track } from '../../services/api';

type MediaItem = {
  media_id: number;
  media_type: 'image' | 'video';
  url: string;
  preview_url?: string;
  thumbnail_url?: string;
  display_url?: string;
  original_url?: string;
  cover_url?: string;
  sort_order: number;
  is_main: boolean;
};

type ProductCard = {
  product_id: number;
  product_name: string;
  sku_code: string;
  cover_image?: string;
  thumbnail_url?: string;
  display_url?: string;
  original_url?: string;
  specification: string;
  category_name?: string;
  brand_name?: string;
  color_family?: string;
  price_display: string;
  is_recall_pinned?: boolean;
};

type LegacyProductDetail = ProductCard & {
  images?: string[];
  videos?: string[];
  surface_finish?: string;
  share_title?: string;
};

type SkuDetail = ProductCard & {
  brand: {
    brand_id: number;
    brand_name: string;
    brand_short_name?: string;
    brand_logo_url?: string;
    brand_logo_thumbnail_url?: string;
    brand_entry_path?: string;
    available: boolean;
  };
  media: MediaItem[];
  image_count: number;
  video_count: number;
  category_path: string[];
  parameters: Array<{ label: string; value: string }>;
  remark?: string;
  surface_finish?: string;
  favorite: boolean;
  same_series_recommendations: ProductCard[];
  same_brand_recommendations: ProductCard[];
  share: {
    title: string;
    path: string;
    image_url?: string;
    summary: string;
  };
};

const FAVORITE_STORAGE_KEY = 'miniapp_favorite_skus_v1';

type FavoriteSnapshot = {
  objectType: 'sku';
  objectId: number;
  product_id: number;
  sku_id: number;
  product_name: string;
  sku_code: string;
  cover_image?: string;
  specification: string;
  brand_name?: string;
  category_name?: string;
  price_display: string;
  status: 'available';
  favorited_at: number;
};

function pagePath(id: number, source: string): string {
  return `/pages/tile-detail/index?skuId=${encodeURIComponent(String(id || 0))}&source=${encodeURIComponent(source || 'direct')}`;
}

function safeRouteParam(value: unknown): string {
  if (value === undefined || value === null) return '';
  return String(value).slice(0, 80);
}

function safeText(value: unknown): string {
  if (typeof value !== 'string') return '';
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : '';
}

function normalizeRemark(value: unknown): string | undefined {
  const text = safeText(value);
  return text || undefined;
}

function normalizeSkuDetail(product: SkuDetail): SkuDetail {
  const remark = normalizeRemark(product.remark);
  const parameters = (product.parameters || []).filter((item) => item.label !== '备注说明');
  return {
    ...product,
    cover_image: product.thumbnail_url || product.cover_image,
    media: (product.media || []).map((item) => item.media_type === 'image' ? {
      ...item,
      display_url: item.display_url || item.thumbnail_url,
      preview_url: item.original_url || item.preview_url || item.url,
    } : item),
    remark,
    parameters: remark ? [...parameters, { label: '备注说明', value: remark }] : parameters,
  };
}

function previewUrlForMedia(item: MediaItem): string {
  return item.original_url || item.preview_url || item.url;
}

function skuShareTitle(product: SkuDetail | null): string {
  if (!product) return '菲尚特瓷砖';
  return safeText(product.share?.title) || [safeText(product.brand?.brand_name), safeText(product.product_name)]
    .filter(Boolean)
    .join(' ') || '菲尚特瓷砖';
}

function skuShareImage(product: SkuDetail | null, fallback: string): string {
  if (!product) return fallback;
  const mainImage = product.media.find((item) => item.media_type === 'image');
  return safeText(product.share?.image_url)
    || safeText(product.display_url)
    || safeText(product.thumbnail_url)
    || safeText(mainImage?.display_url)
    || safeText(mainImage?.thumbnail_url)
    || fallback;
}

function clientId(): string {
  const key = 'miniapp_client_id';
  const saved = wx.getStorageSync(key);
  if (saved) {
    return String(saved);
  }
  const generated = `miniapp-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
  wx.setStorageSync(key, generated);
  return generated;
}

function readLocalFavorites(): FavoriteSnapshot[] {
  try {
    const value = wx.getStorageSync(FAVORITE_STORAGE_KEY);
    return Array.isArray(value) ? value.filter((item) => item && item.objectType === 'sku') : [];
  } catch (_error) {
    return [];
  }
}

function writeLocalFavorites(items: FavoriteSnapshot[]): void {
  try {
    wx.setStorageSync(FAVORITE_STORAGE_KEY, items);
  } catch (_error) {
    wx.showToast({ title: '本机收藏保存失败', icon: 'none' });
  }
}

function favoriteItemFromProduct(product: SkuDetail): FavoriteSnapshot {
  const mediaCover = product.media.find((item) => item.media_type === 'image');
  return {
    objectType: 'sku',
    objectId: product.product_id,
    product_id: product.product_id,
    sku_id: product.product_id,
    product_name: product.product_name,
    sku_code: product.sku_code,
    cover_image: product.thumbnail_url || product.display_url || mediaCover?.thumbnail_url || mediaCover?.display_url || '',
    specification: product.specification || '',
    brand_name: product.brand?.brand_name || '',
    category_name: product.category_path.join(' / '),
    price_display: product.price_display || '暂无',
    status: 'available',
    favorited_at: Date.now(),
  };
}

function syncLocalFavorite(product: SkuDetail, favorite: boolean): void {
  const items = readLocalFavorites().filter((item) => item.objectId !== product.product_id);
  writeLocalFavorites(favorite ? [favoriteItemFromProduct(product), ...items] : items);
}

function legacyToSkuDetail(product: LegacyProductDetail): SkuDetail {
  const images = product.images || (product.cover_image ? [product.cover_image] : []);
  const media = images.map((url, index) => ({
    media_id: index + 1,
    media_type: 'image' as const,
    url,
    preview_url: url,
    sort_order: index,
    is_main: index === 0,
  }));
  (product.videos || []).forEach((url, index) => {
    media.push({
      media_id: 1000 + index,
      media_type: 'video',
      url,
      sort_order: index,
      is_main: false,
    });
  });
  const detail: SkuDetail = {
    ...product,
    thumbnail_url: product.cover_image,
    display_url: product.cover_image,
    original_url: product.cover_image,
    brand: {
      brand_id: 0,
      brand_name: product.brand_name || '菲尚特',
      available: false,
    },
    media,
    image_count: images.length,
    video_count: (product.videos || []).length,
    category_path: product.category_name ? [product.category_name] : [],
    parameters: [
      { label: '类目', value: product.category_name || '—' },
      { label: '规格', value: product.specification || '—' },
      { label: '主色系', value: product.color_family || '—' },
      { label: '表面工艺', value: product.surface_finish || '—' },
    ],
    remark: normalizeRemark((product as LegacyProductDetail & { remark?: unknown }).remark),
    surface_finish: product.surface_finish,
    favorite: false,
    same_series_recommendations: [],
    same_brand_recommendations: [],
    share: {
      title: product.share_title || `${product.brand_name || '菲尚特'} ${product.product_name}`,
      path: `/pages/tile-detail/index?skuId=${product.product_id}&source=share`,
      image_url: product.cover_image || images[0],
      summary: `${product.brand_name || '菲尚特'} · ${product.price_display}`,
    },
  };
  return normalizeSkuDetail(detail);
}

Page({
  data: {
    id: 0,
    source: 'direct',
    routeContext: {
      sourcePage: '',
      sourceModule: '',
      categoryId: '',
      brandId: '',
      keyword: '',
      listContext: '',
      index: '',
      requestId: '',
    },
    clientId: '',
    loading: true,
    favoriteBusy: false,
    mediaIndex: 0,
    mediaPaused: false,
    fullscreenVideoId: 0,
    fullscreenSwitching: false,
    mediaError: '',
    error: '',
    errorDetail: '',
    product: null as SkuDetail | null,
    imageFallback: '/assets/logos/product-logo.png',
  },

  onLoad(query: Record<string, string>) {
    const id = Number(query.skuId || query.id || 0);
    const source = safeRouteParam(query.source || query.sourcePage || 'direct') || 'direct';
    const routeContext = {
      sourcePage: safeRouteParam(query.sourcePage || source),
      sourceModule: safeRouteParam(query.sourceModule),
      categoryId: safeRouteParam(query.categoryId),
      brandId: safeRouteParam(query.brandId),
      keyword: safeRouteParam(query.keyword),
      listContext: safeRouteParam(query.listContext),
      index: safeRouteParam(query.index),
      requestId: safeRouteParam(query.requestId),
    };
    const storedClientId = clientId();
    this.setData({ id, source, routeContext, clientId: storedClientId });
    this.loadProduct(id, source, storedClientId);
  },

  onHide() {
    this.pauseVideo();
  },

  onUnload() {
    this.pauseVideo();
  },

  onShareAppMessage() {
    this.trackSkuShare('wechat_friend');
    const product = this.data.product;
    const skuId = product?.product_id || this.data.id;
    return {
      title: skuShareTitle(product),
      path: pagePath(skuId, 'share'),
      imageUrl: skuShareImage(product, this.data.imageFallback),
    };
  },

  onShareTimeline() {
    this.trackSkuShare('wechat_timeline');
    const product = this.data.product;
    const skuId = product?.product_id || this.data.id;
    return {
      title: skuShareTitle(product),
      query: `skuId=${encodeURIComponent(String(skuId || 0))}&source=share`,
      imageUrl: skuShareImage(product, this.data.imageFallback),
    };
  },

  trackSkuShare(shareChannel: 'wechat_friend' | 'wechat_timeline') {
    const product = this.data.product;
    const skuId = product?.product_id || this.data.id || 0;
    track('sku_share_click', {
      sku_id: skuId,
      page_path: pagePath(skuId, 'share'),
      share_channel: shareChannel,
    });
  },

  loadProduct(id: number, source: string = this.data.source, clientIdValue: string = this.data.clientId) {
    if (!id) {
      this.setData({ loading: false, error: '商品暂不可查看', errorDetail: '缺少有效 SKU ID' });
      track('sku_load_error', {
        sku_id: 0,
        page_path: '/pages/tile-detail/index',
        error_code: 'missing_sku_id',
        stage: 'route',
      });
      return;
    }
    this.setData({ loading: true, error: '', errorDetail: '', mediaError: '' });
    request<SkuDetail>(`/api/v1/miniapp/skus/${id}?client_id=${encodeURIComponent(clientIdValue)}`)
      .catch(() => request<LegacyProductDetail>(`/api/v1/miniapp/products/${id}`).then(legacyToSkuDetail))
      .then((product) => {
        this.setData({ product: normalizeSkuDetail(product), loading: false, mediaIndex: 0, mediaPaused: false });
        if (product.favorite) {
          syncLocalFavorite(product, true);
        }
        track('sku_detail_view', {
          sku_id: product.product_id,
          page_path: pagePath(product.product_id, source),
          source,
          ...this.data.routeContext,
        });
      })
      .catch((error: Error & { attempts?: Array<{ message?: string; errMsg?: string }> }) => {
        const detail = error.attempts
          ? error.attempts.map((item) => item.message || item.errMsg).filter(Boolean).join('；')
          : error.message;
        this.setData({ loading: false, error: '商品暂不可查看', errorDetail: detail || '网络异常' });
        track('sku_load_error', {
          sku_id: id,
          page_path: pagePath(id, source),
          error_code: 'request_failed',
          stage: 'detail',
          ...this.data.routeContext,
        });
      });
  },

  retryLoad() {
    this.loadProduct(this.data.id);
  },

  goBack() {
    const pages = typeof getCurrentPages === 'function' ? getCurrentPages() : [];
    if (pages.length > 1) {
      wx.navigateBack({
        fail: () => wx.switchTab({ url: '/pages/index/index' }),
      });
      return;
    }
    wx.switchTab({
      url: '/pages/index/index',
      fail: () => wx.reLaunch({ url: '/pages/index/index' }),
    });
  },

  onMediaChange(event: WechatMiniprogram.SwiperChange) {
    const current = Number(event.detail.current || 0);
    const product = this.data.product;
    const media = product && product.media[current];
    this.pauseVideo();
    this.setData({ mediaIndex: current, mediaPaused: false });
    if (product && media) {
      track('sku_media_swipe', {
        sku_id: product.product_id,
        page_path: pagePath(product.product_id, this.data.source),
        media_type: media.media_type,
        media_index: current,
      });
    }
  },

  previewImage(event: WechatMiniprogram.BaseEvent) {
    const product = this.data.product;
    if (!product) {
      return;
    }
    const datasetMediaIndex = event.currentTarget.dataset.mediaIndex;
    const mediaIndex = Number(
      datasetMediaIndex !== undefined && datasetMediaIndex !== null
        ? datasetMediaIndex
        : this.data.mediaIndex || 0,
    );
    const imageMedia = product.media
      .map((item, index) => ({ item, index, url: previewUrlForMedia(item) }))
      .filter((entry) => entry.item.media_type === 'image' && entry.url);
    const urls = imageMedia.map((entry) => entry.url);
    const matched = imageMedia.find((entry) => entry.index === mediaIndex);
    const current = matched?.url || urls[0];
    if (!current || !urls.length) {
      return;
    }
    wx.getImageInfo({
      src: current,
      complete: () => {
        wx.previewImage({ urls, current });
        track('sku_image_preview', {
          sku_id: product.product_id,
          page_path: pagePath(product.product_id, this.data.source),
        });
      },
    });
  },

  onVideoPlay() {
    const product = this.data.product;
    this.setData({ mediaPaused: true });
    if (product) {
      track('sku_video_play', {
        sku_id: product.product_id,
        page_path: pagePath(product.product_id, this.data.source),
      });
    }
  },

  openVideoFullscreen(event: WechatMiniprogram.BaseEvent) {
    const mediaId = Number(event.currentTarget.dataset.id || 0);
    const product = this.data.product;
    if (!product || !mediaId) {
      wx.showToast({ title: '视频暂时无法全屏播放', icon: 'none' });
      return;
    }
    const activeVideo = product.media.find((item) => item.media_id === mediaId && item.media_type === 'video');
    if (!activeVideo?.url) {
      wx.showToast({ title: '视频暂时无法全屏播放', icon: 'none' });
      return;
    }
    const videoContext = wx.createVideoContext(`sku-video-${mediaId}`, this);
    this.setData({
      fullscreenVideoId: mediaId,
      fullscreenSwitching: true,
      mediaPaused: true,
      mediaError: '正在进入全屏播放…',
    });
    track('sku_video_play', {
      sku_id: product.product_id,
      media_id: mediaId,
      page_path: pagePath(product.product_id, this.data.source),
      action: 'fullscreen_context',
    });
    videoContext.requestFullScreen({
      direction: 0,
      success: () => {
        this.setData({ mediaError: '' });
      },
      fail: (error) => {
        this.setData({ fullscreenSwitching: false, fullscreenVideoId: 0, mediaError: '全屏播放暂不可用，请在视频控制条中重试' });
        wx.showToast({ title: '全屏播放暂不可用', icon: 'none' });
        track('sku_load_error', {
          sku_id: product.product_id,
          page_path: pagePath(product.product_id, this.data.source),
          error_code: 'video_fullscreen_failed',
          stage: 'fullscreen_context',
          media_id: mediaId,
          url_scheme: activeVideo.url.startsWith('https://') ? 'https' : activeVideo.url.startsWith('http://') ? 'http' : 'relative',
          url_ext: activeVideo.url.split('?')[0].split('.').pop() || '',
          err_msg: String(error.errMsg || '').slice(0, 120),
        });
      },
    });
  },

  onVideoFullscreenChange(event: WechatMiniprogram.BaseEvent) {
    const mediaId = Number(event.currentTarget.dataset.id || 0);
    const fullScreen = Boolean((event.detail as { fullScreen?: boolean }).fullScreen);
    if (fullScreen) {
      this.setData({ fullscreenVideoId: mediaId, fullscreenSwitching: false, mediaPaused: true, mediaError: '' });
      return;
    }
    if (this.data.fullscreenVideoId === mediaId) {
      this.setData({ fullscreenVideoId: 0, fullscreenSwitching: false, mediaError: '' });
    }
  },

  onVideoWaiting(event: WechatMiniprogram.BaseEvent) {
    const mediaId = Number(event.currentTarget.dataset.id || 0);
    if (this.data.fullscreenSwitching && this.data.fullscreenVideoId === mediaId) {
      this.setData({ mediaError: '全屏切换中，视频正在恢复播放…' });
    }
  },

  pauseVideo() {
    const product = this.data.product;
    if (!product) {
      return;
    }
    product.media.forEach((item) => {
      if (item.media_type === 'video') {
        wx.createVideoContext(`sku-video-${item.media_id}`, this).pause();
      }
    });
    this.setData({ mediaPaused: false, fullscreenVideoId: 0, fullscreenSwitching: false });
  },

  onMediaError(event: WechatMiniprogram.BaseEvent) {
    const mediaType = String(event.currentTarget.dataset.type || 'media');
    this.setData({
      mediaError: mediaType === 'video' ? '视频暂时无法播放' : '图片加载失败，可稍后重试',
    });
  },

  toggleFavorite() {
    const product = this.data.product;
    if (!product || this.data.favoriteBusy) {
      return;
    }
    const nextFavorite = !product.favorite;
    const previous = product.favorite;
    this.setData({ favoriteBusy: true, 'product.favorite': nextFavorite });
    request(`/api/v1/miniapp/skus/${product.product_id}/favorite`, {
      method: 'PUT',
      data: {
        client_id: this.data.clientId,
        favorite: nextFavorite,
      },
    })
      .then(() => {
        this.setData({ favoriteBusy: false });
        syncLocalFavorite(product, nextFavorite);
        wx.showToast({ title: nextFavorite ? '已收藏' : '已取消', icon: 'success' });
        track(nextFavorite ? 'sku_favorite' : 'sku_unfavorite', {
          sku_id: product.product_id,
          page_path: pagePath(product.product_id, this.data.source),
        });
      })
      .catch(() => {
        this.setData({ favoriteBusy: false, 'product.favorite': previous });
        wx.showToast({ title: '收藏状态未保存', icon: 'none' });
      });
  },

  openRecommend(event: WechatMiniprogram.BaseEvent) {
    const product = this.data.product;
    const targetId = Number(event.currentTarget.dataset.id || 0);
    const recommendType = String(event.currentTarget.dataset.type || 'same_brand');
    if (!product || !targetId) {
      return;
    }
    track('sku_recommend_click', {
      sku_id: product.product_id,
      target_sku_id: targetId,
      recommend_type: recommendType,
      page_path: pagePath(product.product_id, this.data.source),
    });
    wx.pageScrollTo({ scrollTop: 0, duration: 0 });
    wx.navigateTo({ url: `/pages/tile-detail/index?skuId=${targetId}&source=${recommendType}` });
  },
});
