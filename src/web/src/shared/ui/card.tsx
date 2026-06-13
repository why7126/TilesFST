import * as React from 'react';

import { cn } from '@/shared/lib/cn';

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'rounded-card border border-border-default bg-surface text-primary shadow-none-token',
        className,
      )}
      {...props}
    />
  ),
);
Card.displayName = 'Card';

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col gap-1.5 p-5', className)} {...props} />
  ),
);
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn('text-[13px] font-medium leading-snug text-primary', className)}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-[11px] leading-[1.5] text-muted', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('px-3.5 pb-3.5 pt-3', className)} {...props} />
  ),
);
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex items-center border-t border-border-default px-3.5 py-3', className)}
      {...props}
    />
  ),
);
CardFooter.displayName = 'CardFooter';

const CardMedia = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { aspect?: 'product' | 'featured' }
>(({ className, aspect = 'product', ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'overflow-hidden rounded-t-card bg-bg-overlay',
      aspect === 'product' ? 'h-[130px]' : 'min-h-[180px]',
      'transition-transform duration-[400ms] ease-out group-hover:scale-[1.03]',
      className,
    )}
    {...props}
  />
));
CardMedia.displayName = 'CardMedia';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent, CardMedia };
