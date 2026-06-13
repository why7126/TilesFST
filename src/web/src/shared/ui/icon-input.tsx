import type { LucideIcon } from 'lucide-react';
import * as React from 'react';

import { Input } from '@/components/ui/input';
import { cn } from '@/shared/lib/cn';

export interface IconInputProps extends React.ComponentProps<'input'> {
  icon: LucideIcon;
  error?: string;
  containerClassName?: string;
  iconClassName?: string;
}

const IconInput = React.forwardRef<HTMLInputElement, IconInputProps>(
  ({ icon: Icon, error, className, containerClassName, iconClassName, id, ...props }, ref) => {
    const inputId = id ?? React.useId();
    const errorId = error ? `${inputId}-error` : undefined;

    return (
      <div className={cn('space-y-1', containerClassName)}>
        <div className="relative">
          <Icon
            aria-hidden
            className={cn(
              'pointer-events-none absolute left-4 top-1/2 size-5 -translate-y-1/2 text-brand-gold/80',
              iconClassName,
            )}
          />
          <Input
            ref={ref}
            id={inputId}
            aria-invalid={error ? true : undefined}
            aria-describedby={errorId}
            className={cn('pl-11', className)}
            {...props}
          />
        </div>
        {error ? (
          <p id={errorId} className="text-xs text-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    );
  },
);
IconInput.displayName = 'IconInput';

export { IconInput };
