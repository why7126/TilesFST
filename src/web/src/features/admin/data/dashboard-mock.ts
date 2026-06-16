export interface DashboardMetric {
  id: string;
  label: string;
  value: string;
  description: string;
}

export interface DashboardQuickAction {
  id: string;
  title: string;
  description: string;
}

export interface DashboardRecentUpdate {
  id: string;
  updatedAt: string;
  type: string;
  name: string;
  operator: string;
}

export const dashboardMetrics: DashboardMetric[] = [
  { id: 'sku', label: 'SKU 总数', value: '12,860', description: '已维护瓷砖商品' },
  { id: 'brand', label: '品牌数量', value: '128', description: '品牌资料库' },
  { id: 'banner', label: 'Banner 数量', value: '36', description: '展示位素材' },
  { id: 'user', label: '用户数量', value: '42', description: '后台授权账号' },
];

export const dashboardQuickActions: DashboardQuickAction[] = [
  {
    id: 'sku',
    title: '新增 SKU',
    description: '创建新的瓷砖商品与规格信息',
  },
  {
    id: 'brand',
    title: '新增品牌',
    description: '维护品牌名称、Logo 与简介',
  },
  {
    id: 'category',
    title: '新增类目',
    description: '配置瓷砖分类与展示层级',
  },
  {
    id: 'banner',
    title: '新增 Banner',
    description: '创建首页或活动展示 Banner',
  },
];

export const dashboardRecentUpdates: DashboardRecentUpdate[] = [
  {
    id: '1',
    updatedAt: '2026-06-14 21:12',
    type: 'SKU',
    name: 'CALACATTA 900×1800',
    operator: 'admin',
  },
  {
    id: '2',
    updatedAt: '2026-06-14 19:48',
    type: '品牌',
    name: 'MARBLE PRO',
    operator: 'admin',
  },
  {
    id: '3',
    updatedAt: '2026-06-14 18:06',
    type: 'Banner',
    name: '六月新品推荐',
    operator: 'operator01',
  },
  {
    id: '4',
    updatedAt: '2026-06-13 16:32',
    type: '类目',
    name: '仿古砖 / 深色系',
    operator: 'admin',
  },
  {
    id: '5',
    updatedAt: '2026-06-13 11:20',
    type: '系统',
    name: '登录安全策略更新',
    operator: 'system',
  },
];
