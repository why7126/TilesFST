type SearchNavigationOptions = {
  sourcePage: string;
  scope?: string;
  keyword?: string;
  categoryId?: number | string;
  categoryName?: string;
  categoryLevel?: string;
  brandId?: number | string;
  section?: string;
  requestId?: string;
};

function appendParam(parts: string[], key: string, value: unknown) {
  if (value === undefined || value === null || value === '') return;
  parts.push(`${key}=${encodeURIComponent(String(value).slice(0, 120))}`);
}

export function buildSearchUrl(options: SearchNavigationOptions): string {
  const parts: string[] = [];
  appendParam(parts, 'sourcePage', options.sourcePage);
  appendParam(parts, 'scope', options.scope || 'all');
  appendParam(parts, 'keyword', options.keyword);
  appendParam(parts, 'categoryId', options.categoryId);
  appendParam(parts, 'categoryName', options.categoryName);
  appendParam(parts, 'categoryLevel', options.categoryLevel);
  appendParam(parts, 'brandId', options.brandId);
  appendParam(parts, 'section', options.section);
  appendParam(parts, 'requestId', options.requestId);
  return `/pages/search/index${parts.length ? `?${parts.join('&')}` : ''}`;
}

export function navigateToSearch(options: SearchNavigationOptions) {
  wx.navigateTo({
    url: buildSearchUrl(options),
    fail: () => wx.showToast({ title: '搜索页打开失败，请重试', icon: 'none' }),
  });
}
