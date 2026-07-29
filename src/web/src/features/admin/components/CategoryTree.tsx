import type { TileCategoryTreeNode } from '@/shared/api/generated';

import { flattenCategoryTree } from '../api/tile-categories-api';

interface CategoryTreeProps {
  tree: TileCategoryTreeNode[];
  selectedId: number | null;
  totalCount: number;
  totalSku: number;
  onSelect: (id: number | null) => void;
}

export function CategoryTree({
  tree,
  selectedId,
  totalCount,
  totalSku,
  onSelect,
}: CategoryTreeProps) {
  const flat = flattenCategoryTree(tree);

  return (
    <aside className="tree-card" aria-label="类目树">
      <div className="tree-top">
        <span className="tree-title">类目树</span>
        <span className="section-note">{totalCount} 项</span>
      </div>
      <button
        type="button"
        className={`tree-node${selectedId === null ? ' active' : ''}`}
        onClick={() => onSelect(null)}
      >
        <span className="dot" aria-hidden />
        <span className="tree-name">全部类目</span>
        <span className="tree-count">{totalSku.toLocaleString('zh-CN')}</span>
      </button>
      {flat.map(({ node, level }) => (
        <button
          key={node.id}
          type="button"
          className={`tree-node level-${level}${selectedId === node.id ? ' active' : ''}`}
          onClick={() => onSelect(node.id)}
          title={node.name}
        >
          <span className="dot" aria-hidden />
          <span className="tree-name">{node.name}</span>
          <span className="tree-count">{node.sku_count.toLocaleString('zh-CN')}</span>
        </button>
      ))}
    </aside>
  );
}
