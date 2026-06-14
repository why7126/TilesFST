import * as React from 'react';

import { cn } from '@/shared/lib/cn';

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<'textarea'>>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          'flex min-h-32 w-full rounded-industrial border border-border-strong bg-transparent px-4 py-3 text-[13px] text-primary transition-colors',
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
Textarea.displayName = 'Textarea';

export { Textarea };
