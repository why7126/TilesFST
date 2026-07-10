import { DashboardMetrics } from '@/features/admin/components/DashboardMetrics';
import { DashboardQuickActions } from '@/features/admin/components/DashboardQuickActions';
import '@/features/admin/styles/admin-home.css';
import '@/features/admin/styles/user-management.css';
import { getPaginationWindow } from '@/shared/lib/pagination-window';
import { MetricCard, MetricCardGrid } from '@/shared/ui/metric-card';

import { DesignSection, DesignSubSection } from './components';

const paginationExamples = [
  { label: '首页附近', currentPage: 1, totalPages: 12 },
  { label: '居中页', currentPage: 6, totalPages: 12 },
  { label: '末页附近', currentPage: 12, totalPages: 12 },
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
    </DesignSection>
  );
}
