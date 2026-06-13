import * as React from 'react';

import type { TextureSwatch } from '@shared/business/types';
import { cn } from '@/shared/lib/cn';

export interface TextureRowProps extends React.HTMLAttributes<HTMLElement> {
  items: TextureSwatch[];
}

const TextureRow = React.forwardRef<HTMLElement, TextureRowProps>(
  ({ items, className, ...props }, ref) => (
    <section
      ref={ref}
      aria-label="纹理色系速览"
      className={cn('px-7 py-6', className)}
      {...props}
    >
      <div className="flex w-full">
        {items.map((item) => (
          <div key={item.id} className="relative flex-1 pb-[18px]">
            <div
              className="h-12 w-full rounded-industrial border border-border-default"
              style={{ backgroundColor: item.color }}
              title={item.name}
            />
            <span className="absolute bottom-0 left-0 text-[9px] text-muted">{item.name}</span>
          </div>
        ))}
      </div>
    </section>
  ),
);
TextureRow.displayName = 'TextureRow';

export { TextureRow };
