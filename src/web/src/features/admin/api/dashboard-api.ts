import { api } from '@/features/auth/api/auth-api';
import type { AdminDashboardSummary } from '@/shared/api/generated';

export async function fetchDashboardSummary(): Promise<AdminDashboardSummary> {
  const response = await api.getAdminDashboardSummaryApiV1AdminDashboardSummaryGet();
  const summary = response.data.data;

  if (!summary) {
    throw new Error('Dashboard summary is empty');
  }

  return summary;
}
