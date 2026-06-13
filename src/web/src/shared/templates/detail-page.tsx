import type { DetailPageContent } from '@shared/templates/types';

import { Badge } from '@/shared/ui/badge';
import { Button } from '@/shared/ui/button';
import { Card, CardContent } from '@/shared/ui/card';

import { SiteNav } from './parts/site-nav';

export interface DetailPageProps {
  content: DetailPageContent;
  onBack?: () => void;
  onCta?: () => void;
  backLabel?: string;
}

const defaultNavLinks = [
  { label: '材质库', href: '/catalog' },
  { label: '工程案例', href: '/cases' },
  { label: '供应商', href: '/suppliers' },
];

export function DetailPage({
  content,
  onBack,
  onCta,
  backLabel = '返回列表',
}: DetailPageProps) {
  const {
    name,
    spec,
    price,
    priceUnit = '/m²',
    imageUrl,
    badges = [],
    description,
    specRows,
    ctaLabel = '立即询价',
  } = content;

  return (
    <div className="min-h-screen bg-page text-primary">
      <SiteNav links={defaultNavLinks} />

      <main className="mx-auto max-w-6xl px-7 py-8">
        {onBack ? (
          <button
            type="button"
            onClick={onBack}
            className="mb-6 text-[11px] text-secondary transition-colors hover:text-primary"
          >
            ← {backLabel}
          </button>
        ) : null}

        <Card className="overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2">
            <div className="min-h-[280px] bg-bg-overlay lg:min-h-[420px]">
              {imageUrl ? (
                <img src={imageUrl} alt={name} className="size-full object-cover" />
              ) : null}
            </div>

            <CardContent className="flex flex-col justify-between p-5 lg:p-8">
              <div>
                {badges.length > 0 ? (
                  <div className="mb-3 flex flex-wrap gap-[5px]">
                    {badges.map((badge) => (
                      <Badge key={badge.label} variant={badge.variant}>
                        {badge.label}
                      </Badge>
                    ))}
                  </div>
                ) : null}

                <h1 className="text-[22px] font-normal text-primary">{name}</h1>
                <p className="mt-2 text-[11px] leading-[1.5] text-muted">{spec}</p>

                {description ? (
                  <p className="mt-4 text-[13px] leading-[1.8] text-secondary">{description}</p>
                ) : null}

                <div className="mt-6 grid grid-cols-2 gap-2">
                  {specRows.map((row) => (
                    <div key={row.label} className="rounded-industrial bg-bg-overlay px-3 py-2">
                      <p className="text-[9px] tracking-section text-muted uppercase">{row.label}</p>
                      <p className="mt-1 text-[11px] text-primary">{row.value}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-8 flex items-center justify-between gap-4 border-t border-border-default pt-6">
                <p className="text-[15px] font-medium text-primary">
                  {price}
                  <span className="ml-0.5 text-[10px] font-normal text-muted">{priceUnit}</span>
                </p>
                {onCta ? (
                  <Button size="cta" onClick={onCta}>
                    {ctaLabel}
                  </Button>
                ) : null}
              </div>
            </CardContent>
          </div>
        </Card>
      </main>
    </div>
  );
}
