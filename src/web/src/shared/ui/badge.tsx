import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/shared/lib/cn';

const badgeVariants = cva(
  'inline-flex items-center rounded-[1px] px-[7px] py-[2px] text-[9px] font-medium tracking-badge uppercase',
  {
    variants: {
      variant: {
        inStock: 'bg-brand-gold-badge text-brand-gold',
        new: 'bg-bg-badge-neutral text-secondary',
        hotSale: 'bg-hot-sale-muted text-hot-sale',
        neutral: 'border border-border-chip bg-transparent text-muted',
      },
    },
    defaultVariants: {
      variant: 'neutral',
    },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
