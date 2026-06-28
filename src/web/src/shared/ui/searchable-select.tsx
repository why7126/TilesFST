import { useEffect, useId, useRef, useState } from 'react';

import { cn } from '@/shared/lib/cn';

export interface SearchableSelectOption {
  value: string;
  label: string;
}

export interface SearchableSelectProps {
  value: string | null;
  options: SearchableSelectOption[];
  onChange: (value: string | null) => void;
  onSearch: (keyword: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  'aria-label'?: string;
}

export function SearchableSelect({
  value,
  options,
  onChange,
  onSearch,
  placeholder = '搜索并选择',
  disabled = false,
  className,
  'aria-label': ariaLabel,
}: SearchableSelectProps) {
  const listId = useId();
  const containerRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');

  const selected = options.find((option) => option.value === value);

  useEffect(() => {
    if (!open) return;
    const timer = window.setTimeout(() => onSearch(query), 300);
    return () => window.clearTimeout(timer);
  }, [open, query, onSearch]);

  useEffect(() => {
    const handlePointerDown = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setOpen(false);
        setQuery('');
      }
    };
    document.addEventListener('mousedown', handlePointerDown);
    return () => document.removeEventListener('mousedown', handlePointerDown);
  }, []);

  const displayValue = open ? query : selected?.label ?? '';

  return (
    <div ref={containerRef} className={cn('searchable-select', className)}>
      <input
        className="input searchable-select-input"
        value={displayValue}
        disabled={disabled}
        placeholder={placeholder}
        aria-label={ariaLabel}
        aria-expanded={open}
        aria-controls={listId}
        role="combobox"
        onChange={(event) => {
          setQuery(event.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
      />
      {open && !disabled ? (
        <ul id={listId} className="searchable-select-dropdown" role="listbox">
          {options.length === 0 ? (
            <li className="searchable-select-empty">无匹配结果</li>
          ) : (
            options.map((option) => (
              <li key={option.value}>
                <button
                  type="button"
                  className={cn(
                    'searchable-select-option',
                    option.value === value && 'is-selected',
                  )}
                  role="option"
                  aria-selected={option.value === value}
                  onClick={() => {
                    onChange(option.value);
                    setOpen(false);
                    setQuery('');
                  }}
                >
                  {option.label}
                </button>
              </li>
            ))
          )}
        </ul>
      ) : null}
    </div>
  );
}
