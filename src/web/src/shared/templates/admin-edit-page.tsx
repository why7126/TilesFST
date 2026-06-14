import type { AdminEditPageContent } from '@shared/templates/types';

import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

export interface AdminEditPageProps {
  content: AdminEditPageContent;
  onSubmit?: () => void;
  onCancel?: () => void;
  className?: string;
}

export function AdminEditPage({ content, onSubmit, onCancel, className }: AdminEditPageProps) {
  const {
    title,
    description,
    fields,
    submitLabel = '保存',
    cancelLabel = '取消',
  } = content;

  return (
    <section className={cn('mx-auto max-w-2xl space-y-8', className)}>
      <div className="border-b border-border-default pb-6">
        <h1 className="text-[22px] font-normal text-primary">{title}</h1>
        {description ? <p className="mt-2 text-[13px] text-secondary">{description}</p> : null}
      </div>

      <form
        className="space-y-7"
        onSubmit={(event) => {
          event.preventDefault();
          onSubmit?.();
        }}
      >
        {fields.map((field) => {
          if (field.type === 'checkbox') {
            return (
              <div key={field.id} className="flex items-center gap-3">
                <Checkbox id={field.id} defaultChecked={field.checked} />
                <Label htmlFor={field.id} className="text-[13px] text-primary">
                  {field.label}
                </Label>
              </div>
            );
          }

          if (field.type === 'textarea') {
            return (
              <div key={field.id} className="space-y-2">
                <Label htmlFor={field.id} className="text-[13px] text-secondary">
                  {field.label}
                </Label>
                <Textarea
                  id={field.id}
                  defaultValue={field.defaultValue}
                  placeholder={field.placeholder}
                />
              </div>
            );
          }

          return (
            <div key={field.id} className="space-y-2">
              <Label htmlFor={field.id} className="text-[13px] text-secondary">
                {field.label}
              </Label>
              <Input
                id={field.id}
                defaultValue={field.defaultValue}
                placeholder={field.placeholder}
              />
            </div>
          );
        })}

        <div className="flex flex-wrap gap-3 border-t border-border-default pt-6">
          <Button type="submit">{submitLabel}</Button>
          {onCancel ? (
            <Button type="button" variant="outline" onClick={onCancel}>
              {cancelLabel}
            </Button>
          ) : null}
        </div>
      </form>
    </section>
  );
}
