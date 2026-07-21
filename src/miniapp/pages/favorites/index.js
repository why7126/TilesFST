const { request, track } = require('../../services/api');

const FAVORITE_STORAGE_KEY = 'miniapp_favorite_skus_v1';
const PAGE_SIZE = 10;
const NAV_LOCK_MS = 800;

function nowRequestId() {
  return `fav-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function normalizeFavoriteItem(item) {
  if (!item || item.objectType !== 'sku') {
    return null;
  }
  const id = Number(item.objectId || item.sku_id || item.product_id || 0);
  if (!id) {
    return null;
  }
  return {
    objectType: 'sku',
    objectId: id,
    product_id: Number(item.product_id || id),
    sku_id: Number(item.sku_id || id),
    product_name: item.product_name || '未命名商品',
    sku_code: item.sku_code || '',
    cover_image: item.cover_image || '',
    specification: item.specification || '',
    brand_name: item.brand_name || '',
    category_name: item.category_name || '',
    price_display: item.price_display || '暂无',
    status: item.status || 'available',
    favorited_at: Number(item.favorited_at || 0),
  };
}

function readFavorites() {
  try {
    const value = wx.getStorageSync(FAVORITE_STORAGE_KEY);
    if (!Array.isArray(value)) {
      return [];
    }
    return value.map(normalizeFavoriteItem).filter((item) => Boolean(item));
  } catch (_error) {
    return [];
  }
}

function writeFavorites(items) {
  try {
    wx.setStorageSync(FAVORITE_STORAGE_KEY, items);
    return true;
  } catch (_error) {
    return false;
  }
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

Page({
  data: {
    status: 'loading',
    items: [],
    visibleItems: [],
    total: 0,
    page: 1,
    pageSize: PAGE_SIZE,
    hasMore: false,
    loadingMore: false,
    loadMoreError: '',
    requestId: '',
    navigating: false,
    removingId: 0,
    imageFallback: '/assets/tile-placeholder.png',
    skeletons: [1, 2, 3],
  },

  onLoad() {
    this.setCurrentTab();
    this.refreshFavorites('load');
  },

  onShow() {
    this.setCurrentTab();
    this.refreshFavorites('show');
  },

  onPullDownRefresh() {
    this.refreshFavorites('refresh');
    wx.stopPullDownRefresh();
  },

  onReachBottom() {
    this.loadMore();
  },

  setCurrentTab() {
    const tabBar = this.getTabBar && this.getTabBar();
    if (tabBar) {
      tabBar.setData({ selected: 3 });
    }
  },

  refreshFavorites(sourcePage) {
    const requestId = nowRequestId();
    this.setData({ status: 'loading', requestId, loadMoreError: '' });
    try {
      const items = readFavorites().sort((a, b) => b.favorited_at - a.favorited_at);
      const visibleItems = items.slice(0, this.data.pageSize);
      const status = items.length ? 'ready' : 'empty';
      this.setData({
        status,
        items,
        visibleItems,
        total: items.length,
        page: 1,
        hasMore: items.length > visibleItems.length,
        loadingMore: false,
      });
      track('favorite_list_page_view', {
        page_path: '/pages/favorites/index',
        terminal: 'miniapp',
        sourcePage,
        hasLogin: false,
        resultCount: items.length,
        requestId,
      });
    } catch (_error) {
      this.setData({ status: 'error', loadingMore: false });
      track('favorite_list_load_failed', {
        page_path: '/pages/favorites/index',
        terminal: 'miniapp',
        sourcePage,
        errorCode: 'storage_read_failed',
        requestId,
      });
    }
  },

  loadMore() {
    if (!this.data.hasMore || this.data.loadingMore) {
      return;
    }
    this.setData({ loadingMore: true, loadMoreError: '' });
    try {
      const nextPage = this.data.page + 1;
      const nextVisible = this.data.items.slice(0, nextPage * this.data.pageSize);
      this.setData({
        page: nextPage,
        visibleItems: nextVisible,
        hasMore: this.data.items.length > nextVisible.length,
        loadingMore: false,
      });
    } catch (_error) {
      this.setData({ loadingMore: false, loadMoreError: '加载更多失败，点击重试' });
      track('favorite_list_load_failed', {
        page_path: '/pages/favorites/index',
        terminal: 'miniapp',
        errorCode: 'load_more_failed',
        requestId: this.data.requestId,
      });
    }
  },

  retryLoad() {
    this.refreshFavorites('retry');
  },

  retryLoadMore() {
    this.loadMore();
  },

  openExplore() {
    track('favorite_list_empty_action_click', {
      page_path: '/pages/favorites/index',
      terminal: 'miniapp',
      target: 'product_list',
      requestId: this.data.requestId,
    });
    wx.navigateTo({ url: '/pages/product-list/index?sourcePage=favorites' });
  },

  openItem(event) {
    const id = Number(event.currentTarget.dataset.id || 0);
    const index = Number(event.currentTarget.dataset.index || 0);
    const item = this.data.visibleItems[index];
    if (!id || !item || item.status !== 'available') {
      wx.showToast({ title: '收藏内容暂不可查看', icon: 'none' });
      return;
    }
    if (this.data.navigating) {
      return;
    }
    this.setData({ navigating: true });
    track('favorite_list_item_click', {
      page_path: '/pages/favorites/index',
      terminal: 'miniapp',
      objectType: item.objectType,
      objectId: id,
      index,
      sourcePage: 'favorites',
      hasLogin: false,
      resultCount: this.data.total,
      requestId: this.data.requestId,
    });
    wx.navigateTo({
      url: `/pages/tile-detail/index?skuId=${id}&source=favorites&sourcePage=favorites&listContext=${encodeURIComponent('我的收藏')}&index=${index}&requestId=${encodeURIComponent(this.data.requestId)}`,
      fail: () => wx.showToast({ title: '收藏内容打开失败，请重试', icon: 'none' }),
      complete: () => {
        setTimeout(() => this.setData({ navigating: false }), NAV_LOCK_MS);
      },
    });
  },

  removeItem(event) {
    const id = Number(event.currentTarget.dataset.id || 0);
    if (!id || this.data.removingId) {
      return;
    }
    const previous = this.data.items;
    const nextItems = previous.filter((item) => item.objectId !== id);
    this.setData({ removingId: id });
    request(`/api/v1/miniapp/skus/${id}/favorite`, {
      method: 'PUT',
      data: {
        client_id: clientId(),
        favorite: false,
      },
    })
      .then(() => {
        if (!writeFavorites(nextItems)) {
          throw new Error('storage_write_failed');
        }
        const nextVisible = nextItems.slice(0, this.data.page * this.data.pageSize);
        this.setData({
          items: nextItems,
          visibleItems: nextVisible,
          total: nextItems.length,
          status: nextItems.length ? 'ready' : 'empty',
          hasMore: nextItems.length > nextVisible.length,
          removingId: 0,
        });
        wx.showToast({ title: '已取消收藏', icon: 'success' });
        track('favorite_list_remove', {
          page_path: '/pages/favorites/index',
          terminal: 'miniapp',
          objectType: 'sku',
          objectId: id,
          sourcePage: 'favorites',
          hasLogin: false,
          resultCount: nextItems.length,
          requestId: this.data.requestId,
        });
      })
      .catch(() => {
        this.setData({ removingId: 0 });
        wx.showToast({ title: '取消收藏失败，请重试', icon: 'none' });
      });
  },

  onImageError(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`visibleItems[${index}].cover_image`]: this.data.imageFallback });
  },
});
