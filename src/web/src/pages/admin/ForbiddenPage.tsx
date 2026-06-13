import { Link } from 'react-router-dom';

export function ForbiddenPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-[#18160F] px-6 text-[#EDE8DF]">
      <p className="text-sm tracking-[0.18em] text-[#C8A055]">403</p>
      <h1 className="mt-4 text-3xl font-normal">无权限访问</h1>
      <p className="mt-3 max-w-md text-center text-sm text-[#EDE8DF]/50">
        当前账号没有访问该页面的权限，请联系管理员或使用具备权限的账号登录。
      </p>
      <Link
        to="/admin/login"
        className="mt-8 rounded-[2px] bg-[#C8A055] px-6 py-3 text-sm font-medium text-[#18160F]"
      >
        返回登录页
      </Link>
    </main>
  );
}
