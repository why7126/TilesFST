// Generated from TypeScript; run node scripts/sync-media-read-controller.cjs.
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const page_media_1 = require("../../utils/page-media");
const public_sharing_1 = require("../../utils/public-sharing");
const api_1 = require("../../services/api");
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
    onShow() { (0, page_media_1.beginPageMedia)(this); },
    onHide() { (0, page_media_1.endPageMedia)(this); },
    onUnload() { (0, page_media_1.endPageMedia)(this); },
    onLoad(query) {
        (0, page_media_1.beginPageMedia)(this);
        query = (0, public_sharing_1.receiveShare)('certificate-detail', query);
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
        return (0, public_sharing_1.sharePage)('certificate-detail', this, 'wechat_friend');
    },
    onShareTimeline() {
        return (0, public_sharing_1.sharePage)('certificate-detail', this, 'wechat_timeline');
    },
    loadDetail() {
        if (!this.data.certificateId) {
            this.setData({ loading: false, error: '证书参数无效，可返回证书列表重新进入' });
            this.trackDetailEvent('certificate_detail_load_failed', { errorCode: 'invalid_certificate_id' });
            wx.stopPullDownRefresh();
            return;
        }
        this.setData({ loading: true, error: '', mediaError: '' });
        (0, api_1.request)(`/api/v1/miniapp/certificates/${this.data.certificateId}`)
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
        var _a, _b;
        const mediaIndex = Number(event.detail.current || 0);
        this.setData({ mediaIndex });
        const media = (_b = (_a = this.data.detail) === null || _a === void 0 ? void 0 : _a.media) === null || _b === void 0 ? void 0 : _b[mediaIndex];
        this.trackDetailEvent('certificate_detail_media_switch', {
            mediaIndex,
            mediaType: (media === null || media === void 0 ? void 0 : media.media_type) || 'unknown',
        });
    },
    previewCurrentMedia() {
        var _a, _b;
        const now = Date.now();
        if (now - this.lastActionAt < ACTION_LOCK_MS)
            return;
        this.lastActionAt = now;
        const media = (_b = (_a = this.data.detail) === null || _a === void 0 ? void 0 : _a.media) === null || _b === void 0 ? void 0 : _b[this.data.mediaIndex];
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
    async previewImage(media) {
        const detail = this.data.detail;
        if (!detail)
            return;
        const images = detail.media.filter(item => item.media_type === 'image');
        try {
            const urls = await (0, page_media_1.preparePageImages)(this, images.map(item => ({ resource_type: 'certificate', resource_id: String(detail.certificate_id), media_id: item.media_id || undefined, variant: 'original' })));
            const index = Math.max(0, images.findIndex(item => item.media_id === media.media_id));
            if (urls.length && (0, page_media_1.isPageMediaActive)(this)) {
                wx.previewImage({ urls, current: urls[index], fail: () => this.setData({ mediaError: '图片预览失败，请稍后重试' }) });
                this.trackDetailEvent('certificate_detail_image_preview', { mediaId: media.media_id, mediaIndex: this.data.mediaIndex });
            }
        }
        catch (_a) {
            if ((0, page_media_1.isPageMediaActive)(this))
                this.setData({ mediaError: '图片暂不可预览' });
        }
    },
    async openDocument(media) {
        const detail = this.data.detail;
        if (!detail)
            return;
        try {
            const reference = { resource_type: 'certificate', resource_id: String(detail.certificate_id), media_id: media.media_id || undefined, variant: 'original' };
            const [filePath] = await (0, page_media_1.preparePageFiles)(this, [reference]);
            if (!(0, page_media_1.isPageMediaActive)(this))
                return;
            this.trackDetailEvent('certificate_detail_file_open', { mediaId: media.media_id, mediaType: media.media_type, mediaIndex: this.data.mediaIndex });
            wx.openDocument({ filePath, fileType: media.media_type === 'pdf' ? 'pdf' : undefined,
                success: () => (0, page_media_1.reportPageMedia)(this, reference, 'preview', 'success'),
                fail: () => { if ((0, page_media_1.isPageMediaActive)(this))
                    this.showDocumentOpenFailed(); },
            });
        }
        catch (_a) {
            if ((0, page_media_1.isPageMediaActive)(this))
                this.showDocumentOpenFailed();
        }
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
        (0, api_1.track)(eventName, {
            page_path: '/pages/certificate-detail/index',
            terminal: 'wechat_miniapp',
            certificateId: this.data.certificateId || (detail === null || detail === void 0 ? void 0 : detail.certificate_id),
            brandId: detail === null || detail === void 0 ? void 0 : detail.brand_id,
            certificateType: (detail === null || detail === void 0 ? void 0 : detail.certificate_type) || (detail === null || detail === void 0 ? void 0 : detail.certificate_type_label),
            sourcePage: this.data.sourcePage,
            sourceModule: this.data.sourceModule,
            requestId: this.data.requestId,
            ...extra,
        });
    },
});
