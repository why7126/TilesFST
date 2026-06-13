import * as React from 'react';

import type { TemplateFilterChip } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';

export interface FilterChipsProps extends React.HTMLAttributes<HTMLDivElement> {
  chips: TemplateFilterChip[];
  onChipClick?: (id: string) => void;
}

export function FilterChips({ chips, onChipClick, className, ...props }: FilterChipsProps) {
  return (
    <div className={cn('flex flex-wrap gap-2 bg-page px-7 py-4', className)} {...props}>
      {chips.map((chip) => (
        <button
          key={chip.id}
          type="button"
          onClick={() => onChipClick?.(chip.id)}
          className={cn(
            'rounded-industrial border px-[14px] py-[5px] text-[11px] transition-colors',
            chip.active
              ? 'border-brand bg-brand-gold-muted text-brand-gold'
              : 'border-border-chip bg-transparent text-muted hover:border-border-hover',
          )}
        >
          {chip.label}
        </button>
      ))}
    </div>
  );
}
