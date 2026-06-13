import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/shared/lib/cn';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-page disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 rounded-industrial',
  {
    variants: {
      variant: {
        default:
          'bg-brand-gold text-page hover:bg-brand-gold/90 active:bg-brand-gold/80',
        destructive:
          'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline:
          'border border-border-strong bg-transparent text-secondary hover:border-border-hover hover:text-primary',
        inquiry:
          'border border-brand bg-transparent text-brand-gold hover:border-border-hover hover:bg-brand-gold-muted',
        ghost:
          'text-secondary hover:bg-accent hover:text-primary',
        link: 'text-brand-gold underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-16 px-6 text-sm',
        cta: 'h-auto px-6 py-[11px] text-sm',
        catalog: 'h-11 px-4 text-[13px]',
        sm: 'h-9 px-4 text-xs',
        icon: 'size-8 rounded-industrial',
        pagination: 'size-8 text-xs',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = 'Button';

export { Button, buttonVariants };
