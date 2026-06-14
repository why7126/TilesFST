import * as React from 'react';

import type { TemplateFilterChip } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

export interface FilterChipsProps extends React.HTMLAttributes<HTMLDivElement> {
  chips: TemplateFilterChip[];
  onChipClick?: (id: string) => void;
}

export function FilterChips({ chips, onChipClick, className, ...props }: FilterChipsProps) {
  return (
    <div className={cn('flex flex-wrap gap-2 bg-page px-7 py-4', className)} {...props}>
      {chips.map((chip) => (
        <Button
          key={chip.id}
          type="button"
          variant="ghost"
          size="sm"
          onClick={() => onChipClick?.(chip.id)}
          className={cn(
            'h-auto rounded-industrial px-[14px] py-[5px] text-[11px] font-normal',
            chip.active
              ? 'border border-brand bg-brand-gold-muted text-brand-gold hover:bg-brand-gold-muted'
              : 'border border-border-chip bg-transparent text-muted hover:border-border-hover hover:bg-transparent hover:text-muted',
          )}
        >
          {chip.label}
        </Button>
      ))}
    </div>
  );
}
