import { dashboardMetrics } from '../data/dashboard-mock';

export function DashboardMetrics() {
  return (
    <section className="section" aria-labelledby="metrics-title">
      <div className="section-head">
        <h2 className="section-title" id="metrics-title">
          数据概览
        </h2>
        <span className="section-note">核心主数据</span>
      </div>
      <div className="metric-grid">
        {dashboardMetrics.map((metric) => (
          <article key={metric.id} className="metric-card">
            <div className="metric-label">{metric.label}</div>
            <div className="metric-value">{metric.value}</div>
            <div className="metric-desc">{metric.description}</div>
          </article>
        ))}
      </div>
    </section>
  );
}
