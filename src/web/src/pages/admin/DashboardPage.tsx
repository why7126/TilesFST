import { useOutletContext } from 'react-router-dom';

import { DashboardMetrics } from '../../features/admin/components/DashboardMetrics';
import { DashboardQuickActions } from '../../features/admin/components/DashboardQuickActions';
import { DashboardRecentUpdates } from '../../features/admin/components/DashboardRecentUpdates';

interface DashboardOutletContext {
  onPlaceholder: () => void;
}

export function DashboardPage() {
  const context = useOutletContext<DashboardOutletContext | undefined>();
  const onPlaceholder = context?.onPlaceholder ?? (() => undefined);

  return (
    <>
      <DashboardMetrics />
      <DashboardQuickActions onActionClick={onPlaceholder} />
      <DashboardRecentUpdates />
    </>
  );
}
