import { Link } from 'react-router-dom';

import { Button } from '@/shared/ui/button';

export function ForbiddenPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-page px-6 text-primary">
      <p className="text-sm tracking-[0.18em] text-brand-gold">403</p>
      <h1 className="mt-4 text-3xl font-normal">无权限访问</h1>
      <p className="mt-3 max-w-md text-center text-sm text-secondary">
        当前账号没有访问该页面的权限，请联系管理员或使用具备权限的账号登录。
      </p>
      <Button asChild className="mt-8">
        <Link to="/admin/login">返回登录页</Link>
      </Button>
    </main>
  );
}
