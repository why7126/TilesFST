import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BrandAdminItem, BrandAdminListData } from '@/shared/api/generated';

import {
  canDeleteBrand,
  deleteBrand,
  disableBrand,
  enableBrand,
  fetchBrands,
} from '@/features/admin/api/brands-api';
import { BrandFormModal } from '@/features/admin/components/BrandFormModal';
import { AdminToast } from '@/features/admin/components/AdminToast';
import {
  BRAND_STATUS_OPTIONS,
  brandStatusBadgeClass,
  brandStatusLabel,
  formatBrandDateTime,
  getBrandInitials,
} from '@/features/admin/lib/brand-display';
import { getPaginationWindow } from '@/features/admin/lib/pagination';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/brand-management.css';

export function BrandManagementPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [keyword, setKeyword] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [data, setData] = useState<BrandAdminListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingBrand, setEditingBrand] = useState<BrandAdminItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<BrandAdminItem | null>(null);
  const [statusConfirmTarget, setStatusConfirmTarget] = useState<BrandAdminItem | null>(null);

  const loadBrands = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchBrands({
          page: currentPage,
          page_size: pageSize,
          keyword: keyword.trim() || undefined,
          status: status || undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载品牌列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [keyword, status, page, pageSize],
  );

  useEffect(() => {
    void loadBrands();
  }, [loadBrands]);

  useEffect(() => {
    if (searchParams.get('action') === 'create') {
      setFormMode('create');
      setEditingBrand(null);
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
    setStatus('');
    setPage(1);
    void fetchBrands({ page: 1, page_size: pageSize }).then(setData).catch((err) => {
      setNotice(getErrorMessage(err, '加载品牌列表失败'));
    });
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingBrand(null);
    setFormOpen(true);
  };

  const openEdit = (brand: BrandAdminItem) => {
    setFormMode('edit');
    setEditingBrand(brand);
    setFormOpen(true);
  };

  const openStatusConfirm = (brand: BrandAdminItem) => {
    setStatusConfirmTarget(brand);
  };

  const handleStatusConfirm = async () => {
    if (!statusConfirmTarget) return;
    try {
      if (statusConfirmTarget.status === 'DISABLED') {
        await enableBrand(statusConfirmTarget.id);
        setNotice('品牌已启用');
      } else {
        await disableBrand(statusConfirmTarget.id);
        setNotice('品牌已停用');
      }
      setStatusConfirmTarget(null);
      void loadBrands();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      await deleteBrand(deleteTarget.id);
      setNotice('品牌已删除');
      setDeleteTarget(null);
      void loadBrands();
    } catch (err) {
      setNotice(getErrorMessage(err, '删除失败'));
    }
  };

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);
  const statusConfirmIsEnable = statusConfirmTarget?.status === 'DISABLED';

  return (
    <>
      <AdminToast message={notice} />

      <section className="page-hero">
        <div>
          <p className="eyebrow">MASTER DATA</p>
          <h1 className="page-title">瓷砖品牌</h1>
          <p className="page-desc">
            维护品牌名称、Logo、排序和启停状态，保障 SKU 主数据与前台展示一致。
          </p>
        </div>
        <button type="button" className="btn primary" onClick={openCreate}>
          ＋ 新增品牌
        </button>
      </section>

      <section className="summary-grid" aria-label="品牌统计">
        <article className="metric-card">
          <div className="metric-label">品牌总数</div>
          <div className="metric-value">{data?.summary.total ?? '—'}</div>
          <div className="metric-desc">全部品牌资料</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">启用品牌</div>
          <div className="metric-value">{data?.summary.enabled_count ?? '—'}</div>
          <div className="metric-desc">前台可用品牌</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">停用品牌</div>
          <div className="metric-value">{data?.summary.disabled_count ?? '—'}</div>
          <div className="metric-desc">暂不展示品牌</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">未关联 SKU</div>
          <div className="metric-value">{data?.summary.unlinked_sku_count ?? '—'}</div>
          <div className="metric-desc">可清理候选项</div>
        </article>
      </section>

      <section className="filter-card">
        <div className="brand-filter-row">
          <div className="brand-form-item">
            <label htmlFor="brand-filter-keyword">关键词</label>
            <input
              id="brand-filter-keyword"
              className="input"
              placeholder="搜索品牌名称 / 简称 / 英文名称"
              value={keyword}
              onChange={(e) => {
                setKeyword(e.target.value);
                setPage(1);
              }}
              onKeyDown={(e) => e.key === 'Enter' && setPage(1)}
            />
          </div>
          <div className="brand-form-item">
            <label htmlFor="brand-filter-status">状态</label>
            <select
              id="brand-filter-status"
              className="select"
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
            >
              {BRAND_STATUS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div className="brand-filter-actions">
            <button type="button" className="btn" onClick={handleReset}>
              重置
            </button>
          </div>
        </div>
      </section>

      <section className="table-card" aria-label="品牌列表">
        <table className="brand-mgmt-table">
          <thead>
            <tr>
              <th>品牌</th>
              <th>品牌简称</th>
              <th>英文名称</th>
              <th>排序</th>
              <th>SKU数量</th>
              <th>状态</th>
              <th>更新时间</th>
              <th className="admin-sticky-action-cell">操作</th>
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((brand) => {
              const deletable = canDeleteBrand(brand);
              return (
                <tr key={brand.id}>
                  <td>
                    <div className="brand-cell">
                      <div className="brand-logo">
                        {brand.logo_url ? (
                          <img
                            src={brand.logo_url}
                            alt=""
                            onError={(event) => {
                              event.currentTarget
                                .closest('.brand-logo')
                                ?.classList.add('is-fallback');
                            }}
                          />
                        ) : null}
                        <span className="brand-logo-fallback">
                          {getBrandInitials(brand.name)}
                        </span>
                      </div>
                      <div>
                        <div className="brand-name">{brand.name}</div>
                        {brand.description ? (
                          <div className="brand-sub">{brand.description.slice(0, 24)}</div>
                        ) : null}
                      </div>
                    </div>
                  </td>
                  <td>{brand.short_name || '—'}</td>
                  <td>{brand.english_name || '—'}</td>
                  <td className="sort-num">{brand.sort_order}</td>
                  <td>{brand.sku_count}</td>
                  <td>
                    <span className={brandStatusBadgeClass(brand.status)}>
                      {brandStatusLabel(brand.status)}
                    </span>
                  </td>
                  <td>{formatBrandDateTime(brand.updated_at)}</td>
                  <td className="admin-sticky-action-cell">
                    <div className="brand-actions">
                      <button type="button" className="link-btn" onClick={() => openEdit(brand)}>
                        编辑
                      </button>
                      <button
                        type="button"
                        className="link-btn muted"
                        onClick={() => openStatusConfirm(brand)}
                      >
                        {brand.status === 'DISABLED' ? '启用' : '停用'}
                      </button>
                      <button
                        type="button"
                        className={`link-btn${deletable ? ' danger' : ' disabled'}`}
                        disabled={!deletable}
                        title={
                          deletable ? undefined : '仅允许删除未关联SKU且已停用的品牌'
                        }
                        onClick={() => deletable && setDeleteTarget(brand)}
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
            {!loading && (data?.items.length ?? 0) === 0 ? (
              <tr>
                <td colSpan={8}>暂无品牌数据</td>
              </tr>
            ) : null}
          </tbody>
        </table>
        <div className="pagination">
          <div className="page-summary">共 {total} 条品牌</div>
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
                  setPageSize(Number(e.target.value));
                  setPage(1);
                }}
              >
                <option value={20}>20 条</option>
                <option value={50}>50 条</option>
                <option value={100}>100 条</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <BrandFormModal
        open={formOpen}
        mode={formMode}
        brand={editingBrand}
        onClose={() => setFormOpen(false)}
        onSuccess={(message) => {
          setNotice(message);
          void loadBrands();
        }}
      />

      {statusConfirmTarget ? (
        <div
          className="modal-backdrop"
          role="presentation"
          onClick={() => setStatusConfirmTarget(null)}
        >
          <div
            className="modal-card"
            role="dialog"
            aria-modal="true"
            aria-labelledby="status-brand-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="status-brand-title" className="modal-title">
                {statusConfirmIsEnable ? '启用品牌' : '停用品牌'}
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
                {statusConfirmIsEnable
                  ? `确认启用品牌「${statusConfirmTarget.name}」？`
                  : `确认停用品牌「${statusConfirmTarget.name}」？停用后前台将不再展示该品牌。`}
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setStatusConfirmTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleStatusConfirm()}>
                {statusConfirmIsEnable ? '确认启用' : '确认停用'}
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
            aria-labelledby="delete-brand-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="delete-brand-title" className="modal-title">
                删除品牌
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
              <p className="page-desc">
                确认删除品牌「{deleteTarget.name}」？此操作不可恢复。
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setDeleteTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleDeleteConfirm()}>
                删除品牌
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
