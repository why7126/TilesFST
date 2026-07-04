import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { BrandAdminItem, TileSkuAdminItem } from '@/shared/api/generated';

import { fetchBrands } from '@/features/admin/api/brands-api';
import { buildParentOptions, fetchCategoryTree } from '@/features/admin/api/tile-categories-api';
import {
  canDeleteTileSku,
  deleteTileSku,
  fetchTileSku,
  fetchTileSkus,
  formatReferencePrice,
  publishTileSku,
  unpublishTileSku,
  type TileSkuListData,
} from '@/features/admin/api/tile-skus-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import { TileSkuFormModal } from '@/features/admin/components/TileSkuFormModal';
import {
  formatSkuDateTime,
  MATERIAL_COMPLETENESS_OPTIONS,
  TILE_SKU_STATUS_OPTIONS,
  tileSkuStatusBadgeClass,
  tileSkuStatusLabel,
} from '@/features/admin/lib/tile-sku-display';
import { getPaginationWindow } from '@/features/admin/lib/pagination';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/tile-sku-management.css';

export function TileSkuManagementPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [keyword, setKeyword] = useState('');
  const [brandId, setBrandId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [status, setStatus] = useState('');
  const [materialCompleteness, setMaterialCompleteness] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [data, setData] = useState<TileSkuListData | null>(null);
  const [brands, setBrands] = useState<BrandAdminItem[]>([]);
  const [categoryOptions, setCategoryOptions] = useState<
    Array<{ id: number | null; label: string; level: number }>
  >([]);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  const [formOpen, setFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [editingSku, setEditingSku] = useState<TileSkuAdminItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<TileSkuAdminItem | null>(null);
  const [statusConfirmTarget, setStatusConfirmTarget] = useState<TileSkuAdminItem | null>(null);
  const [statusConfirmAction, setStatusConfirmAction] = useState<'publish' | 'unpublish' | null>(
    null,
  );

  useEffect(() => {
    void Promise.all([
      fetchBrands({ page: 1, page_size: 100 }),
      fetchCategoryTree(),
    ]).then(([brandData, tree]) => {
      setBrands(brandData.items);
      setCategoryOptions(buildParentOptions(tree).filter((o) => o.id != null));
    });
  }, []);

  const loadSkus = useCallback(
    async (overridePage?: number) => {
      const currentPage = overridePage ?? page;
      setLoading(true);
      try {
        const result = await fetchTileSkus({
          page: currentPage,
          page_size: pageSize,
          keyword: keyword.trim() || undefined,
          brand_id: brandId ? Number.parseInt(brandId, 10) : undefined,
          category_id: categoryId ? Number.parseInt(categoryId, 10) : undefined,
          status: status || undefined,
          material_completeness: materialCompleteness || undefined,
        });
        setData(result);
      } catch (err) {
        setNotice(getErrorMessage(err, '加载 SKU 列表失败'));
      } finally {
        setLoading(false);
      }
    },
    [keyword, brandId, categoryId, status, materialCompleteness, page, pageSize],
  );

  useEffect(() => {
    void loadSkus();
  }, [loadSkus]);

  useEffect(() => {
    if (searchParams.get('action') === 'create') {
      setFormMode('create');
      setEditingSku(null);
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
    setBrandId('');
    setCategoryId('');
    setStatus('');
    setMaterialCompleteness('');
    setPage(1);
    void fetchTileSkus({ page: 1, page_size: pageSize })
      .then(setData)
      .catch((err) => setNotice(getErrorMessage(err, '加载 SKU 列表失败')));
  };

  const openCreate = () => {
    setFormMode('create');
    setEditingSku(null);
    setFormOpen(true);
  };

  const openEdit = async (item: TileSkuAdminItem) => {
    try {
      const detail = await fetchTileSku(item.id);
      setFormMode('edit');
      setEditingSku(detail);
      setFormOpen(true);
    } catch (err) {
      setNotice(getErrorMessage(err, '加载 SKU 详情失败'));
    }
  };

  const openPublishConfirm = (item: TileSkuAdminItem) => {
    setStatusConfirmTarget(item);
    setStatusConfirmAction('publish');
  };

  const openUnpublishConfirm = (item: TileSkuAdminItem) => {
    setStatusConfirmTarget(item);
    setStatusConfirmAction('unpublish');
  };

  const closeStatusConfirm = () => {
    setStatusConfirmTarget(null);
    setStatusConfirmAction(null);
  };

  const handleStatusConfirm = async () => {
    if (!statusConfirmTarget || !statusConfirmAction) return;
    try {
      if (statusConfirmAction === 'publish') {
        await publishTileSku(statusConfirmTarget.id);
        setNotice('SKU 已上架');
      } else {
        await unpublishTileSku(statusConfirmTarget.id);
        setNotice('SKU 已下架');
      }
      closeStatusConfirm();
      void loadSkus();
    } catch (err) {
      setNotice(getErrorMessage(err, statusConfirmAction === 'publish' ? '上架失败' : '下架失败'));
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      await deleteTileSku(deleteTarget.id);
      setNotice('SKU 已删除');
      setDeleteTarget(null);
      void loadSkus();
    } catch (err) {
      setNotice(getErrorMessage(err, '删除失败'));
    }
  };

  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageNumbers = getPaginationWindow(page, totalPages);
  const statusConfirmIsPublish = statusConfirmAction === 'publish';

  return (
    <>
      <AdminToast message={notice} />

      <section className="page-hero sku-page-hero">
        <div>
          <p className="eyebrow">OPERATIONS / SKU</p>
          <h1 className="page-title">瓷砖 SKU</h1>
          <p className="page-desc">维护瓷砖商品资料、规格、参考价格、图片与视频素材完整度</p>
        </div>
        <button type="button" className="btn primary" onClick={openCreate}>
          ＋ 新增 SKU
        </button>
      </section>

      <section className="summary-grid" aria-label="SKU 统计">
        <article className="metric-card">
          <div className="metric-label">SKU 总数</div>
          <div className="metric-value">{data?.summary.total ?? '—'}</div>
          <div className="metric-desc">全部商品主数据</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">已上架</div>
          <div className="metric-value">{data?.summary.published_count ?? '—'}</div>
          <div className="metric-desc">前台可见商品</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">待完善</div>
          <div className="metric-value">{data?.summary.needs_completion_count ?? '—'}</div>
          <div className="metric-desc">缺主图或关键参数</div>
        </article>
        <article className="metric-card">
          <div className="metric-label">草稿</div>
          <div className="metric-value">{data?.summary.draft_count ?? '—'}</div>
          <div className="metric-desc">新建默认状态</div>
        </article>
      </section>

      <section className="filter-card">
        <div className="sku-filter-grid">
          <div className="brand-form-item">
            <label>关键词</label>
            <input
              className="input"
              placeholder="SKU 名称 / SKU 编码"
              value={keyword}
              onChange={(e) => {
                setKeyword(e.target.value);
                setPage(1);
              }}
              onKeyDown={(e) => e.key === 'Enter' && setPage(1)}
            />
          </div>
          <div className="brand-form-item">
            <label>品牌</label>
            <select
              className="select"
              value={brandId}
              onChange={(e) => {
                setBrandId(e.target.value);
                setPage(1);
              }}
            >
              <option value="">全部品牌</option>
              {brands.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name}
                </option>
              ))}
            </select>
          </div>
          <div className="brand-form-item">
            <label>类目</label>
            <select
              className="select"
              value={categoryId}
              onChange={(e) => {
                setCategoryId(e.target.value);
                setPage(1);
              }}
            >
              <option value="">全部类目</option>
              {categoryOptions.map((c) => (
                <option key={c.id} value={c.id!}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>
          <div className="brand-form-item">
            <label>状态</label>
            <select
              className="select"
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
            >
              {TILE_SKU_STATUS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div className="brand-form-item">
            <label>素材完整度</label>
            <select
              className="select"
              value={materialCompleteness}
              onChange={(e) => {
                setMaterialCompleteness(e.target.value);
                setPage(1);
              }}
            >
              {MATERIAL_COMPLETENESS_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div className="sku-filter-actions">
            <button type="button" className="btn" onClick={handleReset}>
              重置
            </button>
          </div>
        </div>
      </section>

      <section className="table-card" aria-label="SKU 列表">
        <table className="sku-mgmt-table">
          <thead>
            <tr>
              <th>SKU 信息</th>
              <th>品牌 / 类目</th>
              <th>规格 / 工艺</th>
              <th>参考价格</th>
              <th>素材</th>
              <th>状态</th>
              <th>更新时间</th>
              <th className="admin-sticky-action-cell">操作</th>
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((item) => {
              const deletable = canDeleteTileSku(item);
              return (
                <tr key={item.id}>
                  <td>
                    <div className="sku-cell">
                      <div className="sku-thumb">
                        {item.main_image_url ? <img src={item.main_image_url} alt="" /> : null}
                      </div>
                      <span>
                        <span className="sku-name">{item.name}</span>
                        <span className="sku-code">{item.sku_code}</span>
                      </span>
                    </div>
                  </td>
                  <td>
                    {item.brand_name}
                    <span className="sku-subline">{item.category_name}</span>
                  </td>
                  <td>
                    {item.size}
                    <span className="sku-subline">{item.surface_finish}</span>
                  </td>
                  <td className="sku-price">{formatReferencePrice(item.reference_price)}</td>
                  <td>
                    <div className="material-stack">
                      <span className={`mini-badge${item.has_main_image ? ' gold' : ''}`}>
                        {item.has_main_image ? '主图已设' : '缺主图'}
                      </span>
                      <span className="mini-badge">
                        {item.image_count} 图 / {item.video_count} 视频
                      </span>
                    </div>
                  </td>
                  <td>
                    <span className={tileSkuStatusBadgeClass(item.status)}>
                      {tileSkuStatusLabel(item.status)}
                    </span>
                  </td>
                  <td>{formatSkuDateTime(item.updated_at)}</td>
                  <td className="admin-sticky-action-cell">
                    <div className="sku-actions">
                      <button type="button" className="link-btn" onClick={() => void openEdit(item)}>
                        编辑
                      </button>
                      {item.status === 'PUBLISHED' ? (
                        <button
                          type="button"
                          className="link-btn muted"
                          onClick={() => openUnpublishConfirm(item)}
                        >
                          下架
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="link-btn muted"
                          onClick={() => openPublishConfirm(item)}
                        >
                          {item.status === 'DISABLED' ? '恢复' : '上架'}
                        </button>
                      )}
                      <button
                        type="button"
                        className={`link-btn${deletable ? ' danger' : ' disabled'}`}
                        disabled={!deletable}
                        title={deletable ? undefined : '已上架 SKU 不允许删除'}
                        onClick={() => deletable && setDeleteTarget(item)}
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
                <td colSpan={8}>暂无 SKU 数据</td>
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
                <option value={100}>100 条</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <TileSkuFormModal
        open={formOpen}
        mode={formMode}
        sku={editingSku}
        onClose={() => setFormOpen(false)}
        onSuccess={(message) => {
          setNotice(message);
          void loadSkus();
        }}
      />

      {statusConfirmTarget && statusConfirmAction ? (
        <div className="modal-backdrop" role="presentation" onClick={closeStatusConfirm}>
          <div
            className="modal-card"
            role="dialog"
            aria-modal="true"
            aria-labelledby="status-sku-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="status-sku-title" className="modal-title">
                {statusConfirmIsPublish ? '上架 SKU' : '下架 SKU'}
              </span>
              <button
                type="button"
                className="modal-close"
                aria-label="关闭"
                onClick={closeStatusConfirm}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p className="page-desc">
                {statusConfirmIsPublish
                  ? `确认上架 SKU「${statusConfirmTarget.name}」？`
                  : `确认下架 SKU「${statusConfirmTarget.name}」？下架后前台将不再展示该商品。`}
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={closeStatusConfirm}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleStatusConfirm()}>
                {statusConfirmIsPublish ? '确认上架' : '确认下架'}
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
            aria-labelledby="delete-sku-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-head">
              <span id="delete-sku-title" className="modal-title">
                删除 SKU
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
                确认删除 SKU「{deleteTarget.name}」？此操作不可恢复。
              </p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn" onClick={() => setDeleteTarget(null)}>
                取消
              </button>
              <button type="button" className="btn primary" onClick={() => void handleDeleteConfirm()}>
                删除 SKU
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
