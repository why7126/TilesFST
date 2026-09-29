import { sharePage, receiveShare } from '../../utils/public-sharing';
Page({
  onLoad(query: Record<string, string>) {
    query = receiveShare('find', query);
  },
  onShareTimeline() {
    return sharePage('find', this, 'wechat_timeline');
  },
  onShareAppMessage() {
    return sharePage('find', this, 'wechat_friend');
  },
  openSearch() {
    wx.navigateTo({ url: '/pages/search/index' });
  },
});
