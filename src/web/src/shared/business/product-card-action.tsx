import type { LucideIcon } from 'lucide-react';
import * as React from 'react';

import { cn } from '@/shared/lib/cn';

export interface ProductCardActionProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: LucideIcon;
  label: string;
}

export function ProductCardAction({
  icon: Icon,
  label,
  className,
  ...props
}: ProductCardActionProps) {
  return (
    <button
      type="button"
      aria-label={label}
      className={cn(
        'inline-flex size-7 shrink-0 items-center justify-center rounded-industrial border border-border-default text-muted transition-colors',
        'hover:bg-accent hover:text-primary',
        className,
      )}
      {...props}
    >
      <Icon className="size-3.5" strokeWidth={1.5} aria-hidden />
    </button>
  );
}
