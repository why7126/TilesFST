import { useEffect, useId, useRef, useState } from 'react';

import { cn } from '@/shared/lib/cn';

export interface AdminFilterSelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface AdminFilterSelectProps {
  id?: string;
  value: string;
  options: readonly AdminFilterSelectOption[];
  onChange: (value: string) => void;
  ariaLabel?: string;
  listLabel?: string;
  disabled?: boolean;
  className?: string;
}

export function AdminFilterSelect({
  id,
  value,
  options,
  onChange,
  ariaLabel,
  listLabel,
  disabled = false,
  className,
}: AdminFilterSelectProps) {
  const generatedId = useId();
  const triggerId = id ?? generatedId;
  const listId = `${triggerId}-options`;
  const containerRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const selected = options.find((option) => option.value === value);

  useEffect(() => {
    const handlePointerDown = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handlePointerDown);
    return () => document.removeEventListener('mousedown', handlePointerDown);
  }, []);

  return (
    <div ref={containerRef} className={cn('admin-filter-dropdown', className)}>
      <button
        id={triggerId}
        type="button"
        className="select admin-filter-dropdown-trigger sku-dropdown-trigger"
        aria-label={ariaLabel}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        disabled={disabled}
        onClick={() => setOpen((current) => !current)}
        onKeyDown={(event) => {
          if (event.key === 'Escape') {
            setOpen(false);
          }
        }}
      >
        <span>{selected?.label ?? options[0]?.label ?? '请选择'}</span>
        <span aria-hidden="true">⌄</span>
      </button>
      {open && !disabled ? (
        <div
          id={listId}
          className="admin-filter-dropdown-menu sku-dropdown-menu"
          role="listbox"
          aria-label={listLabel}
        >
          {options.map((option) => (
            <button
              key={option.label}
              type="button"
              className={cn(
                'admin-filter-dropdown-option sku-dropdown-option',
                option.value === value && 'active is-selected',
              )}
              role="option"
              aria-selected={option.value === value}
              aria-label={option.label}
              disabled={option.disabled}
              onClick={() => {
                onChange(option.value);
                setOpen(false);
              }}
            >
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
