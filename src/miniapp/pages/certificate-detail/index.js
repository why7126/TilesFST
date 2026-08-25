const { request, track } = require('../../services/api');

const ACTION_LOCK_MS = 650;

function requestId() {
  return `certificate-detail-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function safeText(value, fallback = '—') {
  const text = String(value || '').trim();
  return text || fallback;
}

function buildSharePath(certificateId) {
  return `/pages/certificate-detail/index?certificateId=${encodeURIComponent(String(certificateId || 0))}&source=share`;
}

function previewUrlForMedia(item) {
  return item.original_url || item.preview_url || item.url || '';
}

Page({
  lastActionAt: 0,
  data: {
    certificateId: 0,
    sourcePage: 'direct',
    sourceModule: 'direct',
    requestId: '',
    title: '证书详情',
    loading: true,
    error: '',
    mediaIndex: 0,
    mediaError: '',
    detail: null,
    fields: [],
  },

  onLoad(query) {
    const certificateId = Number(query.certificateId || query.certificate_id || 0);
    this.setData({
      certificateId,
      sourcePage: query.sourcePage || query.source || 'direct',
      sourceModule: query.sourceModule || 'certificate-detail',
      requestId: query.requestId || requestId(),
    });
    this.loadDetail();
  },

  onPullDownRefresh() {
    this.setData({ requestId: requestId() });
    this.loadDetail();
  },

  onShareAppMessage() {
    this.trackDetailEvent('certificate_detail_share_click', { shareChannel: 'wechat_friend' });
    const detail = this.data.detail;
    return {
      title: (detail && detail.share && detail.share.title) || (detail && detail.certificate_name) || '菲尚特证书',
      path: (detail && detail.share && detail.share.path) || buildSharePath(this.data.certificateId),
      imageUrl: (detail && detail.share && detail.share.image_url) || undefined,
    };
  },

  onShareTimeline() {
    this.trackDetailEvent('certificate_detail_share_click', { shareChannel: 'wechat_timeline' });
    const detail = this.data.detail;
    return {
      title: (detail && detail.share && detail.share.title) || (detail && detail.certificate_name) || '菲尚特证书',
      query: `certificateId=${encodeURIComponent(String(this.data.certificateId || 0))}&source=share`,
      imageUrl: (detail && detail.share && detail.share.image_url) || undefined,
    };
  },

  loadDetail() {
    if (!this.data.certificateId) {
      this.setData({ loading: false, error: '证书参数无效，可返回证书列表重新进入' });
      this.trackDetailEvent('certificate_detail_load_failed', { errorCode: 'invalid_certificate_id' });
      wx.stopPullDownRefresh();
      return;
    }
    this.setData({ loading: true, error: '', mediaError: '' });
    request(`/api/v1/miniapp/certificates/${this.data.certificateId}`)
      .then((detail) => {
        this.setData({
          detail: this.normalizeDetail(detail),
          title: '证书详情',
          fields: this.buildFields(detail),
          loading: false,
          mediaIndex: 0,
        });
        this.trackDetailEvent('certificate_detail_view', {});
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        this.setData({ loading: false, error: '证书暂不可查看，请稍后重试' });
        this.trackDetailEvent('certificate_detail_load_failed', { errorCode: 'detail_request_failed' });
        wx.stopPullDownRefresh();
      });
  },

  normalizeDetail(detail) {
    return {
      ...detail,
      media: (detail.media || []).map((item) => ({
        ...item,
        display_url: item.display_url || null,
        thumbnail_url: item.thumbnail_url || null,
        original_url: item.original_url || item.preview_url || null,
        preview_url: item.preview_url || item.original_url || null,
        image_failed: false,
      })),
    };
  },

  buildFields(detail) {
    return [
      { label: '证书类型', value: safeText(detail.certificate_type_label || detail.certificate_type) },
      { label: '证书编号', value: safeText(detail.certificate_no) },
      { label: '发证机构', value: safeText(detail.issuer) },
      { label: '有效状态', value: safeText(detail.validity_status_label) },
      { label: '备注说明', value: safeText(detail.remark) },
    ];
  },

  onMediaChange(event) {
    const mediaIndex = Number(event.detail.current || 0);
    this.setData({ mediaIndex });
    const media = this.data.detail && this.data.detail.media && this.data.detail.media[mediaIndex];
    this.trackDetailEvent('certificate_detail_media_switch', {
      mediaIndex,
      mediaType: (media && media.media_type) || 'unknown',
    });
  },

  previewCurrentMedia() {
    const now = Date.now();
    if (now - this.lastActionAt < ACTION_LOCK_MS) return;
    this.lastActionAt = now;
    const media = this.data.detail && this.data.detail.media && this.data.detail.media[this.data.mediaIndex];
    if (!media) {
      wx.showToast({ title: '证书文件暂不可预览', icon: 'none' });
      return;
    }
    if (media.media_type === 'image') {
      this.previewImage(media);
      return;
    }
    this.openDocument(media);
  },

  previewImage(media) {
    const urls = ((this.data.detail && this.data.detail.media) || [])
      .filter((item) => item.media_type === 'image')
      .map((item) => previewUrlForMedia(item))
      .filter((url) => !!url);
    if (!urls.length) {
      wx.showToast({ title: '图片暂不可预览', icon: 'none' });
      return;
    }
    const current = previewUrlForMedia(media) || urls[0];
    this.trackDetailEvent('certificate_detail_image_preview', {
      mediaId: media.media_id,
      mediaIndex: this.data.mediaIndex,
    });
    wx.previewImage({
      current,
      urls,
      fail: () => {
        this.setData({ mediaError: '图片预览失败，请稍后重试' });
        wx.showToast({ title: '图片预览失败', icon: 'none' });
      },
    });
  },

  openDocument(media) {
    if (!media.url) {
      wx.showToast({ title: '证书文件暂不可打开', icon: 'none' });
      return;
    }
    this.trackDetailEvent('certificate_detail_file_open', {
      mediaId: media.media_id,
      mediaType: media.media_type,
      mediaIndex: this.data.mediaIndex,
    });
    wx.downloadFile({
      url: media.url,
      success: (result) => {
        if (result.statusCode >= 200 && result.statusCode < 300) {
          wx.openDocument({
            filePath: result.tempFilePath,
            fileType: media.media_type === 'pdf' ? 'pdf' : undefined,
            fail: () => this.showDocumentOpenFailed(),
          });
          return;
        }
        this.showDocumentOpenFailed();
      },
      fail: () => this.showDocumentOpenFailed(),
    });
  },

  showDocumentOpenFailed() {
    wx.showToast({ title: '文件暂不可打开', icon: 'none' });
  },

  onMediaError(event) {
    const index = Number(event.currentTarget.dataset.index || 0);
    this.setData({
      [`detail.media[${index}].image_failed`]: true,
      mediaError: '证书图片加载失败，可继续查看证书信息',
    });
    this.trackDetailEvent('certificate_detail_load_failed', {
      errorCode: 'media_image_failed',
      mediaIndex: index,
    });
  },

  retryLoad() {
    this.loadDetail();
  },

  goCertificateList() {
    wx.switchTab({
      url: '/pages/certificates/index',
      fail: () => wx.reLaunch({ url: '/pages/index/index' }),
    });
  },

  trackDetailEvent(eventName, extra) {
    const detail = this.data.detail;
    track(eventName, {
      page_path: '/pages/certificate-detail/index',
      terminal: 'wechat_miniapp',
      certificateId: this.data.certificateId || (detail && detail.certificate_id),
      brandId: detail && detail.brand_id,
      certificateType: detail && (detail.certificate_type || detail.certificate_type_label),
      sourcePage: this.data.sourcePage,
      sourceModule: this.data.sourceModule,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
