import { beginPageMedia, endPageMedia, isPageMediaActive, preparePageImages, preparePageFiles, reportPageMedia } from '../../utils/page-media';
import { sharePage, receiveShare } from '../../utils/public-sharing';
import { request, track } from '../../services/api';

type CertificateMediaItem = {
  media_id: number;
  media_type: 'image' | 'pdf' | 'unknown';
  url: string;
  preview_url?: string | null;
  thumbnail_url?: string | null;
  display_url?: string | null;
  original_url?: string | null;
  file_name?: string | null;
  file_mime_type?: string | null;
  sort_order: number;
  is_main: boolean;
  image_failed?: boolean;
};

type CertificateDetail = {
  certificate_id: number;
  certificate_name: string;
  certificate_type?: string | null;
  certificate_type_label: string;
  certificate_no?: string | null;
  issuer?: string | null;
  brand_id: number;
  brand_name: string;
  file_url?: string | null;
  thumbnail_url?: string | null;
  file_name?: string | null;
  file_mime_type?: string | null;
  file_kind: 'image' | 'pdf' | 'unknown';
  effective_date?: string | null;
  expiry_date?: string | null;
  validity_status: string;
  validity_status_label: string;
  brand: {
    brand_id: number;
    brand_name: string;
    brand_logo_thumbnail_url?: string | null;
    brand_entry_path: string;
    available: boolean;
  };
  media: CertificateMediaItem[];
  main_media?: CertificateMediaItem | null;
  description?: string | null;
  remark?: string | null;
  share: {
    title: string;
    path: string;
    image_url?: string | null;
    summary: string;
  };
};


const ACTION_LOCK_MS = 650;

function requestId(): string {
  return `certificate-detail-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
}

function safeText(value: unknown, fallback = '—'): string {
  const text = String(value || '').trim();
  return text || fallback;
}

function buildSharePath(certificateId: number): string {
  return `/pages/certificate-detail/index?certificateId=${encodeURIComponent(String(certificateId || 0))}&source=share`;
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
    detail: null as CertificateDetail | null,
    fields: [] as Array<{ label: string; value: string }>,
  },

  onShow() { beginPageMedia(this); },
  onHide() { endPageMedia(this); },
  onUnload() { endPageMedia(this); },

  onLoad(query: Record<string, string>) {
    beginPageMedia(this);
    query = receiveShare('certificate-detail', query);
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
    return sharePage('certificate-detail', this, 'wechat_friend');
  },

  onShareTimeline() {
    return sharePage('certificate-detail', this, 'wechat_timeline');
  },

  loadDetail() {
    if (!this.data.certificateId) {
      this.setData({ loading: false, error: '证书参数无效，可返回证书列表重新进入' });
      this.trackDetailEvent('certificate_detail_load_failed', { errorCode: 'invalid_certificate_id' });
      wx.stopPullDownRefresh();
      return;
    }
    this.setData({ loading: true, error: '', mediaError: '' });
    request<CertificateDetail>(`/api/v1/miniapp/certificates/${this.data.certificateId}`)
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

  normalizeDetail(detail: CertificateDetail): CertificateDetail {
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

  buildFields(detail: CertificateDetail): Array<{ label: string; value: string }> {
    return [
      { label: '证书类型', value: safeText(detail.certificate_type_label || detail.certificate_type) },
      { label: '证书编号', value: safeText(detail.certificate_no) },
      { label: '发证机构', value: safeText(detail.issuer) },
      { label: '有效状态', value: safeText(detail.validity_status_label) },
      { label: '备注说明', value: safeText(detail.remark) },
    ];
  },

  onMediaChange(event: WechatMiniprogram.SwiperChange) {
    const mediaIndex = Number(event.detail.current || 0);
    this.setData({ mediaIndex });
    const media = this.data.detail?.media?.[mediaIndex];
    this.trackDetailEvent('certificate_detail_media_switch', {
      mediaIndex,
      mediaType: media?.media_type || 'unknown',
    });
  },

  previewCurrentMedia() {
    const now = Date.now();
    if (now - this.lastActionAt < ACTION_LOCK_MS) return;
    this.lastActionAt = now;
    const media = this.data.detail?.media?.[this.data.mediaIndex];
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

  async previewImage(media: CertificateMediaItem) {
    const detail = this.data.detail;
    if (!detail) return;
    const images = detail.media.filter(item => item.media_type === 'image');
    try {
      const urls = await preparePageImages(this, images.map(item => ({resource_type:'certificate',resource_id:String(detail.certificate_id),media_id:item.media_id || undefined,variant:'original'})));
      const index = Math.max(0, images.findIndex(item => item.media_id === media.media_id));
      if (urls.length && isPageMediaActive(this)) {
        wx.previewImage({urls,current:urls[index],fail:() => this.setData({mediaError:'图片预览失败，请稍后重试'})});
        this.trackDetailEvent('certificate_detail_image_preview',{mediaId:media.media_id,mediaIndex:this.data.mediaIndex});
      }
    } catch { if (isPageMediaActive(this)) this.setData({mediaError:'图片暂不可预览'}); }
  },

  async openDocument(media: CertificateMediaItem) {
    const detail = this.data.detail;
    if (!detail) return;
    try {
      const reference = {resource_type:'certificate' as const,resource_id:String(detail.certificate_id),media_id:media.media_id || undefined,variant:'original' as const};
      const [filePath] = await preparePageFiles(this,[reference]);
      if (!isPageMediaActive(this)) return;
      this.trackDetailEvent('certificate_detail_file_open',{mediaId:media.media_id,mediaType:media.media_type,mediaIndex:this.data.mediaIndex});
      wx.openDocument({filePath,fileType:media.media_type === 'pdf' ? 'pdf' : undefined,
        success: () => reportPageMedia(this,reference,'preview','success'),
        fail: () => { if (isPageMediaActive(this)) this.showDocumentOpenFailed(); },
      });
    } catch { if (isPageMediaActive(this)) this.showDocumentOpenFailed(); }
  },

  showDocumentOpenFailed() {
    wx.showToast({ title: '文件暂不可打开', icon: 'none' });
  },

  onMediaError(event: WechatMiniprogram.TouchEvent) {
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

  trackDetailEvent(eventName: string, extra: Record<string, unknown>) {
    const detail = this.data.detail;
    track(eventName, {
      page_path: '/pages/certificate-detail/index',
      terminal: 'wechat_miniapp',
      certificateId: this.data.certificateId || detail?.certificate_id,
      brandId: detail?.brand_id,
      certificateType: detail?.certificate_type || detail?.certificate_type_label,
      sourcePage: this.data.sourcePage,
      sourceModule: this.data.sourceModule,
      requestId: this.data.requestId,
      ...extra,
    });
  },
});
