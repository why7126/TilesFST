import { useState } from 'react';

import type { TileCategoryTreeNode } from '@/shared/api/generated';

interface CategoryTreeProps {
  tree: TileCategoryTreeNode[];
  selectedId: number | null;
  totalCount: number;
  onSelect: (id: number | null) => void;
}

export function CategoryTree({
  tree,
  selectedId,
  totalCount,
  onSelect,
}: CategoryTreeProps) {
  const [expandedIds, setExpandedIds] = useState<Set<number>>(() => new Set());

  const toggleExpanded = (id: number) => {
    setExpandedIds((current) => {
      const next = new Set(current);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const renderNode = (node: TileCategoryTreeNode, level: number) => {
    const children = node.children ?? [];
    const hasChildren = children.length > 0;
    const expanded = expandedIds.has(node.id);
    const childCount = node.children_count ?? children.length;

    return (
      <div key={node.id} className="tree-node-wrap">
        <div className={`tree-node-row level-${level}`}>
          {hasChildren ? (
            <button
              type="button"
              className="tree-toggle"
              aria-label={`${expanded ? '收起' : '展开'}${node.name}`}
              aria-expanded={expanded}
              onClick={() => toggleExpanded(node.id)}
            >
              {expanded ? '-' : '+'}
            </button>
          ) : (
            <span className="tree-toggle-spacer" aria-hidden />
          )}
          <button
            type="button"
            className={`tree-node${selectedId === node.id ? ' active' : ''}`}
            onClick={() => onSelect(node.id)}
            title={node.name}
          >
            <span className="tree-name">{node.name}</span>
            <span className="tree-count">{childCount.toLocaleString('zh-CN')}</span>
          </button>
        </div>
        {hasChildren && expanded ? children.map((child) => renderNode(child, level + 1)) : null}
      </div>
    );
  };

  return (
    <aside className="tree-card" aria-label="类目树">
      <div className="tree-top">
        <span className="tree-title">类目树</span>
        <span className="section-note">{totalCount} 项</span>
      </div>
      <div className="tree-node-row all-categories-row level-1">
        <button
          type="button"
          className={`tree-node all-categories-node${selectedId === null ? ' active' : ''}`}
          onClick={() => onSelect(null)}
        >
          <span className="tree-name">全部类目</span>
          <span className="tree-count">{tree.length.toLocaleString('zh-CN')}</span>
        </button>
      </div>
      {tree.map((node) => renderNode(node, 1))}
    </aside>
  );
}
