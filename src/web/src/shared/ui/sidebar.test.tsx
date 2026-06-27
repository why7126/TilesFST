import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { PRODUCT_VERSION } from '@shared/product-version';

import { Sidebar } from './sidebar';

const sampleSections = [
  {
    id: 'material',
    title: '材质',
    items: [{ id: 'marble', label: '大理石' }],
  },
];

describe('Sidebar', () => {
  it('renders catalog brand head with product version', () => {
    const { container } = render(<Sidebar sections={sampleSections} />);
    expect(container.textContent).toMatch(/STONEX/);
    const pill = screen.getByLabelText(`产品版本 ${PRODUCT_VERSION}`);
    expect(pill).toHaveTextContent(PRODUCT_VERSION);
    expect(pill).toHaveClass('version-pill');
    expect(pill.className).toMatch(/border-border-chip/);
  });

  it('hides brand head when showBrandHead is false', () => {
    render(<Sidebar sections={sampleSections} showBrandHead={false} />);
    expect(screen.queryByText(PRODUCT_VERSION)).not.toBeInTheDocument();
  });
});
