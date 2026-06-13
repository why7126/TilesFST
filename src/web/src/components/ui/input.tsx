import * as React from 'react';

import { cn } from '@/shared/lib/cn';

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<'input'>>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-16 w-full rounded-industrial border border-border-strong bg-transparent px-4 text-sm text-primary transition-colors',
          'placeholder:text-muted',
          'hover:border-border-hover',
          'focus-visible:border-border-focus focus-visible:outline-none focus-visible:ring-0',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'aria-invalid:border-error',
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = 'Input';

export { Input };
