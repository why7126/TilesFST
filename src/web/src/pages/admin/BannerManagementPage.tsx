import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BannerAdminItem, BannerAdminListData } from '@/shared/api/generated';

import {
  deleteBanner,
  fetchBanners,
  offlineBanner,
  onlineBanner,
} from '@/features/admin/api/banners-api';
import { BannerFormModal } from '@/features/admin/components/BannerFormModal';
import { AdminToast } from '@/features/admin/components/AdminToast';
import {
  BANNER_PAGE_SIZES,
  BANNER_STATUS_OPTIONS,
  DISPLAY_CLIENT_OPTIONS,
  TIME_STATUS_OPTIONS,
  bannerStatusDisplay,
  canDeleteBanner,
  canOnlineBanner,
  displayClientBadgeClass,
  displayClientLabel,
  formatBannerDateTime,
  jumpTypeBadgeClass,
  jumpTypeLabel,
  positionLabel,
} from '@/features/admin/lib/banner-display';
import { getPaginationWindow } from '@/features/admin/lib/pagination';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/banner-management.css';

const MINIAPP_DISPLAY_CLIENT = 'MINIAPP_HOME';

export function BannerManagementPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [keyword, setKeyword] = useState('');
  const [displayClient, setDisplayClient] = useState(MINIAPP_DISPLAY_CLIENT);
  const [status, setStatus] = useState('');
  const [timeStatus, setTimeStatus] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [data, setData] = useState<BannerAdminListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingBanner, setEditingBanner] = useState<BannerAdminItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<BannerAdminItem | null>(null);
  const [statusConfirmTarget, setStatusConfirmTarget] = useState<BannerAdminItem | null>(null);

  const loadBanners = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchBanners({
          page: currentPage,
          page_size: pageSize,
          keyword: keyword.trim() || undefined,
          display_client: MINIAPP_DISPLAY_CLIENT,
          status: status || undefined,
          time_status: timeStatus || undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载 Banner 列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [keyword, displayClient, status, timeStatus, page, pageSize],
  );

  useEffect(() => {
    void loadBanners();
  }, [loadBanners]);

  useEffect(() => {
    if (searchParams.get('action') === 'create') {
      setFormMode('create');
      setEditingBanner(null);
      setFormOpen(true);
      setSearchParams({}, { replace: true });
    }
  }, [searchParams, setSearchParams]);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const handleReset = () => {
    setKeyword('');
    setDisplayClient(MINIAPP_DISPLAY_CLIENT);
    setStatus('');
    setTimeStatus('');
    setPage(1);
    void fetchBanners({
      page: 1,
      page_size: pageSize,
      display_client: MINIAPP_DISPLAY_CLIENT,
    }).then(setData).catch((err) => {
      setNotice(getErrorMessage(err, '加载 Banner 列表失败'));
    });
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingBanner(null);
    setFormOpen(true);
  };

  const openEdit = (banner: BannerAdminItem) => {
    setFormMode('edit');
    setEditingBanner(banner);
    setFormOpen(true);
  };

  const handleStatusConfirm = async () => {
    if (!statusConfirmTarget) return;
    try {
      if (statusConfirmTarget.status === 'ONLINE') {
        await offlineBanner(statusConfirmTarget.id);
        setNotice('Banner 已下线');
      } else {
        await onlineBanner(statusConfirmTarget.id);
        setNotice('Banner 已上线');
      }
      setStatusConfirmTarget(null);
      void loadBanners();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      await deleteBanner(deleteTarget.id);
      setNotice('Banner 已删除');
      setDeleteTarget(null);
      void loadBanners();
    } catch (err) {
      setNotice(getErrorMessage(err, '删除失败'));
    }
  };

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);
  const statusConfirmIsOnline = statusConfirmTarget?.status === 'ONLINE';

  return (
    <>
      <AdminToast message={notice} />

      <section className="page-hero">
        <div>
          <p className="eyebrow">OPERATIONS / BANNER MANAGEMENT</p>
          <h1 className="page-title">Banner 管理</h1>
          <p className="page-desc">
            维护小程序首页轮播与品牌列表页轮播的 Banner 内容、排序、跳转与生效时间。
          </p>
        </div>
        <button type="button" className="btn primary" onClick={openCreate}>
          ＋ 新增 Banner
        </button>
      </section>

      <section className="summary-grid" aria-label="Banner 统计">
        <article className="metric-card">
          <div className="metric-label">Banner 总数</div>
          <div className="metric-value">{data?.summary.total ?? '—'}</div>
          <div className="metric-desc">全部有效 Banner</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">当前筛选</div>
          <div className="metric-value">{data?.summary.filtered_count ?? '—'}</div>
          <div className="metric-desc">符合条件 Banner</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">已上线</div>
          <div className="metric-value">{data?.summary.online_count ?? '—'}</div>
          <div className="metric-desc">当前前台展示</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">待生效</div>
          <div className="metric-value">{data?.summary.pending_count ?? '—'}</div>
          <div className="metric-desc">已配置上线时间</div>
        </article>
      </section>

      <section className="filter-card">
        <div className="banner-filter-grid">
          <label>
            <span className="field-label">关键词</span>
            <input
              className="input"
              placeholder="搜索标题 / 位置 / 跳转链接"
              value={keyword}
              onChange={(e) => {
                setKeyword(e.target.value);
                setPage(1);
              }}
              onKeyDown={(e) => e.key === 'Enter' && setPage(1)}
            />
          </label>
          <label>
            <span className="field-label">展示端</span>
            <select
              className="select"
              value={displayClient}
              onChange={(e) => {
                setDisplayClient(e.target.value || MINIAPP_DISPLAY_CLIENT);
                setPage(1);
              }}
            >
              {DISPLAY_CLIENT_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">状态</span>
            <select
              className="select"
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
            >
              {BANNER_STATUS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">时间状态</span>
            <select
              className="select"
              value={timeStatus}
              onChange={(e) => {
                setTimeStatus(e.target.value);
                setPage(1);
              }}
            >
              {TIME_STATUS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
          <button type="button" className="btn" onClick={handleReset}>
            重置
          </button>
        </div>
      </section>

      <section className="table-card" aria-label="Banner 列表">
        <table className="banner-mgmt-table">
            <thead>
              <tr>
                <th>Banner</th>
                <th>展示位置</th>
                <th>展示端</th>
                <th>跳转类型</th>
                <th>状态</th>
                <th>有效期</th>
                <th>排序</th>
                <th>更新时间</th>
                <th className="admin-sticky-action-cell">操作</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={9}>加载中…</td>
                </tr>
              ) : (data?.items.length ?? 0) === 0 ? (
                <tr>
                  <td colSpan={9}>暂无 Banner</td>
                </tr>
              ) : (
                data?.items.map((banner) => {
                  const statusDisplay = bannerStatusDisplay(banner);
                  const deletable = canDeleteBanner(banner);
                  const onlineable = canOnlineBanner(banner);
                  return (
                    <tr key={banner.id}>
                      <td className="admin-sticky-action-cell">
                        <div className="banner-cell">
                          <span className="banner-thumb">
                            {banner.image_url ? <img src={banner.image_url} alt="" /> : null}
                          </span>
                          <span className="banner-main">{banner.title}</span>
                        </div>
                      </td>
                      <td>
                        <span className="banner-position">{positionLabel(banner.position)}</span>
                      </td>
                      <td>
                        <span className={displayClientBadgeClass(banner.display_client)}>
                          {displayClientLabel(banner.display_client)}
                        </span>
                      </td>
                      <td>
                        <span className={jumpTypeBadgeClass(banner.jump_type)}>
                          {jumpTypeLabel(banner.jump_type)}
                        </span>
                      </td>
                      <td>
                        <span className={statusDisplay.className}>{statusDisplay.label}</span>
                      </td>
                      <td>
                        <div className="time-range">
                          {formatBannerDateTime(banner.valid_from)}
                          <br />
                          {formatBannerDateTime(banner.valid_to)}
                        </div>
                      </td>
                      <td>{banner.sort_order}</td>
                      <td>{formatBannerDateTime(banner.updated_at)}</td>
                      <td>
                        <div className="banner-actions">
                          <button type="button" className="link-btn" onClick={() => openEdit(banner)}>
                            编辑
                          </button>
                          {banner.status === 'ONLINE' ? (
                            <button
                              type="button"
                              className="link-btn danger"
                              onClick={() => setStatusConfirmTarget(banner)}
                            >
                              下线
                            </button>
                          ) : (
                            <button
                              type="button"
                              className={`link-btn${onlineable ? '' : ' disabled'}`}
                              disabled={!onlineable}
                              title={onlineable ? undefined : '已过期 Banner 无法上线'}
                              onClick={() => onlineable && setStatusConfirmTarget(banner)}
                            >
                              上线
                            </button>
                          )}
                          <button
                            type="button"
                            className={`link-btn danger${deletable ? '' : ' disabled'}`}
                            disabled={!deletable}
                            title={deletable ? undefined : '已上线 Banner 需先下线后删除'}
                            onClick={() => deletable && setDeleteTarget(banner)}
                          >
                            删除
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        <div className="pagination">
          <div className="page-summary">共 {loading ? '…' : total} 个 Banner</div>
          <div className="page-right">
            <div className="page-buttons">
              <button
                type="button"
                className="page-btn"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
              >
                ‹
              </button>
              {pageNumbers.map((pageNumber) => (
                <button
                  key={pageNumber}
                  type="button"
                  className={`page-btn${pageNumber === page ? ' active' : ''}`}
                  aria-current={pageNumber === page ? 'page' : undefined}
                  onClick={() => setPage(pageNumber)}
                >
                  {pageNumber}
                </button>
              ))}
              <button
                type="button"
                className="page-btn"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              >
                ›
              </button>
            </div>
            <div className="page-size-wrap">
              <span>每页显示</span>
              <select
                className="page-size"
                value={pageSize}
                aria-label="每页显示条数"
                onChange={(e) => {
                  setPageSize(Number.parseInt(e.target.value, 10));
                  setPage(1);
                }}
              >
                {BANNER_PAGE_SIZES.map((size) => (
                  <option key={size} value={size}>
                    {size} 条
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </section>

      <BannerFormModal
        open={formOpen}
        mode={formMode}
        banner={editingBanner}
        onClose={() => setFormOpen(false)}
        onSuccess={(message) => {
          setNotice(message);
          void loadBanners();
        }}
      />

      {statusConfirmTarget ? (
        <div className="modal-backdrop" role="presentation" onClick={() => setStatusConfirmTarget(null)}>
          <div
            className="modal-card"
            role="dialog"
            aria-modal="true"
            aria-labelledby="banner-status-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="banner-status-title" className="modal-title">
                {statusConfirmIsOnline ? '下线 Banner' : '上线 Banner'}
              </span>
              <button
                type="button"
                className="modal-close"
                aria-label="关闭"
                onClick={() => setStatusConfirmTarget(null)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p className="page-desc">
                {statusConfirmIsOnline
                  ? `确认下线 Banner「${statusConfirmTarget.title}」？下线后前台将不再展示。`
                  : `确认上线 Banner「${statusConfirmTarget.title}」？上线后将按有效期在前台展示。`}
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setStatusConfirmTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleStatusConfirm()}>
                {statusConfirmIsOnline ? '确认下线' : '确认上线'}
              </button>
            </div>
          </div>
        </div>
      ) : null}

      {deleteTarget ? (
        <div className="modal-backdrop" role="presentation" onClick={() => setDeleteTarget(null)}>
          <div
            className="modal-card"
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-banner-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="delete-banner-title" className="modal-title">
                删除 Banner
              </span>
              <button
                type="button"
                className="modal-close"
                aria-label="关闭"
                onClick={() => setDeleteTarget(null)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p className="page-desc">确认删除 Banner「{deleteTarget.title}」？此操作不可恢复。</p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setDeleteTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleDeleteConfirm()}>
                删除 Banner
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
