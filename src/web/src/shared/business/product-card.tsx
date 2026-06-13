import type { LucideIcon } from 'lucide-react';
import * as React from 'react';

import type { ProductCardData } from '@shared/business/types';
import { cn } from '@/shared/lib/cn';
import { Badge } from '@/shared/ui/badge';

import { ProductCardAction } from './product-card-action';

export interface ProductCardActionConfig {
  id: string;
  label: string;
  icon: LucideIcon;
  onClick?: () => void;
}

export interface ProductCardProps extends React.HTMLAttributes<HTMLElement> {
  product: ProductCardData;
  actions?: ProductCardActionConfig[];
}

const cardSurfaceClass =
  'group overflow-hidden rounded-card border border-border-default bg-surface text-primary';

const ProductCard = React.forwardRef<HTMLElement, ProductCardProps>(
  ({ product, actions = [], className, ...props }, ref) => {
    const {
      name,
      spec,
      price,
      priceUnit = '/m²',
      imageUrl,
      imageAlt,
      badges = [],
      href,
      onClick,
    } = product;

    const body = (
      <>
        <div className="h-[130px] overflow-hidden bg-bg-overlay">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={imageAlt ?? name}
              className="size-full object-cover transition-transform duration-[400ms] ease-out group-hover:scale-[1.03]"
            />
          ) : null}
        </div>

        <div className="px-3.5 pb-3.5 pt-3">
          {badges.length > 0 ? (
            <div className="mb-2 flex flex-wrap gap-[5px]">
              {badges.map((badge) => (
                <Badge key={`${badge.variant}-${badge.label}`} variant={badge.variant}>
                  {badge.label}
                </Badge>
              ))}
            </div>
          ) : null}

          <h3 className="text-[13px] font-medium text-primary">{name}</h3>
          <p className="mt-1 text-[11px] leading-[1.5] text-muted">{spec}</p>

          <div className="mt-3 flex items-center justify-between gap-2">
            <p className="text-[15px] font-medium text-primary">
              {price}
              <span className="ml-0.5 text-[10px] font-normal text-muted">{priceUnit}</span>
            </p>

            {actions.length > 0 ? (
              <div className="flex items-center gap-[5px]">
                {actions.map((action) => (
                  <ProductCardAction
                    key={action.id}
                    icon={action.icon}
                    label={action.label}
                    onClick={action.onClick}
                  />
                ))}
              </div>
            ) : null}
          </div>
        </div>
      </>
    );

    if (href) {
      return (
        <a
          ref={ref as React.Ref<HTMLAnchorElement>}
          href={href}
          className={cn(cardSurfaceClass, 'block', className)}
          {...props}
        >
          {body}
        </a>
      );
    }

    if (onClick) {
      return (
        <button
          ref={ref as React.Ref<HTMLButtonElement>}
          type="button"
          onClick={onClick}
          className={cn(cardSurfaceClass, 'w-full text-left', className)}
          {...props}
        >
          {body}
        </button>
      );
    }

    return (
      <article ref={ref as React.Ref<HTMLElement>} className={cn(cardSurfaceClass, className)} {...props}>
        {body}
      </article>
    );
  },
);
ProductCard.displayName = 'ProductCard';

export { ProductCard };
