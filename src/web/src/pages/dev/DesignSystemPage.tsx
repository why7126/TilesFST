import { AdminSection } from './design-system/admin-section';
import { BusinessSection } from './design-system/business-section';
import { designSystemNav } from './design-system/components';
import { TokensSection } from './design-system/tokens-section';
import { UiSection } from './design-system/ui-section';

export function DesignSystemPage() {
  return (
    <main className="min-h-screen bg-page text-primary">
      <div className="mx-auto flex max-w-7xl gap-8 px-8 py-8">
        <aside className="hidden w-44 shrink-0 lg:block">
          <nav className="sticky top-8 space-y-1">
            <p className="mb-3 text-[10px] font-medium tracking-section text-muted uppercase">
              验收导航
            </p>
            {designSystemNav.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="block rounded-industrial px-2 py-1.5 text-[12px] text-secondary transition-colors hover:bg-accent hover:text-primary"
              >
                {item.label}
              </a>
            ))}
          </nav>
        </aside>

        <div className="min-w-0 flex-1 space-y-8">
          <header className="space-y-2 border-b border-border-default pb-6">
            <p className="text-[10px] tracking-eyebrow text-brand-gold uppercase">
              STONEX Design System
            </p>
            <h1 className="text-[38px] font-normal leading-[1.3] text-primary">设计验收页</h1>
            <p className="max-w-3xl text-[13px] leading-[1.8] text-secondary">
              展示全部 Design Token、UI 组件与业务组件，对照 rules/ui-design.md 进行视觉与结构验收。
              开发环境路由：<code className="text-brand-gold">/design-system</code>
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              {['Token', 'UI', 'Business'].map((tag) => (
                <span
                  key={tag}
                  className="rounded-industrial border border-border-chip px-2 py-1 text-[10px] text-muted"
                >
                  {tag}
                </span>
              ))}
            </div>
          </header>

          <TokensSection />
          <UiSection />
          <BusinessSection />
          <AdminSection />

          <footer className="border-t border-border-default pt-6 text-[11px] text-subtle">
            参考文档：rules/ui-design.md · src/shared/design-system/tokens/ ·
            src/web/src/styles/globals.css
          </footer>
        </div>
      </div>
    </main>
  );
}
