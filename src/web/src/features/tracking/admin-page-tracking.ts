type AdminPageTrackingContext = {
  module: string;
  entity_type: 'admin_page';
  entity_id: string;
  page_title: string;
  route_pattern: string;
};

const adminPageTrackingRules: Array<{
  pattern: string;
  matches: (pathname: string) => boolean;
  context: Omit<AdminPageTrackingContext, 'route_pattern'>;
}> = [
  {
    pattern: '/admin/dashboard',
    matches: (pathname) => pathname === '/admin/dashboard',
    context: {
      module: 'dashboard',
      entity_type: 'admin_page',
      entity_id: 'admin_dashboard',
      page_title: '数据概览',
    },
  },
  {
    pattern: '/admin/tile-skus',
    matches: (pathname) => pathname === '/admin/tile-skus',
    context: {
      module: 'tile_sku',
      entity_type: 'admin_page',
      entity_id: 'admin_tile_skus',
      page_title: '瓷砖 SKU',
    },
  },
  {
    pattern: '/admin/brands',
    matches: (pathname) => pathname === '/admin/brands',
    context: {
      module: 'brand',
      entity_type: 'admin_page',
      entity_id: 'admin_brands',
      page_title: '瓷砖品牌',
    },
  },
  {
    pattern: '/admin/tile-categories',
    matches: (pathname) => pathname === '/admin/tile-categories',
    context: {
      module: 'tile_category',
      entity_type: 'admin_page',
      entity_id: 'admin_tile_categories',
      page_title: '瓷砖类目',
    },
  },
  {
    pattern: '/admin/tile-specs',
    matches: (pathname) => pathname === '/admin/tile-specs',
    context: {
      module: 'tile_spec',
      entity_type: 'admin_page',
      entity_id: 'admin_tile_specs',
      page_title: '瓷砖规格',
    },
  },
  {
    pattern: '/admin/banners',
    matches: (pathname) => pathname === '/admin/banners',
    context: {
      module: 'banner',
      entity_type: 'admin_page',
      entity_id: 'admin_banners',
      page_title: 'Banner 管理',
    },
  },
  {
    pattern: '/admin/profile',
    matches: (pathname) => pathname === '/admin/profile',
    context: {
      module: 'profile',
      entity_type: 'admin_page',
      entity_id: 'admin_profile',
      page_title: '个人资料',
    },
  },
  {
    pattern: '/admin/users',
    matches: (pathname) => pathname === '/admin/users',
    context: {
      module: 'user_management',
      entity_type: 'admin_page',
      entity_id: 'admin_users',
      page_title: '用户管理',
    },
  },
  {
    pattern: '/admin/settings/:tab',
    matches: (pathname) => pathname === '/admin/settings' || pathname.startsWith('/admin/settings/'),
    context: {
      module: 'system_settings',
      entity_type: 'admin_page',
      entity_id: 'admin_settings',
      page_title: '系统设置',
    },
  },
  {
    pattern: '/admin/logs',
    matches: (pathname) => pathname === '/admin/logs',
    context: {
      module: 'log_audit',
      entity_type: 'admin_page',
      entity_id: 'admin_logs',
      page_title: '日志审计',
    },
  },
  {
    pattern: '/admin/api-docs',
    matches: (pathname) => pathname === '/admin/api-docs',
    context: {
      module: 'api_docs',
      entity_type: 'admin_page',
      entity_id: 'admin_api_docs',
      page_title: '接口文档',
    },
  },
];

export function resolveAdminPageTrackingContext(pathname: string): AdminPageTrackingContext {
  const matchedRule = adminPageTrackingRules.find((rule) => rule.matches(pathname));
  if (!matchedRule) {
    return {
      module: 'admin',
      entity_type: 'admin_page',
      entity_id: 'admin_unknown',
      page_title: '管理端页面',
      route_pattern: pathname || '/admin',
    };
  }

  return {
    ...matchedRule.context,
    route_pattern: matchedRule.pattern,
  };
}
