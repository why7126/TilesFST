const { request, track } = require('../../services/api');

const FAVORITE_STORAGE_KEY = 'miniapp_favorite_skus_v1';

function pagePath(id, source) {
  return `/pages/tile-detail/index?skuId=${encodeURIComponent(String(id || 0))}&source=${encodeURIComponent(source || 'direct')}`;
}

function safeRouteParam(value) {
  if (value === undefined || value === null) return '';
  return String(value).slice(0, 80);
}

function safeText(value) {
  if (typeof value !== 'string') return '';
  const text = value.trim();
  return text && text !== 'null' && text !== 'undefined' ? text : '';
}

function skuShareTitle(product) {
  if (!product) return '菲尚特瓷砖';
  const title = safeText(product.share && product.share.title);
  if (title) return title;
  return [safeText(product.brand && product.brand.brand_name), safeText(product.product_name)]
    .filter(Boolean)
    .join(' ') || '菲尚特瓷砖';
}

function skuShareImage(product, fallback) {
  if (!product) return fallback;
  const mainImage = product.media.find((item) => item.media_type === 'image');
  return safeText(product.share && product.share.image_url)
    || safeText(product.cover_image)
    || safeText(mainImage && mainImage.preview_url)
    || safeText(mainImage && mainImage.url)
    || fallback;
}

function clientId() {
  const key = 'miniapp_client_id';
  const saved = wx.getStorageSync(key);
  if (saved) {
    return String(saved);
  }
  const generated = `miniapp-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
  wx.setStorageSync(key, generated);
  return generated;
}

function readLocalFavorites() {
  try {
    const value = wx.getStorageSync(FAVORITE_STORAGE_KEY);
    return Array.isArray(value) ? value.filter((item) => item && item.objectType === 'sku') : [];
  } catch (_error) {
    return [];
  }
}

function writeLocalFavorites(items) {
  try {
    wx.setStorageSync(FAVORITE_STORAGE_KEY, items);
  } catch (_error) {
    wx.showToast({ title: '本机收藏保存失败', icon: 'none' });
  }
}

function favoriteItemFromProduct(product) {
  const media = product.media || [];
  const mediaCover = media.find((item) => item.media_type === 'image');
  const brand = product.brand || {};
  const categoryPath = product.category_path || [];
  return {
    objectType: 'sku',
    objectId: product.product_id,
    product_id: product.product_id,
    sku_id: product.product_id,
    product_name: product.product_name,
    sku_code: product.sku_code,
    cover_image: product.cover_image || (mediaCover && (mediaCover.preview_url || mediaCover.url)) || '',
    specification: product.specification || '',
    brand_name: brand.brand_name || '',
    category_name: categoryPath.join(' / '),
    price_display: product.price_display || '暂无',
    status: 'available',
    favorited_at: Date.now(),
  };
}

function syncLocalFavorite(product, favorite) {
  const items = readLocalFavorites().filter((item) => item.objectId !== product.product_id);
  writeLocalFavorites(favorite ? [favoriteItemFromProduct(product), ...items] : items);
}

function legacyToSkuDetail(product) {
  const images = product.images || (product.cover_image ? [product.cover_image] : []);
  const media = images.map((url, index) => ({
    media_id: index + 1,
    media_type: 'image',
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
      { label: '类目', value: product.category_name || '—' },
      { label: '规格', value: product.specification || '—' },
      { label: '主色系', value: product.color_family || '—' },
      { label: '表面工艺', value: product.surface_finish || '—' },
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
    mediaError: '',
    error: '',
    errorDetail: '',
    product: null,
    imageFallback: '/assets/tile-placeholder.png',
  },

  onLoad(query) {
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
    const skuId = (product && product.product_id) || this.data.id;
    return {
      title: skuShareTitle(product),
      path: pagePath(skuId, 'share'),
      imageUrl: skuShareImage(product, this.data.imageFallback),
    };
  },

  onShareTimeline() {
    this.trackSkuShare('wechat_timeline');
    const product = this.data.product;
    const skuId = (product && product.product_id) || this.data.id;
    return {
      title: skuShareTitle(product),
      query: `skuId=${encodeURIComponent(String(skuId || 0))}&source=share`,
      imageUrl: skuShareImage(product, this.data.imageFallback),
    };
  },

  trackSkuShare(shareChannel) {
    const product = this.data.product;
    const skuId = (product && product.product_id) || this.data.id || 0;
    track('sku_share_click', {
      sku_id: skuId,
      page_path: pagePath(skuId, 'share'),
      share_channel: shareChannel,
    });
  },

  loadProduct(id, source = this.data.source, clientIdValue = this.data.clientId) {
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
    request(`/api/v1/miniapp/skus/${id}?client_id=${encodeURIComponent(clientIdValue)}`)
      .catch(() => request(`/api/v1/miniapp/products/${id}`).then(legacyToSkuDetail))
      .then((product) => {
        this.setData({ product, loading: false, mediaIndex: 0, mediaPaused: false });
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
      .catch((error) => {
        const detail = error && error.attempts
          ? error.attempts.map((item) => item.message || item.errMsg).filter(Boolean).join('；')
          : error && error.message;
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

  onMediaChange(event) {
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

  previewImage(event) {
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

  onMediaError(event) {
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

  openRecommend(event) {
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
