import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import { AdminListPage } from '@/shared/templates';
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
  const statusConfirmIsEnable = statusConfirmTarget?.status === 'DISABLED';
  const rows = data?.items ?? [];

  return (
    <AdminListPage
      content={{
        eyebrow: 'MASTER DATA',
        title: '瓷砖品牌',
        description: '维护品牌名称、Logo、排序和启停状态，保障 SKU 主数据与前台展示一致。',
        primaryActionLabel: '＋ 新增品牌',
        metrics: [
          { label: '品牌总数', value: data?.summary.total, description: '全部品牌资料' },
          { label: '启用品牌', value: data?.summary.enabled_count, description: '前台可用品牌' },
          { label: '停用品牌', value: data?.summary.disabled_count, description: '暂不展示品牌' },
          { label: '未关联 SKU', value: data?.summary.unlinked_sku_count, description: '可清理候选项' },
        ],
        filters: [
          {
            id: 'brand-filter-keyword',
            label: '关键词',
            control: (
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
            ),
          },
          {
            id: 'brand-filter-status',
            label: '状态',
            control: (
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
            ),
          },
        ],
        columns: [
          {
            key: 'brand',
            header: '品牌',
            render: (brand) => (
              <div className="brand-cell">
                <div className="brand-logo">
                  {brand.logo_url ? (
                    <img
                      src={brand.logo_url}
                      alt=""
                      onError={(event) => {
                        event.currentTarget.closest('.brand-logo')?.classList.add('is-fallback');
                      }}
                    />
                  ) : null}
                  <span className="brand-logo-fallback">{getBrandInitials(brand.name)}</span>
                </div>
                <div>
                  <div className="brand-name">{brand.name}</div>
                  {brand.description ? (
                    <div className="brand-sub">{brand.description.slice(0, 24)}</div>
                  ) : null}
                </div>
              </div>
            ),
          },
          { key: 'short_name', header: '品牌简称', render: (brand) => brand.short_name || '—' },
          { key: 'english_name', header: '英文名称', render: (brand) => brand.english_name || '—' },
          { key: 'sort_order', header: '排序', className: 'sort-num' },
          { key: 'sku_count', header: 'SKU数量' },
          {
            key: 'status',
            header: '状态',
            render: (brand) => (
              <span className={brandStatusBadgeClass(brand.status)}>
                {brandStatusLabel(brand.status)}
              </span>
            ),
          },
          {
            key: 'updated_at',
            header: '更新时间',
            render: (brand) => formatBrandDateTime(brand.updated_at),
          },
          {
            key: 'actions',
            header: '操作',
            stickyAction: true,
            render: (brand) => {
              const deletable = canDeleteBrand(brand);
              return (
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
                    title={deletable ? undefined : '仅允许删除未关联SKU且已停用的品牌'}
                    onClick={() => deletable && setDeleteTarget(brand)}
                  >
                    删除
                  </button>
                </div>
              );
            },
          },
        ],
        rows,
        pagination: {
          page,
          total,
          pageSize,
          itemLabel: '品牌',
        },
        state: {
          emptyText: '暂无品牌数据',
          loadingText: '品牌数据加载中…',
        },
      }}
      onCreate={openCreate}
      onReset={handleReset}
      onPageChange={setPage}
      onPageSizeChange={(nextPageSize) => {
        setPageSize(nextPageSize);
        setPage(1);
      }}
      loading={loading}
      tableClassName="brand-mgmt-table"
      feedback={<AdminToast message={notice} />}
      confirmDialog={
        <>
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
      }
    />
  );
}
