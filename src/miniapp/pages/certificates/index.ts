import { request, track } from '../../services/api';

type CertificateItem = {
  certificate_id: number;
  certificate_name: string;
  certificate_type?: string | null;
  certificate_type_label: string;
  brand_id: number;
  brand_name: string;
  file_url?: string | null;
  file_kind: 'image' | 'pdf' | 'unknown';
  image_failed?: boolean;
};

type CertificateListResponse = {
  items: CertificateItem[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
};

const PAGE_SIZE = 12;
const CLICK_LOCK_MS = 650;

function requestId(): string {
  return `cert-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

Page({
  lastPreviewAt: 0,
  data: {
    title: '证书列表',
    page: 1,
    pageSize: PAGE_SIZE,
    total: 0,
    hasMore: true,
    loading: true,
    refreshing: false,
    loadingMore: false,
    error: '',
    loadMoreError: '',
    requestId: '',
    skeletons: [1, 2, 3, 4],
    items: [] as CertificateItem[],
  },

  onLoad() {
    this.setCurrentTab();
    this.setData({ requestId: requestId() });
    this.trackListEvent('certificate_list_page_view', {});
    this.loadCertificates({ reset: true, eventName: 'certificate_list_load' });
  },

  onShow() {
    this.setCurrentTab();
  },

  onPullDownRefresh() {
    this.setData({ refreshing: true, requestId: requestId() });
    this.loadCertificates({ reset: true, eventName: 'certificate_list_refresh' });
  },

  onReachBottom() {
    this.loadCertificates({ reset: false, eventName: 'certificate_list_load_more' });
  },

  onShareAppMessage() {
    return {
      title: '菲尚特证书',
      path: '/pages/certificates/index',
    };
  },

  setCurrentTab() {
    const tabBar = this.getTabBar && this.getTabBar();
    if (tabBar) {
      tabBar.setData({ selected: 3 });
    }
  },

  loadCertificates(options: { reset: boolean; eventName?: string }) {
    if (this.data.loadingMore || (!options.reset && this.data.loading)) return;
    if (!options.reset && !this.data.hasMore) return;
    const nextPage = options.reset ? 1 : this.data.page + 1;
    this.setData({
      loading: options.reset,
      loadingMore: !options.reset,
      error: '',
      loadMoreError: '',
      ...(options.reset ? { items: [], hasMore: true, page: 1 } : {}),
    });

    request<CertificateListResponse>(`/api/v1/miniapp/certificates?${this.buildQuery(nextPage)}`)
      .then((data) => {
        const incoming = data.items || [];
        const merged = options.reset ? incoming : this.mergeCertificates(this.data.items, incoming);
        this.setData({
          items: merged,
          total: data.total || merged.length,
          page: data.page || nextPage,
          pageSize: data.page_size || this.data.pageSize,
          hasMore: Boolean(data.has_more),
          loading: false,
          refreshing: false,
          loadingMore: false,
        });
        this.trackListEvent(options.eventName || 'certificate_list_load', {
          page: nextPage,
          pageSize: this.data.pageSize,
          resultCount: incoming.length,
        });
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        this.setData(
          options.reset
            ? { error: this.data.items.length ? '网络异常，已保留已加载证书' : '证书列表加载失败，请重试', loading: false, refreshing: false }
            : { loadMoreError: '加载更多失败，点击重试', loadingMore: false },
        );
        this.trackListEvent('certificate_load_failed', {
          page: nextPage,
          pageSize: this.data.pageSize,
          errorCode: options.reset ? 'first_page_failed' : 'load_more_failed',
        });
        wx.stopPullDownRefresh();
      });
  },

  buildQuery(page: number): string {
    return [`page=${page}`, `pageSize=${this.data.pageSize}`].join('&');
  },

  mergeCertificates(current: CertificateItem[], incoming: CertificateItem[]): CertificateItem[] {
    const seen = new Set<number>();
    const result: CertificateItem[] = [];
    current.concat(incoming).forEach((item) => {
      if (!item || seen.has(item.certificate_id)) return;
      seen.add(item.certificate_id);
      result.push(item);
    });
    return result;
  },

  retryLoad() {
    this.loadCertificates({ reset: true, eventName: 'certificate_list_retry' });
  },

  retryLoadMore() {
    this.loadCertificates({ reset: false, eventName: 'certificate_list_load_more' });
  },

  openCertificate(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    const item = this.data.items[index];
    if (!item) return;
    const now = Date.now();
    if (now - this.lastPreviewAt < CLICK_LOCK_MS) return;
    this.lastPreviewAt = now;
    this.trackListEvent('certificate_click', this.certificateTrackPayload(item, index));
    wx.navigateTo({
      url: `/pages/certificate-detail/index?certificateId=${encodeURIComponent(String(item.certificate_id))}&sourcePage=certificate-list&sourceModule=certificate-card&index=${index}&requestId=${encodeURIComponent(this.data.requestId)}`,
      fail: () => wx.showToast({ title: '证书详情暂不可打开', icon: 'none' }),
    });
  },

  onImageError(event: WechatMiniprogram.TouchEvent) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({ [`items[${index}].image_failed`]: true });
    const item = this.data.items[index];
    if (item) {
      this.trackListEvent('certificate_load_failed', {
        ...this.certificateTrackPayload(item, index),
        errorCode: 'image_failed',
      });
    }
  },

  certificateTrackPayload(item: CertificateItem, index: number): Record<string, unknown> {
    return {
      certificateId: item.certificate_id,
      brandId: item.brand_id,
      certificateType: item.certificate_type || item.certificate_type_label,
      index,
      sourcePage: 'certificate_list',
    };
  },

  trackListEvent(eventName: string, extra: Record<string, unknown>) {
    track(eventName, {
      page_path: '/pages/certificates/index',
      terminal: 'wechat_miniapp',
      sourcePage: 'certificate_list',
      page: this.data.page,
      pageSize: this.data.pageSize,
      resultCount: this.data.total,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
