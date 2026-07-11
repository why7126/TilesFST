import { DashboardMetrics } from '@/features/admin/components/DashboardMetrics';
import { DashboardQuickActions } from '@/features/admin/components/DashboardQuickActions';
import '@/features/admin/styles/admin-home.css';
import '@/features/admin/styles/user-management.css';
import { getPaginationWindow } from '@/shared/lib/pagination-window';
import { AdminListPage } from '@/shared/templates';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';

import { DesignSection, DesignSubSection } from './components';

const paginationExamples = [
  { label: '首页附近', currentPage: 1, totalPages: 12 },
  { label: '居中页', currentPage: 6, totalPages: 12 },
  { label: '末页附近', currentPage: 12, totalPages: 12 },
] as const;

const adminListMatrix = [
  '/admin/tile-skus',
  '/admin/brands',
  '/admin/tile-categories',
  '/admin/tile-specs',
  '/admin/banners',
  '/admin/users',
  '/admin/logs',
  '/admin/api-docs',
] as const;

const adminListRows = [
  {
    id: 'sku-001',
    name: '岩境灰 750x1500',
    category: '岩板',
    status: '已上架',
    updatedAt: '2026-07-10 18:30',
  },
  {
    id: 'sku-002',
    name: '云脉白 600x1200',
    category: '瓷砖',
    status: '草稿',
    updatedAt: '2026-07-10 16:12',
  },
];

const adminListColumns = [
  { key: 'name', header: '名称' },
  { key: 'category', header: '分类' },
  { key: 'status', header: '状态' },
  { key: 'updatedAt', header: '更新时间' },
  {
    key: 'actions',
    header: '操作',
    stickyAction: true,
    render: () => (
      <div className="brand-actions">
        <button type="button" className="link-btn">
          编辑
        </button>
        <button type="button" className="link-btn muted">
          查看
        </button>
      </div>
    ),
  },
] as const;

export function AdminSection() {
  return (
    <DesignSection
      id="admin-shell"
      title="Admin Shell"
      description="管理端工作台 Shell 预览（REQ-0004 / admin-home.css Port）"
    >
      <DesignSubSection title="Dashboard 模块片段">
        <div className="admin-shell overflow-hidden rounded-card border border-border-default">
          <div className="main-content !h-auto !max-h-[520px] !py-8 !px-6">
            <div className="content-inner">
              <DashboardMetrics />
              <DashboardQuickActions onActionClick={() => undefined} />
            </div>
          </div>
        </div>
      </DesignSubSection>

      <DesignSubSection title="管理端列表基础组件">
        <div id="admin-list-foundation" className="admin-shell rounded-card border border-border-default bg-page p-6">
          <MetricCardGrid ariaLabel="2 卡指标示例" columns={2}>
            <MetricCard label="TOTAL" value={128} description="正常数值" />
            <MetricCard label="EMPTY" value={null} description="统一空值占位" />
          </MetricCardGrid>

          <MetricCardGrid ariaLabel="3 卡指标示例" columns={3}>
            <MetricCard label="LOADING" loading description="加载中占位" />
            <MetricCard label="API ERRORS" value={7} description="异常请求" dangerDescription />
            <MetricCard label="SENSITIVE OPS" value={18} description="审计操作" />
          </MetricCardGrid>

          <MetricCardGrid ariaLabel="4 卡指标示例">
            <MetricCard label="SKU 总数" value={248} description="全部商品主数据" />
            <MetricCard label="已上架" value={196} description="前台可见商品" />
            <MetricCard label="待完善" value={16} description="缺主图或关键参数" dangerDescription />
            <MetricCard label="草稿" value={36} description="新建默认状态" />
          </MetricCardGrid>
        </div>
      </DesignSubSection>

      <DesignSubSection title="分页窗口边界">
        <div className="admin-shell overflow-hidden rounded-card border border-border-default">
          {paginationExamples.map((example) => (
            <div key={example.label} className="pagination">
              <span className="page-summary">
                {example.label} · 第 {example.currentPage} / {example.totalPages} 页
              </span>
              <div className="page-right">
                <div className="page-buttons">
                  {getPaginationWindow(example.currentPage, example.totalPages).map((pageNumber) => (
                    <button
                      key={pageNumber}
                      type="button"
                      className={`page-btn${pageNumber === example.currentPage ? ' active' : ''}`}
                      aria-current={pageNumber === example.currentPage ? 'page' : undefined}
                    >
                      {pageNumber}
                    </button>
                  ))}
                </div>
                <div className="page-size-wrap">
                  <span>每页显示</span>
                  <select className="page-size" aria-label={`${example.label}每页显示条数`} defaultValue="20">
                    <option value="20">20 条</option>
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
      </DesignSubSection>

      <DesignSubSection title="AdminListPage 页面模板契约">
        <div id="admin-list-page-contract" className="admin-shell rounded-card border border-border-default bg-page p-6">
          <AdminListPage
            content={{
              eyebrow: 'ADMIN LIST PAGE',
              title: '管理端列表模板',
              description: '页面级模板固定标题、指标卡、筛选、列表和分页模块顺序。',
              primaryActionLabel: '新增样例',
              metrics: [
                { label: 'TOTAL', value: 128, description: '全部记录' },
                { label: 'ACTIVE', value: 96, description: '可用记录' },
                { label: 'RISK', value: 7, description: '异常待处理', dangerDescription: true },
                { label: 'DRAFT', value: 25, description: '草稿记录' },
              ],
              filters: [
                {
                  id: 'admin-list-contract-keyword',
                  label: '关键词',
                  control: (
                    <input
                      id="admin-list-contract-keyword"
                      className="input"
                      placeholder="搜索名称 / 编号"
                      readOnly
                    />
                  ),
                },
                {
                  id: 'admin-list-contract-status',
                  label: '状态',
                  control: (
                    <select id="admin-list-contract-status" className="select" defaultValue="">
                      <option value="">全部状态</option>
                      <option value="active">已启用</option>
                      <option value="draft">草稿</option>
                    </select>
                  ),
                },
              ],
              columns: adminListColumns,
              rows: adminListRows,
              pagination: {
                page: 3,
                total: 128,
                pageSize: 20,
                itemLabel: '样例',
              },
            }}
            onCreate={() => undefined}
            onReset={() => undefined}
            onPageChange={() => undefined}
            onPageSizeChange={() => undefined}
            tableClassName="brand-mgmt-table"
            feedback={<div className="admin-toast-region" aria-live="polite" />}
          />

          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {[
              { label: 'loading', text: '数据加载中…' },
              { label: 'empty', text: '暂无数据' },
              { label: 'error', text: '加载失败，请稍后重试' },
              { label: 'single-page', text: '单页分页仍展示禁用翻页与当前页 1' },
            ].map((state) => (
              <article
                key={state.label}
                className="rounded-card border border-border-default bg-surface p-4"
                data-admin-list-boundary={state.label}
              >
                <p className="text-[10px] tracking-section text-brand-gold uppercase">{state.label}</p>
                <p className="mt-2 text-[12px] text-secondary">{state.text}</p>
              </article>
            ))}
          </div>

          <div className="mt-6">
            <p className="text-[10px] tracking-section text-muted uppercase">BUG-0055 页面矩阵</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {adminListMatrix.map((path) => (
                <span
                  key={path}
                  className="rounded-industrial border border-border-chip px-2 py-1 text-[11px] text-secondary"
                >
                  {path}
                </span>
              ))}
            </div>
          </div>
        </div>
      </DesignSubSection>
    </DesignSection>
  );
}
