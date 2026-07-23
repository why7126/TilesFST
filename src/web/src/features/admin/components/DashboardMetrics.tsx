import { useCallback, useEffect, useState } from 'react';

import { fetchDashboardSummary } from '../api/dashboard-api';
import type { AdminDashboardMetric, AdminDashboardSummary } from '../../../shared/api/generated';

type DashboardSummaryKey = keyof AdminDashboardSummary;

type MetricDefinition = {
  id: DashboardSummaryKey;
  label: string;
};

const metricDefinitions: MetricDefinition[] = [
  { id: 'sku_total', label: 'SKU 总数' },
  { id: 'brand_total', label: '品牌数量' },
  { id: 'banner_total', label: 'Banner 数量' },
  { id: 'user_total', label: '用户数量' },
];

function formatMetricValue(metric: AdminDashboardMetric | undefined): string {
  if (!metric) {
    return '加载中';
  }

  if (metric.visible === false) {
    return '—';
  }

  return new Intl.NumberFormat('zh-CN').format(metric.value);
}

export function DashboardMetrics() {
  const [summary, setSummary] = useState<AdminDashboardSummary | null>(null);
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');

  const loadSummary = useCallback(() => {
    let active = true;

    setStatus('loading');
    fetchDashboardSummary()
      .then((data) => {
        if (!active) {
          return;
        }
        setSummary(data);
        setStatus('success');
      })
      .catch(() => {
        if (!active) {
          return;
        }
        setSummary(null);
        setStatus('error');
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => loadSummary(), [loadSummary]);

  const metrics = metricDefinitions.map((definition) => {
    const metric = summary?.[definition.id];
    return { ...definition, metric };
  });

  return (
    <section className="section" aria-labelledby="metrics-title">
      <div className="section-head">
        <h2 className="section-title" id="metrics-title">
          数据概览
        </h2>
        <span className="section-note">核心主数据</span>
      </div>
      <div className="metric-grid">
        {metrics.map(({ id, label, metric }) => (
          <article key={id} className={`metric-card${status === 'loading' ? ' is-loading' : ''}`}>
            <div className="metric-label">{label}</div>
            <div className="metric-value">{formatMetricValue(metric)}</div>
            <div className="metric-desc">
              {status === 'loading' ? '正在同步数据' : (metric?.description ?? '等待服务端返回')}
            </div>
          </article>
        ))}
      </div>
      {status === 'error' ? (
        <div className="metrics-state" role="alert">
          <span>数据概览加载失败</span>
          <button className="metrics-retry" type="button" onClick={loadSummary}>
            重试
          </button>
        </div>
      ) : null}
    </section>
  );
}
