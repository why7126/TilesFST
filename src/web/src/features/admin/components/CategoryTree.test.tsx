import { fireEvent, render, screen, within } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it, vi } from 'vitest';

import type { TileCategoryTreeNode } from '@/shared/api/generated';

import { CategoryTree } from './CategoryTree';

const cssPath = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '../styles/tile-category-management.css',
);
const tileCategoryCss = readFileSync(cssPath, 'utf8');

const tree: TileCategoryTreeNode[] = [
  {
    id: 1,
    name: '岩板-一级',
    code: 'CAT-ROOT',
    level: 1,
    status: 'ENABLED',
    sku_count: 8,
    children_count: 1,
    children: [
      {
        id: 2,
        name: '仿古砖/客厅',
        code: 'CAT-CHILD',
        level: 2,
        status: 'ENABLED',
        sku_count: 3,
        children_count: 0,
        children: [],
      },
    ],
  },
  {
    id: 3,
    name: '通体砖',
    code: 'CAT-PLAIN',
    level: 1,
    status: 'ENABLED',
    sku_count: 5,
    children_count: 0,
    children: [],
  },
];

describe('CategoryTree', () => {
  it('renders only level-1 categories by default and uses plus/minus expand controls', () => {
    const onSelect = vi.fn();
    const { container } = render(
      <CategoryTree
        tree={tree}
        selectedId={null}
        totalCount={3}
        onSelect={onSelect}
      />,
    );

    expect(screen.getByText('岩板-一级')).toBeInTheDocument();
    expect(screen.getByText('通体砖')).toBeInTheDocument();
    expect(screen.queryByText('仿古砖/客厅')).not.toBeInTheDocument();
    expect(container.querySelector('input[type="checkbox"]')).toBeNull();

    const expandButton = screen.getByRole('button', { name: '展开岩板-一级' });
    expect(expandButton).toHaveTextContent('+');
    fireEvent.click(expandButton);

    expect(screen.getByText('仿古砖/客厅')).toBeInTheDocument();
    const collapseButton = screen.getByRole('button', { name: '收起岩板-一级' });
    expect(collapseButton).toHaveTextContent('-');
    expect(collapseButton).toHaveAttribute('aria-expanded', 'true');

    fireEvent.click(collapseButton);
    expect(screen.queryByText('仿古砖/客厅')).not.toBeInTheDocument();
  });

  it('keeps selecting categories separate from expanding nodes', () => {
    const onSelect = vi.fn();
    render(
      <CategoryTree
        tree={tree}
        selectedId={1}
        totalCount={3}
        onSelect={onSelect}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: '展开岩板-一级' }));
    expect(onSelect).not.toHaveBeenCalled();

    const selectedRow = screen.getByTitle('岩板-一级');
    expect(selectedRow).toHaveClass('active');
    fireEvent.click(within(selectedRow).getByText('岩板-一级'));
    expect(onSelect).toHaveBeenCalledWith(1);

    fireEvent.click(screen.getByTitle('仿古砖/客厅'));
    expect(onSelect).toHaveBeenCalledWith(2);
  });

  it('shows category child counts instead of sku counts', () => {
    const onSelect = vi.fn();
    render(
      <CategoryTree
        tree={tree}
        selectedId={null}
        totalCount={3}
        onSelect={onSelect}
      />,
    );

    const allCategories = screen.getByRole('button', { name: /全部类目/ });
    expect(within(allCategories).getByText('2')).toBeInTheDocument();
    expect(within(allCategories).queryByText('16')).not.toBeInTheDocument();

    const rootCategory = screen.getByTitle('岩板-一级');
    expect(within(rootCategory).getByText('1')).toBeInTheDocument();
    expect(within(rootCategory).queryByText('8')).not.toBeInTheDocument();

    const leafCategory = screen.getByTitle('通体砖');
    expect(within(leafCategory).getByText('0')).toBeInTheDocument();
    expect(within(leafCategory).queryByText('5')).not.toBeInTheDocument();
  });

  it('keeps the all-categories active border complete while preserving count alignment', () => {
    render(
      <CategoryTree
        tree={tree}
        selectedId={null}
        totalCount={3}
        onSelect={vi.fn()}
      />,
    );

    const allCategories = screen.getByRole('button', { name: /全部类目/ });
    const firstCategory = screen.getByTitle('岩板-一级');
    const allRow = allCategories.closest('.tree-node-row');
    const firstRow = firstCategory.closest('.tree-node-row');

    expect(allCategories).toHaveClass('all-categories-node');
    expect(allCategories).toHaveClass('active');
    expect(allRow).toHaveClass('all-categories-row');
    expect(allRow).toHaveClass('level-1');
    expect(firstRow).toHaveClass('level-1');
    expect(allRow?.querySelector('.tree-toggle-spacer')).toBeNull();
    expect(firstRow?.querySelector('.tree-toggle, .tree-toggle-spacer')).toBeTruthy();
    expect(tileCategoryCss).toMatch(
      /\.admin-shell \.all-categories-node\s*\{[^}]*padding-left:\s*6px;/s,
    );
    expect(tileCategoryCss).not.toContain('margin-left: -26px');
  });
});
