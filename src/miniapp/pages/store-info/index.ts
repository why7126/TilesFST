import { request, track } from '../../services/api';

type HomeData = {
  store: { name: string; description?: string; address?: string };
  services: Array<{
    key: string;
    title: string;
    description: string;
    action_type: 'none';
    action_value?: string;
  }>;
};

Page({
  data: {
    loading: true,
    error: '',
    store: null as HomeData['store'] | null,
    services: [] as HomeData['services'],
  },

  onLoad() {
    this.loadStore();
  },

  loadStore() {
    this.setData({ loading: true, error: '' });
    request<HomeData>('/api/v1/miniapp/home')
      .then((data) => this.setData({ store: data.store, services: data.services, loading: false }))
      .catch(() => this.setData({ error: '门店信息加载失败', loading: false }));
  },

  useService(event: WechatMiniprogram.TouchEvent) {
    const item = event.currentTarget.dataset.service as HomeData['services'][number];
    if (!item) return;
    track('home_contact_click', {
      page_path: '/pages/store-info/index',
      contact_type: item.action_type,
    });
    wx.showToast({ title: '门店服务信息已展示', icon: 'none' });
  },
});
