import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { PRODUCT_VERSION } from '@shared/product-version';

import { ProductVersionBadge } from './product-version-badge';

describe('ProductVersionBadge', () => {
  it('renders version pill with semantic token classes', () => {
    render(<ProductVersionBadge />);
    const pill = screen.getByLabelText(`产品版本 ${PRODUCT_VERSION}`);
    expect(pill).toHaveTextContent(PRODUCT_VERSION);
    expect(pill).toHaveClass('version-pill');
    expect(pill.className).toMatch(/border-border-chip/);
    expect(pill.className).toMatch(/text-muted/);
    expect(pill.className).toMatch(/rounded-industrial/);
  });

  it('supports custom version prop', () => {
    render(<ProductVersionBadge version="v9.9.9" />);
    expect(screen.getByLabelText('产品版本 v9.9.9')).toHaveTextContent('v9.9.9');
  });
});
