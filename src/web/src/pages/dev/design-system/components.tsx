import type { ReactNode } from 'react';

import { cn } from '@/shared/lib/cn';

export function DesignSection({
  id,
  title,
  description,
  children,
}: {
  id: string;
  title: string;
  description?: string;
  children: ReactNode;
}) {
  return (
    <section
      id={id}
      className="scroll-mt-24 space-y-4 rounded-card border border-border-default bg-surface p-6"
    >
      <div>
        <h2 className="text-base font-medium tracking-brand text-primary uppercase">{title}</h2>
        {description ? <p className="mt-1 text-[13px] text-secondary">{description}</p> : null}
      </div>
      {children}
    </section>
  );
}

export function DesignSubSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-[13px] font-medium text-secondary">{title}</h3>
      {children}
    </div>
  );
}

export function TokenTable({
  rows,
}: {
  rows: Array<{ token: string; cssVar?: string; value: string; className?: string }>;
}) {
  return (
    <div className="overflow-x-auto rounded-industrial border border-border-default">
      <table className="w-full min-w-[640px] text-left text-[12px]">
        <thead className="border-b border-border-default bg-page">
          <tr>
            <th className="px-3 py-2 font-medium text-muted">Token / Class</th>
            <th className="px-3 py-2 font-medium text-muted">CSS Variable</th>
            <th className="px-3 py-2 font-medium text-muted">Value</th>
            <th className="px-3 py-2 font-medium text-muted">Preview</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border-default">
          {rows.map((row) => (
            <tr key={row.token}>
              <td className="px-3 py-2 font-mono text-primary">{row.token}</td>
              <td className="px-3 py-2 font-mono text-muted">{row.cssVar ?? '—'}</td>
              <td className="px-3 py-2 font-mono text-subtle">{row.value}</td>
              <td className="px-3 py-2">
                {row.className ? (
                  <span
                    className={cn(
                      'inline-block min-w-16 rounded-industrial border border-border-default px-2 py-1',
                      row.className,
                    )}
                  >
                    Aa
                  </span>
                ) : (
                  '—'
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function SwatchGrid({
  items,
  type,
}: {
  items: Array<{ name: string; className: string; value: string }>;
  type: 'bg' | 'text' | 'border';
}) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {items.map((item) => (
        <div
          key={item.name}
          className="rounded-industrial border border-border-default bg-page p-3"
        >
          <div
            className={
              type === 'bg'
                ? `mb-2 h-10 rounded-industrial ${item.className}`
                : type === 'border'
                  ? `mb-2 h-10 rounded-industrial border-2 bg-transparent ${item.className}`
                  : `mb-2 text-sm ${item.className}`
            }
          >
            {type === 'text' ? 'Aa 样本' : null}
          </div>
          <p className="font-mono text-[11px] text-primary">{item.name}</p>
          <p className="font-mono text-[10px] text-muted">{item.value}</p>
        </div>
      ))}
    </div>
  );
}

export const designSystemNav = [
  { href: '#tokens-colors', label: '色彩 Token' },
  { href: '#tokens-typography', label: '字体 Token' },
  { href: '#tokens-spacing', label: '间距 Token' },
  { href: '#tokens-radius', label: '圆角 Token' },
  { href: '#tokens-shadows', label: '阴影 Token' },
  { href: '#ui-shadcn', label: 'shadcn 基础' },
  { href: '#ui-composite', label: '复合 UI' },
  { href: '#business-catalog', label: '业务组件' },
] as const;
