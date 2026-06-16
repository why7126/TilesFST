import { DashboardMetrics } from '@/features/admin/components/DashboardMetrics';
import { DashboardQuickActions } from '@/features/admin/components/DashboardQuickActions';
import '@/features/admin/styles/admin-home.css';

import { DesignSection, DesignSubSection } from './components';

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
    </DesignSection>
  );
}
