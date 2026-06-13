import { Eye, EyeOff, Lock } from 'lucide-react';
import { useId, useState } from 'react';

import { Input } from '@/components/ui/input';
import { cn } from '@/shared/lib/cn';

interface PasswordInputProps {
  id?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  onEnter?: () => void;
  className?: string;
}

export function PasswordInput({
  id: idProp,
  value,
  onChange,
  placeholder = '请输入密码',
  error,
  onEnter,
  className,
}: PasswordInputProps) {
  const generatedId = useId();
  const id = idProp ?? generatedId;
  const errorId = error ? `${id}-error` : undefined;
  const [visible, setVisible] = useState(false);

  return (
    <div className="space-y-1">
      <div className="relative">
        <Lock
          className="pointer-events-none absolute left-4 top-1/2 size-5 -translate-y-1/2 text-brand-gold/80"
          aria-hidden="true"
        />
        <label htmlFor={id} className="sr-only">
          密码
        </label>
        <Input
          id={id}
          type={visible ? 'text' : 'password'}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              onEnter?.();
            }
          }}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
          aria-describedby={errorId}
          className={cn('pl-11 pr-12', error && 'border-error', className)}
        />
        <button
          type="button"
          onClick={() => setVisible((current) => !current)}
          className="absolute right-4 top-1/2 -translate-y-1/2 text-muted transition-colors hover:text-primary"
          aria-label={visible ? '隐藏密码' : '显示密码'}
        >
          {visible ? <EyeOff className="size-5" /> : <Eye className="size-5" />}
        </button>
      </div>
      {error ? (
        <p id={errorId} className="text-xs text-error" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
