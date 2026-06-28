import { useCallback, useEffect, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { TileSpecAdminItem, TileSpecAdminListData } from '@/shared/api/generated';

import {
  canDeleteTileSpec,
  deleteTileSpec,
  disableTileSpec,
  enableTileSpec,
  fetchTileSpecs,
} from '@/features/admin/api/tile-specs-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import { TileSpecFormModal } from '@/features/admin/components/TileSpecFormModal';
import {
  brandStatusBadgeClass,
  brandStatusLabel,
  formatBrandDateTime,
} from '@/features/admin/lib/brand-display';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/brand-management.css';
import '@/features/admin/styles/tile-spec-management.css';

const STATUS_OPTIONS = [
  { label: '全部状态', value: '' },
  { label: '启用', value: 'ENABLED' },
  { label: '停用', value: 'DISABLED' },
];

export function TileSpecManagementPage() {
  const [keyword, setKeyword] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [data, setData] = useState<TileSpecAdminListData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingSpec, setEditingSpec] = useState<TileSpecAdminItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<TileSpecAdminItem | null>(null);
  const [statusConfirmTarget, setStatusConfirmTarget] = useState<TileSpecAdminItem | null>(null);

  const loadSpecs = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchTileSpecs({
          page: currentPage,
          page_size: pageSize,
          keyword: keyword.trim() || undefined,
          status: status || undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载规格列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [keyword, status, page, pageSize],
  );

  useEffect(() => {
    void loadSpecs();
  }, [loadSpecs]);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const statusConfirmIsEnable = statusConfirmTarget?.status === 'DISABLED';

  const handleStatusConfirm = async () => {
    if (!statusConfirmTarget) return;
    try {
      if (statusConfirmTarget.status === 'DISABLED') {
        await enableTileSpec(statusConfirmTarget.id);
        setNotice('规格已启用');
      } else {
        await disableTileSpec(statusConfirmTarget.id);
        setNotice('规格已停用');
      }
      setStatusConfirmTarget(null);
      void loadSpecs();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      await deleteTileSpec(deleteTarget.id);
      setNotice('规格已删除');
      setDeleteTarget(null);
      void loadSpecs();
    } catch (err) {
      setNotice(getErrorMessage(err, '删除失败'));
    }
  };

  return (
    <>
      <AdminToast message={notice} />

      <section className="page-hero">
        <div>
          <p className="eyebrow">MASTER DATA</p>
          <h1 className="page-title">瓷砖规格</h1>
          <p className="page-desc">
            维护瓷砖宽度、长度、厚度，尺寸名称由系统自动生成，保障 SKU 建档与前台筛选一致。
          </p>
        </div>
        <button
          type="button"
          className="btn primary"
          onClick={() => {
            setFormMode('create');
            setEditingSpec(null);
            setFormOpen(true);
          }}
        >
          ＋ 新增瓷砖规格
        </button>
      </section>

      <section className="summary-grid" aria-label="规格统计">
        <article className="metric-card">
          <div className="metric-label">规格总数</div>
          <div className="metric-value">{data?.summary.total ?? '—'}</div>
          <div className="metric-desc">全部规格主数据</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">启用规格</div>
          <div className="metric-value">{data?.summary.enabled_count ?? '—'}</div>
          <div className="metric-desc">可用于 SKU 建档</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">停用规格</div>
          <div className="metric-value">{data?.summary.disabled_count ?? '—'}</div>
          <div className="metric-desc">不在下拉中展示</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">未关联 SKU</div>
          <div className="metric-value">{data?.summary.unlinked_sku_count ?? '—'}</div>
          <div className="metric-desc">可清理候选项</div>
        </article>
      </section>

      <section className="filter-card">
        <div className="tile-spec-filter-row">
          <input
            className="input"
            placeholder="搜索尺寸名称 / 宽度 / 长度 / 备注"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && (setPage(1), void loadSpecs(1))}
          />
          <select className="select" value={status} onChange={(e) => setStatus(e.target.value)}>
            {STATUS_OPTIONS.map((opt) => (
              <option key={opt.label} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
          <button
            type="button"
            className="btn primary"
            onClick={() => {
              setPage(1);
              void loadSpecs(1);
            }}
          >
            查询
          </button>
          <button
            type="button"
            className="btn"
            onClick={() => {
              setKeyword('');
              setStatus('');
              setPage(1);
              void fetchTileSpecs({ page: 1, page_size: pageSize }).then(setData);
            }}
          >
            重置
          </button>
        </div>
      </section>

      <section className="table-card" aria-label="规格列表">
        <table className="tile-spec-table">
          <thead>
            <tr>
              <th>尺寸名称</th>
              <th>宽度(mm)</th>
              <th>长度(mm)</th>
              <th>厚度(mm)</th>
              <th>关联SKU</th>
              <th>排序</th>
              <th>状态</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((spec) => {
              const deletable = canDeleteTileSpec(spec);
              return (
                <tr key={spec.id}>
                  <td>
                    <div className="size-name">{spec.display_name}</div>
                    {spec.remark ? <div className="size-sub">{spec.remark}</div> : null}
                  </td>
                  <td>{spec.width_mm}</td>
                  <td>{spec.length_mm}</td>
                  <td>{spec.thickness_mm ?? '—'}</td>
                  <td>{spec.sku_count}</td>
                  <td className="sort-num">{spec.sort_order}</td>
                  <td>
                    <span className={brandStatusBadgeClass(spec.status)}>
                      {brandStatusLabel(spec.status)}
                    </span>
                  </td>
                  <td>{formatBrandDateTime(spec.updated_at)}</td>
                  <td>
                    <div className="tile-spec-actions">
                      <button
                        type="button"
                        className="link-btn"
                        onClick={() => {
                          setFormMode('edit');
                          setEditingSpec(spec);
                          setFormOpen(true);
                        }}
                      >
                        编辑
                      </button>
                      <button
                        type="button"
                        className="link-btn muted"
                        onClick={() => setStatusConfirmTarget(spec)}
                      >
                        {spec.status === 'DISABLED' ? '启用' : '停用'}
                      </button>
                      <button
                        type="button"
                        className={`link-btn${deletable ? ' danger' : ' disabled'}`}
                        disabled={!deletable}
                        title={deletable ? undefined : '仅允许删除未关联SKU且已停用的规格'}
                        onClick={() => deletable && setDeleteTarget(spec)}
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
                <td colSpan={9}>暂无规格数据</td>
              </tr>
            ) : null}
          </tbody>
        </table>

        <div className="pagination">
          <div className="page-summary">共 {loading ? '…' : total} 条</div>
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
              <button type="button" className="page-btn active">
                {page}
              </button>
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

      <TileSpecFormModal
        open={formOpen}
        mode={formMode}
        spec={editingSpec}
        onClose={() => setFormOpen(false)}
        onSuccess={(message) => {
          setNotice(message);
          void loadSpecs();
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
            aria-labelledby="status-spec-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="status-spec-title" className="modal-title">
                {statusConfirmIsEnable ? '启用规格' : '停用规格'}
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
                  ? `确认启用规格「${statusConfirmTarget.display_name}」？`
                  : `确认停用规格「${statusConfirmTarget.display_name}」？停用后前台将不再展示该规格。`}
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
            aria-labelledby="delete-spec-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="delete-spec-title" className="modal-title">
                删除规格
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
                确认删除规格「{deleteTarget.display_name}」？此操作不可恢复。
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setDeleteTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleDeleteConfirm()}>
                删除规格
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
