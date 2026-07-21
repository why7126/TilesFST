const { request, track } = require('../../services/api');

const PRODUCT_PAGE_SIZE = 10;

function requestId() {
  return `brand-detail-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function titleText(brand) {
  return (brand && brand.brand_name) || '品牌主页';
}

function fileKindFromUrl(url) {
  const cleanUrl = String(url || '').split('?')[0].toLowerCase();
  if (!cleanUrl) return 'unknown';
  if (cleanUrl.endsWith('.pdf')) return 'pdf';
  if (/\.(png|jpe?g|webp|gif)$/.test(cleanUrl)) return 'image';
  return 'unknown';
}

function normalizeCertificate(item) {
  return {
    ...item,
    certificate_type_label: item.certificate_type_label || item.certificate_type || '证书',
    file_kind: item.file_kind || fileKindFromUrl(item.file_url),
  };
}

Page({
  data: {
    brandId: 0,
    sourcePage: 'direct',
    title: '品牌主页',
    brand: null,
    activeTab: 'products',
    loading: true,
    error: '',
    requestId: '',
    imageFailed: false,
    productPage: 1,
    productPageSize: PRODUCT_PAGE_SIZE,
    productTotal: 0,
    products: [],
    productsLoading: false,
    productsError: '',
    productsHasMore: true,
    productsLoadMoreError: '',
    certificates: [],
    certificatesLoading: false,
    certificatesLoaded: false,
    certificatesError: '',
    imageFallback: '/assets/tile-placeholder.png',
    skeletons: [1, 2, 3, 4],
  },

  onLoad(query) {
    const brandId = Number(query.brandId || query.brand_id || 0);
    this.setData({
      brandId,
      sourcePage: query.sourcePage || query.source || 'direct',
      requestId: requestId(),
    });
    this.loadBrand();
  },

  onPullDownRefresh() {
    this.setData({ requestId: requestId() });
    this.loadBrand();
  },

  onReachBottom() {
    if (this.data.activeTab === 'products') {
      this.loadProducts({ reset: false, eventName: 'brand_products_load_more' });
    }
  },

  onShareAppMessage() {
    return {
      title: (this.data.brand && this.data.brand.brand_name) || '品牌主页',
      path: `/pages/brand-detail/index?brandId=${this.data.brandId}&source=share`,
    };
  },

  loadBrand() {
    if (!this.data.brandId) {
      this.setData({ loading: false, error: '品牌参数无效，可返回品牌馆重新进入' });
      return;
    }
    this.setData({ loading: true, error: '', imageFailed: false });
    request(`/api/v1/miniapp/brands/${this.data.brandId}`)
      .then((brand) => {
        this.setData({
          brand,
          title: titleText(brand),
          loading: false,
        });
        this.trackDetailEvent('brand_detail_view', {});
        this.loadProducts({ reset: true });
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        this.setData({ loading: false, error: '品牌暂不可查看，请返回品牌馆重试' });
        this.trackDetailEvent('brand_detail_load_failed', {});
        wx.stopPullDownRefresh();
      });
  },

  switchTab(event) {
    const tab = String(event.currentTarget.dataset.tab || 'products');
    if (tab === this.data.activeTab) return;
    this.setData({ activeTab: tab });
    this.trackDetailEvent('brand_detail_tab_click', { tab });
    if (tab === 'certificates' && !this.data.certificatesLoaded) {
      this.loadCertificates();
    }
  },

  loadProducts(options) {
    if (this.data.productsLoading) return;
    if (!options.reset && !this.data.productsHasMore) return;
    const nextPage = options.reset ? 1 : this.data.productPage + 1;
    this.setData({
      productsLoading: true,
      productsError: '',
      productsLoadMoreError: '',
      ...(options.reset ? { products: [], productPage: 1, productsHasMore: true } : {}),
    });
    request(`/api/v1/miniapp/products?brandId=${this.data.brandId}&page=${nextPage}&pageSize=${this.data.productPageSize}`)
      .then((data) => {
        const incoming = data.items || [];
        const merged = options.reset ? incoming : this.mergeProducts(this.data.products, incoming);
        this.setData({
          products: merged,
          productTotal: data.total || merged.length,
          productPage: data.page || nextPage,
          productPageSize: data.page_size || this.data.productPageSize,
          productsHasMore: Boolean(data.has_more),
          productsLoading: false,
        });
        this.trackDetailEvent(options.eventName || 'brand_products_load', {
          tab: 'products',
          page: nextPage,
          pageSize: this.data.productPageSize,
          resultCount: incoming.length,
        });
      })
      .catch(() => {
        this.setData(
          options.reset
            ? { productsError: '该品牌商品加载失败，请重试', productsLoading: false }
            : { productsLoadMoreError: '加载更多失败，点击重试', productsLoading: false },
        );
        this.trackDetailEvent('brand_products_load_failed', { tab: 'products', page: nextPage });
      });
  },

  loadCertificates() {
    this.setData({ certificatesLoading: true, certificatesError: '' });
    request(`/api/v1/miniapp/brands/${this.data.brandId}/certificates`)
      .then((data) => {
        this.setData({
          certificates: (data.items || []).map(normalizeCertificate),
          certificatesLoaded: true,
          certificatesLoading: false,
        });
        this.trackDetailEvent('brand_certificates_load', {
          tab: 'certificates',
          resultCount: data.total || 0,
        });
      })
      .catch(() => {
        this.setData({ certificatesLoading: false, certificatesError: '该品牌证书加载失败，请重试' });
        this.trackDetailEvent('brand_certificates_load_failed', { tab: 'certificates' });
      });
  },

  mergeProducts(current, incoming) {
    const seen = new Set();
    const result = [];
    current.concat(incoming).forEach((item) => {
      if (!item || seen.has(item.product_id)) return;
      seen.add(item.product_id);
      result.push(item);
    });
    return result;
  },

  retryBrand() {
    this.loadBrand();
  },

  retryProducts() {
    this.loadProducts({ reset: true });
  },

  retryProductsMore() {
    this.loadProducts({ reset: false, eventName: 'brand_products_load_more' });
  },

  retryCertificates() {
    this.loadCertificates();
  },

  onBrandImageError() {
    this.setData({ imageFailed: true });
  },

  previewCertificate(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    const item = this.data.certificates[index];
    if (!item || !item.file_url) return;
    this.trackDetailEvent('brand_certificate_click', {
      tab: 'certificates',
      certificateId: item.certificate_id,
      index,
    });
    if (item.file_kind === 'pdf') {
      wx.downloadFile({
        url: item.file_url,
        success: (result) => {
          if (result.statusCode >= 200 && result.statusCode < 300) {
            wx.openDocument({
              filePath: result.tempFilePath,
              fileType: 'pdf',
              fail: () => this.copyCertificateUrl(item.file_url),
            });
            return;
          }
          this.copyCertificateUrl(item.file_url);
        },
        fail: () => this.copyCertificateUrl(item.file_url),
      });
      return;
    }
    if (item.file_kind === 'unknown') {
      wx.showToast({ title: '证书文件暂不可预览', icon: 'none' });
      return;
    }
    wx.previewImage({
      current: item.file_url,
      urls: this.data.certificates
        .filter((cert) => cert.file_kind === 'image')
        .map((cert) => cert.file_url)
        .filter(Boolean),
      fail: () => wx.showToast({ title: '证书预览失败，请重试', icon: 'none' }),
    });
  },

  copyCertificateUrl(url) {
    wx.setClipboardData({
      data: url,
      success: () => wx.showToast({ title: 'PDF 链接已复制', icon: 'none' }),
      fail: () => wx.showToast({ title: 'PDF 暂不可打开', icon: 'none' }),
    });
  },

  trackDetailEvent(eventName, extra) {
    const brand = this.data.brand;
    track(eventName, {
      page_path: '/pages/brand-detail/index',
      sourcePage: this.data.sourcePage,
      sourceModule: 'brand_detail',
      brandId: this.data.brandId || undefined,
      brandName: brand && brand.brand_name,
      tab: this.data.activeTab,
      page: this.data.productPage,
      pageSize: this.data.productPageSize,
      resultCount: this.data.activeTab === 'products' ? this.data.productTotal : this.data.certificates.length,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
