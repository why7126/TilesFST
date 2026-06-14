import { HeartIcon } from 'lucide-react';
import * as React from 'react';

import type { FeaturedCardData } from '@shared/business/types';
import { cn } from '@/shared/lib/cn';
import { Badge } from '@/shared/ui/badge';
import { Button } from '@/shared/ui/button';

import { ProductCardAction } from './product-card-action';

export interface FeaturedCardProps extends React.HTMLAttributes<HTMLElement> {
  product: FeaturedCardData;
}

const FeaturedCard = React.forwardRef<HTMLElement, FeaturedCardProps>(
  ({ product, className, ...props }, ref) => {
    const {
      name,
      spec,
      price,
      priceUnit = '/m²',
      imageUrl,
      imageAlt,
      badges = [],
      specs,
      ctaLabel = '查看详情',
      onCta,
      onFavorite,
      favoriteLabel = '收藏',
      href,
      onClick,
    } = product;

    const body = (
      <div className="grid grid-cols-2">
        <div className="min-h-[180px] overflow-hidden bg-bg-overlay">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={imageAlt ?? name}
              className="size-full min-h-[180px] object-cover transition-transform duration-[400ms] ease-out group-hover:scale-[1.03]"
            />
          ) : null}
        </div>

        <div className="flex flex-col justify-between p-5">
          <div>
            {badges.length > 0 ? (
              <div className="mb-3 flex flex-wrap gap-[5px]">
                {badges.map((badge) => (
                  <Badge key={`${badge.variant}-${badge.label}`} variant={badge.variant}>
                    {badge.label}
                  </Badge>
                ))}
              </div>
            ) : null}

            <h3 className="text-[18px] font-normal text-primary">{name}</h3>
            <p className="mt-2 text-[11px] leading-[1.5] text-muted">{spec}</p>

            <div className="mt-4 grid grid-cols-2 gap-2">
              {specs.map((item) => (
                <div
                  key={`${item.label}-${item.value}`}
                  className="rounded-industrial bg-bg-overlay px-3 py-2"
                >
                  <p className="text-[9px] tracking-section text-muted uppercase">{item.label}</p>
                  <p className="mt-1 text-[11px] text-primary">{item.value}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-5 flex items-center justify-between gap-3">
            <p className="text-[15px] font-medium text-primary">
              {price}
              <span className="ml-0.5 text-[10px] font-normal text-muted">{priceUnit}</span>
            </p>

            <div className="flex items-center gap-2">
              {onFavorite ? (
                <ProductCardAction icon={HeartIcon} label={favoriteLabel} onClick={onFavorite} />
              ) : null}
              {onCta ? (
                <Button type="button" size="cta" onClick={onCta}>
                  {ctaLabel}
                </Button>
              ) : null}
            </div>
          </div>
        </div>
      </div>
    );

    const surfaceClass = cn(
      'group col-span-2 overflow-hidden rounded-card border border-border-default bg-surface',
      className,
    );

    if (href) {
      return (
        <a ref={ref as React.Ref<HTMLAnchorElement>} href={href} className={cn(surfaceClass, 'block')} {...props}>
          {body}
        </a>
      );
    }

    if (onClick) {
      return (
        <Button
          ref={ref as React.Ref<HTMLButtonElement>}
          type="button"
          variant="ghost"
          onClick={onClick}
          className={cn(
            surfaceClass,
            'h-auto w-full justify-start p-0 text-left font-normal hover:bg-surface',
          )}
          {...props}
        >
          {body}
        </Button>
      );
    }

    return (
      <article ref={ref as React.Ref<HTMLElement>} className={surfaceClass} {...props}>
        {body}
      </article>
    );
  },
);
FeaturedCard.displayName = 'FeaturedCard';

export { FeaturedCard };
