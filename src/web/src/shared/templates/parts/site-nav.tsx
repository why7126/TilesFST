import * as React from 'react';

import type { TemplateNavLink } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

export interface SiteNavProps extends React.HTMLAttributes<HTMLElement> {
  links: TemplateNavLink[];
  brand?: React.ReactNode;
  actions?: React.ReactNode;
}

export function SiteNav({ links, brand, actions, className, ...props }: SiteNavProps) {
  return (
    <header
      className={cn(
        'flex h-[52px] items-center justify-between border-b border-border-default bg-page px-7',
        className,
      )}
      {...props}
    >
      <div className="flex items-center gap-8">
        {brand ?? (
          <span className="font-brand text-sm tracking-brand text-primary uppercase">
            ST<span className="text-brand-gold">ONE</span>X
          </span>
        )}
        <nav className="hidden items-center gap-6 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className={cn(
                'relative text-[13px] font-medium transition-colors',
                link.active
                  ? 'text-primary after:absolute after:-bottom-[17px] after:left-0 after:h-[1.5px] after:w-full after:bg-brand-gold after:content-[""]'
                  : 'text-[var(--color-text-nav-link)] hover:text-primary',
              )}
            >
              {link.label}
            </a>
          ))}
        </nav>
      </div>
      <div className="flex items-center gap-3">
        {actions ?? (
          <>
            <Button variant="inquiry" size="sm">
              询价
            </Button>
            <Button variant="inquiry" size="sm">
              登录
            </Button>
          </>
        )}
      </div>
    </header>
  );
}
