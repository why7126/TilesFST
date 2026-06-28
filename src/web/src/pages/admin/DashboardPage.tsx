import { useNavigate, useOutletContext } from 'react-router-dom';

import { DashboardMetrics } from '../../features/admin/components/DashboardMetrics';
import { DashboardQuickActions } from '../../features/admin/components/DashboardQuickActions';
import { DashboardRecentUpdates } from '../../features/admin/components/DashboardRecentUpdates';

interface DashboardOutletContext {
  onPlaceholder: () => void;
}

export function DashboardPage() {
  const navigate = useNavigate();
  const context = useOutletContext<DashboardOutletContext | undefined>();
  const onPlaceholder = context?.onPlaceholder ?? (() => undefined);

  const onQuickAction = (actionId: string) => {
    if (actionId === 'brand') {
      navigate('/admin/brands?action=create');
      return;
    }
    if (actionId === 'category') {
      navigate('/admin/tile-categories?action=create');
      return;
    }
    if (actionId === 'sku') {
      navigate('/admin/tile-skus?action=create');
      return;
    }
    if (actionId === 'banner') {
      navigate('/admin/banners?action=create');
      return;
    }
    onPlaceholder();
  };

  return (
    <>
      <DashboardMetrics />
      <DashboardQuickActions onActionClick={onQuickAction} />
      <DashboardRecentUpdates />
    </>
  );
}
