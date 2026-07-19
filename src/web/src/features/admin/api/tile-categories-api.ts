import { api } from '@/features/auth/api/auth-api';
import type {
  ListCategoriesApiV1AdminTileCategoriesGetParams,
  TileCategoryAdminItem,
  TileCategoryCreateRequest,
  TileCategoryTreeNode,
  TileCategoryUpdateRequest,
} from '@/shared/api/generated';

export async function fetchCategoryTree() {
  const response = await api.getCategoryTreeApiV1AdminTileCategoriesTreeGet();
  return response.data.data ?? [];
}

export async function fetchCategories(params: ListCategoriesApiV1AdminTileCategoriesGetParams) {
  const response = await api.listCategoriesApiV1AdminTileCategoriesGet(params);
  return response.data.data!;
}

export async function createCategory(payload: TileCategoryCreateRequest) {
  const response = await api.createCategoryApiV1AdminTileCategoriesPost(payload);
  return response.data.data!;
}

export async function updateCategory(categoryId: number, payload: TileCategoryUpdateRequest) {
  const response = await api.updateCategoryApiV1AdminTileCategoriesCategoryIdPut(
    categoryId,
    payload,
  );
  return response.data.data!;
}

export async function enableCategory(categoryId: number) {
  const response = await api.enableCategoryApiV1AdminTileCategoriesCategoryIdEnablePost(categoryId);
  return response.data.data!;
}

export async function disableCategory(categoryId: number) {
  const response = await api.disableCategoryApiV1AdminTileCategoriesCategoryIdDisablePost(categoryId);
  return response.data.data!;
}

export async function deleteCategory(categoryId: number) {
  await api.deleteCategoryApiV1AdminTileCategoriesCategoryIdDelete(categoryId);
}

export function canDeleteCategory(
  category: Pick<TileCategoryAdminItem, 'sku_count' | 'status'>,
): boolean {
  return category.sku_count === 0 && category.status === 'DISABLED';
}

export function flattenCategoryTree(
  nodes: TileCategoryTreeNode[],
): Array<{ node: TileCategoryTreeNode; level: number }> {
  const result: Array<{ node: TileCategoryTreeNode; level: number }> = [];
  const walk = (items: TileCategoryTreeNode[], level: number) => {
    for (const node of items) {
      result.push({ node, level });
      if (node.children?.length) {
        walk(node.children, level + 1);
      }
    }
  };
  walk(nodes, 1);
  return result;
}

export function buildParentOptions(
  tree: TileCategoryTreeNode[],
): Array<{ id: number | null; label: string; level: number }> {
  const options: Array<{ id: number | null; label: string; level: number }> = [
    { id: null, label: '无，创建一级类目', level: 0 },
  ];
  const walk = (nodes: TileCategoryTreeNode[], prefix: string) => {
    for (const node of nodes) {
      if (node.level >= 2) continue;
      const label = prefix ? `${prefix} / ${node.name}` : node.name;
      options.push({ id: node.id, label, level: node.level });
      if (node.children?.length) {
        walk(node.children, label);
      }
    }
  };
  walk(tree, '');
  return options;
}

export type { TileCategoryAdminItem, TileCategoryTreeNode };
