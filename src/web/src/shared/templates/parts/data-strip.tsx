import * as React from 'react';

import type { TemplateStatItem } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';

export interface DataStripProps extends React.HTMLAttributes<HTMLElement> {
  items: [TemplateStatItem, TemplateStatItem, TemplateStatItem, TemplateStatItem];
}

export function DataStrip({ items, className, ...props }: DataStripProps) {
  return (
    <section
      className={cn(
        'grid grid-cols-2 border-y border-border-default bg-page lg:grid-cols-4',
        className,
      )}
      {...props}
    >
      {items.map((item, index) => (
        <div
          key={item.label}
          className={cn(
            'px-7 py-[18px]',
            index < items.length - 1 && 'border-b border-border-default lg:border-b-0 lg:border-r',
          )}
        >
          <p className="text-[20px] font-medium text-primary">{item.value}</p>
          <p className="mt-1 text-[11px] text-muted">{item.label}</p>
        </div>
      ))}
    </section>
  );
}
