import { PRODUCT_VERSION } from '@shared/product-version';

import { cn } from '@/shared/lib/cn';
import { Badge } from '@/shared/ui/badge';

export interface ProductVersionBadgeProps {
  version?: string;
  className?: string;
}

export function ProductVersionBadge({
  version = PRODUCT_VERSION,
  className,
}: ProductVersionBadgeProps) {
  return (
    <Badge
      variant="version"
      className={cn('version-pill', className)}
      aria-label={`产品版本 ${version}`}
    >
      {version}
    </Badge>
  );
}
