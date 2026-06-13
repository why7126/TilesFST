import { SearchIcon, SparklesIcon } from 'lucide-react';
import * as React from 'react';

import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/shared/lib/cn';

import { Button } from './button';

export interface SearchBarProps extends React.HTMLAttributes<HTMLDivElement> {
  categoryLabel?: string;
  categorySlot?: React.ReactNode;
  placeholder?: string;
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  onSearch?: (value: string) => void;
  onAiFindBrick?: () => void;
  aiFindBrickLabel?: string;
  searchLabel?: string;
}

const SearchBar = React.forwardRef<HTMLDivElement, SearchBarProps>(
  (
    {
      className,
      categoryLabel = '全部品类',
      categorySlot,
      placeholder = '搜索石材名称、规格、产地…',
      value,
      defaultValue,
      onValueChange,
      onSearch,
      onAiFindBrick,
      aiFindBrickLabel = 'AI 找砖',
      searchLabel = '搜索',
      ...props
    },
    ref,
  ) => {
    const [internalValue, setInternalValue] = React.useState(defaultValue ?? '');
    const query = value ?? internalValue;

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      if (value === undefined) {
        setInternalValue(event.target.value);
      }
      onValueChange?.(event.target.value);
    };

    const submit = () => {
      onSearch?.(query);
    };

    return (
      <div
        ref={ref}
        className={cn(
          'flex h-11 items-stretch overflow-hidden rounded-card border border-border-emphasis bg-surface',
          className,
        )}
        {...props}
      >
        <div className="flex shrink-0 items-center border-r border-border-default px-3.5">
          {categorySlot ?? (
            <button
              type="button"
              className="text-[11px] text-muted transition-colors hover:text-secondary"
            >
              {categoryLabel}
            </button>
          )}
        </div>

        <div className="relative min-w-0 flex-1">
          <Input
            value={query}
            onChange={handleChange}
            onKeyDown={(event) => {
              if (event.key === 'Enter') submit();
            }}
            placeholder={placeholder}
            className="h-11 rounded-none border-0 bg-transparent px-3.5 text-[13px] focus-visible:border-0"
          />
        </div>

        {onAiFindBrick ? (
          <>
            <Separator orientation="vertical" className="bg-border-default" />
            <button
              type="button"
              onClick={onAiFindBrick}
              className="inline-flex shrink-0 items-center gap-1.5 px-3.5 text-[11px] text-brand-gold transition-colors hover:text-brand-gold/90"
            >
              <SparklesIcon className="size-3.5" aria-hidden />
              {aiFindBrickLabel}
            </button>
          </>
        ) : null}

        <Button
          type="button"
          size="catalog"
          className="rounded-none rounded-r-card px-5"
          onClick={submit}
        >
          <SearchIcon className="size-3.5" aria-hidden />
          {searchLabel}
        </Button>
      </div>
    );
  },
);
SearchBar.displayName = 'SearchBar';

export { SearchBar };
