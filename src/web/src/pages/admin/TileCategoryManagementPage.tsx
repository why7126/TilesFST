import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { TileCategoryAdminItem, TileCategoryAdminListData } from '@/shared/api/generated';

import {
  canDeleteCategory,
  deleteCategory,
  disableCategory,
  enableCategory,
  fetchCategories,
  fetchCategoryTree,
} from '@/features/admin/api/tile-categories-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import { CategoryFormModal } from '@/features/admin/components/CategoryFormModal';
import { CategoryTree } from '@/features/admin/components/CategoryTree';
import {
  CATEGORY_LEVEL_OPTIONS,
  CATEGORY_STATUS_OPTIONS,
  categoryLevelLabel,
  categoryStatusBadgeClass,
  categoryStatusLabel,
  formatCategoryDateTime,
  formatSkuCount,
} from '@/features/admin/lib/category-display';
import { getPaginationWindow } from '@/features/admin/lib/pagination';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/tile-category-management.css';

export function TileCategoryManagementPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [keyword, setKeyword] = useState('');
  const [status, setStatus] = useState('');
  const [level, setLevel] = useState('');
  const [selectedTreeId, setSelectedTreeId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [data, setData] = useState<TileCategoryAdminListData | null>(null);
  const [tree, setTree] = useState<Awaited<ReturnType<typeof fetchCategoryTree>>>([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingCategory, setEditingCategory] = useState<TileCategoryAdminItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<TileCategoryAdminItem | null>(null);
  const [statusConfirmTarget, setStatusConfirmTarget] = useState<TileCategoryAdminItem | null>(
    null,
  );

  const loadTree = useCallback(async () => {
    try {
      const nodes = await fetchCategoryTree();
      setTree(nodes);
    } catch (err) {
      setNotice(getErrorMessage(err, '加载类目树失败'));
    }
  }, []);

  const loadCategories = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchCategories({
          page: currentPage,
          page_size: pageSize,
          keyword: keyword.trim() || undefined,
          status: status || undefined,
          level: level ? Number(level) : undefined,
          parent_id: selectedTreeId ?? undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载类目列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [keyword, status, level, selectedTreeId, page, pageSize],
  );

  const refreshAll = useCallback(
    async (overridePage?: number) => {
      await loadTree();
      await loadCategories(overridePage);
    },
    [loadTree, loadCategories],
  );

  useEffect(() => {
    void refreshAll();
  }, [refreshAll]);

  useEffect(() => {
    if (searchParams.get('action') === 'create') {
      setFormMode('create');
      setEditingCategory(null);
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
    setLevel('');
    setSelectedTreeId(null);
    setPage(1);
    void fetchCategories({ page: 1, page_size: pageSize }).then(setData).catch((err) => {
      setNotice(getErrorMessage(err, '加载类目列表失败'));
    });
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingCategory(null);
    setFormOpen(true);
  };

  const openEdit = (category: TileCategoryAdminItem) => {
    setFormMode('edit');
    setEditingCategory(category);
    setFormOpen(true);
  };

  const openStatusConfirm = (category: TileCategoryAdminItem) => {
    setStatusConfirmTarget(category);
  };

  const handleStatusConfirm = async () => {
    if (!statusConfirmTarget) return;
    try {
      if (statusConfirmTarget.status === 'DISABLED') {
        await enableCategory(statusConfirmTarget.id);
        setNotice('类目已启用');
      } else {
        await disableCategory(statusConfirmTarget.id);
        setNotice('类目已停用');
      }
      setStatusConfirmTarget(null);
      void refreshAll();
    } catch (err) {
      setNotice(getErrorMessage(err, '操作失败'));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      await deleteCategory(deleteTarget.id);
      setNotice('类目已删除');
      setDeleteTarget(null);
      void refreshAll();
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
          <p className="eyebrow">CATEGORY MANAGEMENT</p>
          <h1 className="page-title">瓷砖类目管理</h1>
          <p className="page-desc">维护前台展示类目、层级路径、排序权重与 SKU 绑定关系。</p>
        </div>
        <button type="button" className="btn primary" onClick={openCreate}>
          ＋ 新增类目
        </button>
      </section>

      <section className="cat-section" aria-label="类目统计">
        <div className="summary-grid">
          <article className="metric-card">
            <div className="metric-label">类目总数</div>
            <div className="metric-value">{data?.summary.total ?? '—'}</div>
            <div className="metric-desc">含一级、二级类目</div>
          </article>
          <article className="metric-card">
            <div className="metric-label">启用类目</div>
            <div className="metric-value">{data?.summary.enabled_count ?? '—'}</div>
            <div className="metric-desc">当前前台可见类目</div>
          </article>
          <article className="metric-card">
            <div className="metric-label">绑定 SKU</div>
            <div className="metric-value">
              {data?.summary.bound_sku_total?.toLocaleString('zh-CN') ?? '—'}
            </div>
            <div className="metric-desc">已挂载商品数量</div>
          </article>
          <article className="metric-card">
            <div className="metric-label">最大层级</div>
            <div className="metric-value">{data?.summary.max_level ?? 2}</div>
            <div className="metric-desc">支持二级分类结构</div>
          </article>
        </div>
      </section>

      <section className="cat-section">
        <div className="filter-card">
          <div className="cat-filter-grid">
            <label>
              <span className="field-label">类目名称 / 编码</span>
              <input
                className="input"
                placeholder="输入类目名称、英文名或编码"
                value={keyword}
                onChange={(e) => {
                  setKeyword(e.target.value);
                  setPage(1);
                }}
                onKeyDown={(e) => e.key === 'Enter' && setPage(1)}
              />
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
                {CATEGORY_STATUS_OPTIONS.map((opt) => (
                  <option key={opt.label} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span className="field-label">层级</span>
              <select
                className="select"
                value={level}
                onChange={(e) => {
                  setLevel(e.target.value);
                  setPage(1);
                }}
              >
                {CATEGORY_LEVEL_OPTIONS.map((opt) => (
                  <option key={opt.label} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </label>
            <div className="cat-filter-actions">
              <button type="button" className="btn" onClick={handleReset}>
                重置
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="cat-section">
        <div className="cat-work-grid">
          <CategoryTree
            tree={tree}
            selectedId={selectedTreeId}
            totalCount={data?.summary.total ?? 0}
            totalSku={data?.summary.bound_sku_total ?? 0}
            onSelect={(id) => {
              setSelectedTreeId(id);
              setPage(1);
            }}
          />
          <div className="table-card">
            <table className="cat-mgmt-table">
              <thead>
                <tr>
                  <th>类目名称</th>
                  <th>层级</th>
                  <th>排序</th>
                  <th>SKU 数量</th>
                  <th>状态</th>
                  <th>更新时间</th>
                  <th className="admin-sticky-action-cell">操作</th>
                </tr>
              </thead>
              <tbody>
                {(data?.items ?? []).map((category) => {
                  const deletable = canDeleteCategory(category);
                  return (
                    <tr key={category.id}>
                      <td className="admin-sticky-action-cell">
                        <span className="cat-name">{category.name}</span>
                        <span className="cat-path">
                          {category.code} / {category.path}
                        </span>
                      </td>
                      <td>
                        <span className="cat-badge">{categoryLevelLabel(category.level)}</span>
                      </td>
                      <td>{category.sort_order}</td>
                      <td>{formatSkuCount(category.sku_count)}</td>
                      <td>
                        <span className={categoryStatusBadgeClass(category.status)}>
                          {categoryStatusLabel(category.status)}
                        </span>
                      </td>
                      <td>{formatCategoryDateTime(category.updated_at)}</td>
                      <td>
                        <div className="cat-actions">
                          <button
                            type="button"
                            className="link-btn"
                            onClick={() => openEdit(category)}
                          >
                            编辑
                          </button>
                          <button
                            type="button"
                            className="link-btn muted"
                            onClick={() => openStatusConfirm(category)}
                          >
                            {category.status === 'DISABLED' ? '启用' : '停用'}
                          </button>
                          {category.status === 'DISABLED' ? (
                            <button
                              type="button"
                              className={`link-btn${deletable ? ' danger' : ' disabled'}`}
                              disabled={!deletable}
                              title={
                                deletable ? undefined : '仅允许删除未绑定SKU且已停用的类目'
                              }
                              onClick={() => deletable && setDeleteTarget(category)}
                            >
                              删除
                            </button>
                          ) : null}
                        </div>
                      </td>
                    </tr>
                  );
                })}
                {!loading && (data?.items.length ?? 0) === 0 ? (
                  <tr>
                    <td colSpan={7}>暂无类目数据</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
            <div className="pagination">
              <div className="page-summary">共 {loading ? '…' : total} 个类目</div>
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
                    <option value={10}>10 条</option>
                    <option value={20}>20 条</option>
                    <option value={50}>50 条</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <CategoryFormModal
        open={formOpen}
        mode={formMode}
        category={editingCategory}
        tree={tree}
        defaultParentId={selectedTreeId}
        onClose={() => setFormOpen(false)}
        onSuccess={(message) => {
          setNotice(message);
          void refreshAll();
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
            aria-labelledby="status-category-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="status-category-title" className="modal-title">
                {statusConfirmIsEnable ? '启用类目' : '停用类目'}
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
                  ? `确认启用类目「${statusConfirmTarget.name}」？`
                  : `确认停用类目「${statusConfirmTarget.name}」？停用后前台将不再展示该类目。`}
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
            aria-labelledby="delete-category-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="delete-category-title" className="modal-title">
                删除类目
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
                确认删除类目「{deleteTarget.name}」？此操作不可恢复。
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setDeleteTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleDeleteConfirm()}>
                删除类目
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
