import type { ReactNode } from 'react';

import { cn } from '@/shared/lib/cn';

interface DividerTextProps {
  children: ReactNode;
  className?: string;
}

export function DividerText({ children, className }: DividerTextProps) {
  return (
    <div className={cn('flex items-center gap-4', className)}>
      <div className="h-[0.5px] flex-1 bg-border-default" />
      <span className="shrink-0 text-xs text-muted">{children}</span>
      <div className="h-[0.5px] flex-1 bg-border-default" />
    </div>
  );
}
