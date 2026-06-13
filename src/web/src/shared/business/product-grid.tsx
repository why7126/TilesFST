import * as React from 'react';

import type { ProductGridEntry, TextureSwatch } from '@shared/business/types';
import { cn } from '@/shared/lib/cn';

import { FeaturedCard, type FeaturedCardProps } from './featured-card';
import { ProductCard, type ProductCardActionConfig } from './product-card';
import { TextureRow } from './texture-row';

export interface ProductGridProps extends React.HTMLAttributes<HTMLDivElement> {
  items: ProductGridEntry[];
  /** Optional texture swatch row rendered below the grid — ui-design §5.9 */
  textures?: TextureSwatch[];
  /** Icon actions applied to all standard product cards */
  productActions?: ProductCardActionConfig[];
  getProductActions?: (productId: string) => ProductCardActionConfig[];
}

function ProductGrid({
  items,
  textures,
  productActions,
  getProductActions,
  className,
  ...props
}: ProductGridProps) {
  return (
    <div className={cn('space-y-0', className)} {...props}>
      <div className="grid grid-cols-3 gap-3">
        {items.map((entry) => {
          if (entry.kind === 'featured') {
            return <FeaturedCard key={entry.data.id} product={entry.data} />;
          }

          const actions = getProductActions?.(entry.data.id) ?? productActions ?? [];

          return (
            <ProductCard key={entry.data.id} product={entry.data} actions={actions} />
          );
        })}
      </div>

      {textures && textures.length > 0 ? <TextureRow items={textures} /> : null}
    </div>
  );
}

export { ProductGrid };
export type { FeaturedCardProps };
