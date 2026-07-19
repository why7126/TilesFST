const { request, track } = require('../../services/api');

Page({
  data: {
    loading: true,
    error: '',
    store: null,
    services: [],
  },

  onLoad() {
    this.loadStore();
  },

  loadStore() {
    this.setData({ loading: true, error: '' });
    request('/api/v1/miniapp/home')
      .then((data) => this.setData({ store: data.store, services: data.services, loading: false }))
      .catch(() => this.setData({ error: '门店信息加载失败', loading: false }));
  },

  useService(event) {
    const item = event.currentTarget.dataset.service;
    if (!item || item.action_type === 'none') return;
    track('home_contact_click', {
      page_path: '/pages/store-info/index',
      contact_type: item.action_type,
    });
    if (item.action_type === 'phone' && item.action_value) {
      wx.makePhoneCall({ phoneNumber: item.action_value });
    } else if (item.action_value) {
      wx.setClipboardData({ data: item.action_value });
    }
  },
});
