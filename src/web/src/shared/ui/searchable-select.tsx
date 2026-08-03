import { useEffect, useId, useRef, useState } from 'react';

import { cn } from '@/shared/lib/cn';

export interface SearchableSelectOption {
  value: string;
  label: string;
  description?: string;
}

export interface SearchableSelectProps {
  value: string | null;
  options: SearchableSelectOption[];
  onChange: (value: string | null) => void;
  onSearch: (keyword: string) => void;
  placeholder?: string;
  disabled?: boolean;
  loading?: boolean;
  error?: string | null;
  emptyText?: string;
  loadingText?: string;
  clearable?: boolean;
  clearLabel?: string;
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
  loading = false,
  error = null,
  emptyText = '无匹配结果',
  loadingText = '加载中...',
  clearable = false,
  clearLabel = '清空选择',
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

  const showStatus = loading || error || options.length === 0;

  return (
    <div ref={containerRef} className={cn('admin-filter-dropdown searchable-select', className)}>
      <input
        className="input admin-filter-dropdown-trigger searchable-select-input"
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
      {clearable && value && !disabled ? (
        <button
          type="button"
          className="searchable-select-clear"
          aria-label={clearLabel}
          onClick={() => {
            onChange(null);
            setOpen(false);
            setQuery('');
          }}
        >
          ×
        </button>
      ) : null}
      {open && !disabled ? (
        <ul
          id={listId}
          className="admin-filter-dropdown-menu searchable-select-dropdown"
          role="listbox"
        >
          {showStatus ? (
            <li className="admin-filter-dropdown-empty searchable-select-empty">
              {loading ? loadingText : error || emptyText}
            </li>
          ) : (
            options.map((option) => (
              <li key={option.value}>
                <button
                  type="button"
                  className={cn(
                    'admin-filter-dropdown-option searchable-select-option',
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
                  {option.description ? (
                    <span className="searchable-select-option-desc">{option.description}</span>
                  ) : null}
                  <span className="searchable-select-option-label">{option.label}</span>
                </button>
              </li>
            ))
          )}
        </ul>
      ) : null}
    </div>
  );
}
