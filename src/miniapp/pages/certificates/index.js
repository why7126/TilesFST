const { track } = require('../../services/api');

Page({
  data: {
    title: '证书',
    message: '证书功能建设中',
  },

  onLoad() {
    track('miniapp_certificate_tab_click', {
      page_path: '/pages/certificates/index',
      source: 'tab',
    });
  },
});
