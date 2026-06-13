import * as React from 'react';

import type { TemplateHeroMaterial, TemplateStatItem } from '@shared/templates/types';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/button';

export interface HeroSectionProps extends React.HTMLAttributes<HTMLElement> {
  eyebrow: string;
  title: string;
  description: string;
  materials: [TemplateHeroMaterial, TemplateHeroMaterial, TemplateHeroMaterial];
  stats: [TemplateStatItem, TemplateStatItem, TemplateStatItem, TemplateStatItem];
  onPrimaryAction?: () => void;
  onSecondaryAction?: () => void;
  primaryLabel?: string;
  secondaryLabel?: string;
}

export function HeroSection({
  eyebrow,
  title,
  description,
  materials,
  stats,
  onPrimaryAction,
  onSecondaryAction,
  primaryLabel = '浏览材质库',
  secondaryLabel = 'AI 找砖',
  className,
  ...props
}: HeroSectionProps) {
  const [tall, topRight, bottomRight] = materials;

  return (
    <section className={cn('bg-page px-7 pb-12 pt-[60px]', className)} {...props}>
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div className="flex flex-col justify-center">
          <p className="text-[10px] font-medium tracking-eyebrow text-brand-gold uppercase">
            {eyebrow}
          </p>
          <h1 className="mt-4 text-[38px] font-normal leading-[1.3] text-primary">{title}</h1>
          <p className="mt-4 max-w-xl text-[13px] leading-[1.8] text-secondary">{description}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button size="cta" onClick={onPrimaryAction}>
              {primaryLabel}
            </Button>
            <Button variant="outline" size="cta" onClick={onSecondaryAction}>
              {secondaryLabel}
            </Button>
          </div>
          <dl className="mt-10 grid grid-cols-2 gap-4 border-t border-border-default pt-6 sm:grid-cols-4">
            {stats.map((item) => (
              <div key={item.label}>
                <dt className="sr-only">{item.label}</dt>
                <dd className="text-[22px] font-medium text-primary">{item.value}</dd>
                <dt className="mt-1 text-[11px] text-subtle">{item.label}</dt>
              </div>
            ))}
          </dl>
        </div>

        <div className="grid grid-cols-2 grid-rows-2 gap-[3px]">
          <div
            className="relative row-span-2 overflow-hidden rounded-industrial border border-border-default"
            style={{ backgroundColor: tall.color }}
          >
            <MaterialCaption name={tall.name} spec={tall.spec} />
          </div>
          <div
            className="relative overflow-hidden rounded-industrial border border-border-default"
            style={{ backgroundColor: topRight.color }}
          >
            <MaterialCaption name={topRight.name} spec={topRight.spec} />
          </div>
          <div
            className="relative overflow-hidden rounded-industrial border border-border-default"
            style={{ backgroundColor: bottomRight.color }}
          >
            <MaterialCaption name={bottomRight.name} spec={bottomRight.spec} />
          </div>
        </div>
      </div>
    </section>
  );
}

function MaterialCaption({ name, spec }: { name: string; spec: string }) {
  return (
    <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-page/80 to-transparent px-3 py-3">
      <p className="text-[11px] font-medium text-primary">{name}</p>
      <p className="text-[9px] text-muted">{spec}</p>
    </div>
  );
}
