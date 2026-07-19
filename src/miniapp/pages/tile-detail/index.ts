import { request, track } from '../../services/api';

type MediaItem = {
  media_id: number;
  media_type: 'image' | 'video';
  url: string;
  preview_url?: string;
  cover_url?: string;
  sort_order: number;
  is_main: boolean;
};

type ProductCard = {
  product_id: number;
  product_name: string;
  sku_code: string;
  cover_image?: string;
  specification: string;
  category_name?: string;
  brand_name?: string;
  color_family?: string;
  price_display: string;
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

function pagePath(id: number, source: string): string {
  return `/pages/tile-detail/index?skuId=${id}&source=${source || 'direct'}`;
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
  return {
    ...product,
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
      { label: 'SKU 编码', value: product.sku_code },
      { label: '规格', value: product.specification || '—' },
      { label: '表面工艺', value: product.surface_finish || '—' },
      { label: '主色系', value: product.color_family || '—' },
      { label: '类目', value: product.category_name || '—' },
    ],
    remark: undefined,
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
}

Page({
  data: {
    id: 0,
    source: 'direct',
    clientId: '',
    loading: true,
    favoriteBusy: false,
    mediaIndex: 0,
    mediaPaused: false,
    mediaError: '',
    error: '',
    errorDetail: '',
    product: null as SkuDetail | null,
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query: Record<string, string>) {
    const id = Number(query.skuId || query.id || 0);
    const source = query.source || 'direct';
    const storedClientId = clientId();
    this.setData({ id, source, clientId: storedClientId });
    this.loadProduct(id, source, storedClientId);
  },

  onHide() {
    this.pauseVideo();
  },

  onUnload() {
    this.pauseVideo();
  },

  onShareAppMessage() {
    const product = this.data.product;
    if (product) {
      track('sku_share_click', {
        sku_id: product.product_id,
        page_path: pagePath(product.product_id, this.data.source),
      });
    }
    return {
      title: (product && product.share.title) || '菲尚特瓷砖',
      path: (product && product.share.path) || pagePath(this.data.id, 'share'),
      imageUrl: product && product.share.image_url,
    };
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
        this.setData({ product, loading: false, mediaIndex: 0, mediaPaused: false });
        track('sku_detail_view', {
          sku_id: product.product_id,
          page_path: pagePath(product.product_id, source),
          source,
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
    const current = String(event.currentTarget.dataset.url || '');
    const product = this.data.product;
    if (!product || !current) {
      return;
    }
    const urls = product.media
      .filter((item) => item.media_type === 'image')
      .map((item) => item.preview_url || item.url);
    wx.previewImage({ urls, current });
    track('sku_image_preview', {
      sku_id: product.product_id,
      page_path: pagePath(product.product_id, this.data.source),
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
    this.setData({ mediaPaused: false });
  },

  onMediaError(event: WechatMiniprogram.BaseEvent) {
    const mediaType = String(event.currentTarget.dataset.type || 'media');
    this.setData({ mediaError: mediaType === 'video' ? '视频暂时无法播放' : '图片加载失败，可稍后重试' });
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

  openBrand() {
    const product = this.data.product;
    if (!product) {
      return;
    }
    track('sku_brand_click', {
      sku_id: product.product_id,
      brand_id: product.brand.brand_id,
      page_path: pagePath(product.product_id, this.data.source),
    });
    wx.navigateTo({
      url: product.brand.brand_entry_path || `/pages/search/index?keyword=${encodeURIComponent(product.brand.brand_name)}`,
      fail: () => wx.navigateTo({ url: `/pages/search/index?keyword=${encodeURIComponent(product.brand.brand_name)}` }),
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
