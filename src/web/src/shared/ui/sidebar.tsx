import * as React from 'react';

import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/shared/lib/cn';

export interface SidebarFilterItem {
  id: string;
  label: string;
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
}

export interface SidebarSection {
  id: string;
  title: string;
  items: SidebarFilterItem[];
}

export interface SidebarProps extends React.HTMLAttributes<HTMLElement> {
  sections: SidebarSection[];
  footer?: React.ReactNode;
}

const Sidebar = React.forwardRef<HTMLElement, SidebarProps>(
  ({ className, sections, footer, ...props }, ref) => (
    <aside
      ref={ref}
      className={cn(
        'w-[200px] shrink-0 border-r border-border-default bg-page px-5 py-6',
        className,
      )}
      {...props}
    >
      <div className="space-y-6">
        {sections.map((section, index) => (
          <div key={section.id}>
            {index > 0 ? <Separator className="mb-6 bg-border-default" /> : null}
            <SidebarSectionBlock section={section} />
          </div>
        ))}
      </div>
      {footer ? <div className="mt-6 border-t border-border-default pt-6">{footer}</div> : null}
    </aside>
  ),
);
Sidebar.displayName = 'Sidebar';

function SidebarSectionBlock({ section }: { section: SidebarSection }) {
  return (
    <div className="space-y-3">
      <h2 className="text-[10px] font-medium tracking-section text-muted uppercase">
        {section.title}
      </h2>
      <ul className="space-y-2.5">
        {section.items.map((item) => (
          <SidebarFilterRow key={item.id} item={item} />
        ))}
      </ul>
    </div>
  );
}

function SidebarFilterRow({ item }: { item: SidebarFilterItem }) {
  const checked = item.checked ?? false;

  return (
    <li className="flex items-center gap-2">
      <Checkbox
        id={item.id}
        checked={checked}
        onCheckedChange={(value) => item.onCheckedChange?.(value === true)}
        className="size-[13px] rounded-industrial"
      />
      <Label
        htmlFor={item.id}
        className={cn(
          'cursor-pointer text-[12px] font-normal leading-none',
          checked ? 'text-primary' : 'text-muted',
        )}
      >
        {item.label}
      </Label>
    </li>
  );
}

export { Sidebar };
