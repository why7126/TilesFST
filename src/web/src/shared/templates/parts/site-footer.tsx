import * as React from 'react';

import type { TemplateFooterColumn } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';
import { Separator } from '@/components/ui/separator';

export interface SiteFooterProps extends React.HTMLAttributes<HTMLElement> {
  brand: { title: string; description: string };
  columns: TemplateFooterColumn[];
  copyright: string;
  social?: React.ReactNode;
}

export function SiteFooter({ brand, columns, copyright, social, className, ...props }: SiteFooterProps) {
  return (
    <footer className={cn('border-t border-border-default bg-deep px-7 pb-5 pt-7', className)} {...props}>
      <div className="grid gap-8 lg:grid-cols-[2fr_1fr_1fr_1fr]">
        <div>
          <p className="font-brand text-lg tracking-brand text-brand-gold uppercase">{brand.title}</p>
          <p className="mt-3 max-w-sm text-[11px] leading-[1.8] text-secondary">{brand.description}</p>
        </div>
        {columns.map((column) => (
          <div key={column.title ?? column.links[0]?.label}>
            {column.title ? (
              <p className="text-[10px] font-medium tracking-section text-muted uppercase">
                {column.title}
              </p>
            ) : null}
            <ul className="mt-3 space-y-2">
              {column.links.map((link) => (
                <li key={link.href}>
                  <a href={link.href} className="text-[11px] text-secondary transition-colors hover:text-primary">
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <Separator className="my-5 bg-border-default" />
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-[11px] text-subtle">{copyright}</p>
        {social}
      </div>
    </footer>
  );
}
