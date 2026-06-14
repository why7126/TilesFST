import { Navigate, Outlet, useLocation } from 'react-router-dom';

import { useAuth } from '../../features/auth/hooks/useAuth';

interface ProtectedRouteProps {
  requireAdmin?: boolean;
}

export function ProtectedRoute({ requireAdmin = false }: ProtectedRouteProps) {
  const location = useLocation();
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-page text-primary">
        加载中...
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/admin/login" replace state={{ from: location.pathname }} />;
  }

  if (user.role === 'store_owner') {
    return <Navigate to="/admin/forbidden" replace />;
  }

  if (requireAdmin && user.role !== 'admin') {
    return <Navigate to="/admin/forbidden" replace />;
  }

  return <Outlet />;
}
