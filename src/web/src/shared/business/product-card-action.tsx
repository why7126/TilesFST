import type { LucideIcon } from 'lucide-react';
import * as React from 'react';

import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

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
    <Button
      type="button"
      variant="outline"
      size="icon"
      aria-label={label}
      className={cn('text-muted hover:text-primary', className)}
      {...props}
    >
      <Icon className="size-3.5" strokeWidth={1.5} aria-hidden />
    </Button>
  );
}
