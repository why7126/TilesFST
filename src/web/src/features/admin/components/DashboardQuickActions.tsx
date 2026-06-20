import { dashboardQuickActions } from '../data/dashboard-mock';

interface DashboardQuickActionsProps {
  onActionClick: (actionId: string) => void;
}

export function DashboardQuickActions({ onActionClick }: DashboardQuickActionsProps) {
  return (
    <section className="section" aria-labelledby="quick-title">
      <div className="section-head">
        <h2 className="section-title" id="quick-title">
          快捷操作
        </h2>
        <span className="section-note">常用管理入口</span>
      </div>
      <div className="quick-grid">
        {dashboardQuickActions.map((action) => (
          <button
            key={action.id}
            type="button"
            className="quick-card"
            onClick={() => onActionClick(action.id)}
          >
            <div className="quick-icon" aria-hidden>
              ＋
            </div>
            <div className="quick-title">{action.title}</div>
            <div className="quick-desc">{action.description}</div>
          </button>
        ))}
      </div>
    </section>
  );
}
