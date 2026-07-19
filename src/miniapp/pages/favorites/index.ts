import { track } from '../../services/api';

Page({
  data: {
    title: '收藏',
    message: '收藏功能建设中',
  },

  onLoad() {
    track('miniapp_home_favorite_visual_click', {
      page_path: '/pages/favorites/index',
      source: 'tab',
      product_id: 0,
    });
  },
});
