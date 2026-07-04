import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ApiDocsPage } from './ApiDocsPage';
import { fetchApiDocs } from '../../features/admin/api/api-docs-api';
import type { ApiDocsData, ApiDocsRouteItem } from '../../shared/api/generated';

vi.mock('../../features/admin/api/api-docs-api', () => ({
  fetchApiDocs: vi.fn(),
}));

const apiDocsData: ApiDocsData = {
  routes: [
    {
      method: 'GET',
      path: '/api/v1/admin/api-docs',
      tag: 'admin api/docs',
      summary: '管理端接口文档目录',
      auth_requirement: 'admin',
      included_in_openapi: true,
      operation_id: 'get api/docs',
      orval_method_name: 'getApiDocsApiV1AdminApiDocsGet',
      source: 'openapi',
    },
    {
      method: 'GET',
      path: '/media/{object_key:path}',
      tag: 'media',
      summary: '媒体直出',
      auth_requirement: 'public',
      included_in_openapi: false,
      operation_id: null,
      orval_method_name: null,
      source: 'runtime',
      missing_orval_reason: '未纳入 OpenAPI',
    },
    {
      method: 'GET',
      path: '/health',
      tag: 'health',
      summary: '健康检查',
      auth_requirement: 'public',
      included_in_openapi: true,
      operation_id: 'health_check_health_get',
      orval_method_name: 'healthCheckHealthGet',
      source: 'openapi',
    },
    {
      method: 'GET',
      path: '/docs',
      tag: 'docs',
      summary: 'Swagger UI',
      auth_requirement: 'public',
      included_in_openapi: true,
      operation_id: null,
      orval_method_name: null,
      source: 'runtime',
      missing_orval_reason: '缺少 operationId',
    },
  ],
  summary: {
    total_routes: 4,
    protected_routes: 1,
    orval_mapped_routes: 2,
    non_api_v1_routes: 2,
  },
  environment: {
    app_env: 'production',
    allow_try_it_out: false,
    label: '生产环境只读',
    description: '生产环境展示入口，但隐藏 Swagger Try It Out 调试能力。',
  },
};

function createRoute(index: number): ApiDocsRouteItem {
  const padded = String(index).padStart(2, '0');
  return {
    method: 'GET',
    path: `/api/v1/demo-${padded}`,
    tag: index === 25 ? 'billing' : 'demo',
    summary: `演示接口 ${padded}`,
    auth_requirement: index === 25 ? 'admin' : 'public',
    included_in_openapi: true,
    operation_id: `demo_${padded}_get`,
    orval_method_name: `getDemo${padded}`,
    source: 'openapi',
  };
}

const paginatedApiDocsData: ApiDocsData = {
  ...apiDocsData,
  routes: Array.from({ length: 25 }, (_, index) => createRoute(index + 1)),
  summary: {
    total_routes: 25,
    protected_routes: 1,
    orval_mapped_routes: 25,
    non_api_v1_routes: 0,
  },
};

const methodPaletteApiDocsData: ApiDocsData = {
  ...apiDocsData,
  routes: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'].map((method) => ({
    method,
    path: `/api/v1/method-${method.toLowerCase()}`,
    tag: 'method-palette',
    summary: `${method} 方法色块`,
    auth_requirement: 'admin',
    included_in_openapi: true,
    operation_id: `${method.toLowerCase()}_method_palette`,
    orval_method_name: `${method.toLowerCase()}MethodPalette`,
    source: 'openapi',
  })),
  summary: {
    total_routes: 5,
    protected_routes: 5,
    orval_mapped_routes: 5,
    non_api_v1_routes: 0,
  },
};

describe('ApiDocsPage', () => {
  beforeEach(() => {
    vi.mocked(fetchApiDocs).mockReset();
  });

  it('renders all route families with Orval method names and missing labels', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    expect(await screen.findByText('接口文档')).toBeInTheDocument();
    expect(screen.getByText('getApiDocsApiV1AdminApiDocsGet')).toBeInTheDocument();
    expect(screen.getByText('/media/{object_key:path}')).toBeInTheDocument();
    expect(screen.getAllByText(/未生成/)).toHaveLength(2);
    expect(screen.queryByText('SWAGGER POLICY')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Swagger 策略')).not.toBeInTheDocument();
  });

  it('renders row-level Swagger operation links for OpenAPI routes', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    const routePath = await screen.findByText('/api/v1/admin/api-docs');
    const routeRow = routePath.closest('tr');
    expect(routeRow).not.toBeNull();

    const viewLink = within(routeRow as HTMLTableRowElement).getByRole('link', {
      name: '查看 GET /api/v1/admin/api-docs Swagger 详情',
    });
    const actionCell = viewLink.closest('td');

    expect(viewLink).toHaveTextContent('查看');
    expect(actionCell).toHaveClass('api-docs-action-cell');
    expect(actionCell).toHaveClass('admin-sticky-action-cell');
    expect(screen.getByRole('columnheader', { name: 'ACTION' })).toHaveClass(
      'api-docs-action-cell',
    );
    expect(screen.getByRole('columnheader', { name: 'ACTION' })).toHaveClass(
      'admin-sticky-action-cell',
    );
    expect(viewLink).toHaveAttribute('href', '/docs#/admin%20api%2Fdocs/get%20api%2Fdocs');
    expect(viewLink).toHaveAttribute('target', '_blank');
    expect(viewLink).toHaveAttribute('rel', 'noreferrer');
    expect(viewLink).not.toHaveAttribute('href', expect.stringContaining('token'));
    expect(viewLink).not.toHaveAttribute('href', expect.stringContaining('Bearer'));
    expect(viewLink).not.toHaveAttribute('href', expect.stringContaining('localhost:8000'));

    const pathLink = within(routeRow as HTMLTableRowElement).getByRole('link', {
      name: '通过 PATH 打开 GET /api/v1/admin/api-docs Swagger 详情',
    });
    expect(pathLink).toHaveAttribute('href', '/docs#/admin%20api%2Fdocs/get%20api%2Fdocs');
    expect(pathLink).toHaveAttribute('target', '_blank');
    expect(pathLink).toHaveAttribute('rel', 'noreferrer');
  });

  it('renders disabled row-level Swagger actions for non-OpenAPI and missing-operationId routes', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    const mediaRow = (await screen.findByText('/media/{object_key:path}')).closest('tr');
    expect(mediaRow).not.toBeNull();

    const mediaAction = within(mediaRow as HTMLTableRowElement).getByRole('button', {
      name: /查看 GET \/media\/\{object_key:path\} Swagger 详情不可用/,
    });
    expect(mediaAction).toBeDisabled();
    expect(mediaAction).toHaveAttribute('title', '未纳入 OpenAPI，暂无 Swagger 详情');
    expect(mediaAction).not.toHaveAttribute('href');
    expect(
      within(mediaRow as HTMLTableRowElement).queryByRole('link', {
        name: /通过 PATH 打开 GET \/media\/\{object_key:path\} Swagger 详情/,
      }),
    ).not.toBeInTheDocument();

    const docsRow = (await screen.findByText('/docs')).closest('tr');
    expect(docsRow).not.toBeNull();

    const docsAction = within(docsRow as HTMLTableRowElement).getByRole('button', {
      name: /查看 GET \/docs Swagger 详情不可用/,
    });
    expect(docsAction).toBeDisabled();
    expect(docsAction).toHaveAttribute('title', '缺少 operationId，暂无 Swagger 详情');
    expect(docsAction).not.toHaveAttribute('href');
    expect(
      within(docsRow as HTMLTableRowElement).queryByRole('link', {
        name: /通过 PATH 打开 GET \/docs Swagger 详情/,
      }),
    ).not.toBeInTheDocument();
  });

  it('renders summary metrics with the admin metric card structure', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    await screen.findByText('接口文档');

    const summary = screen.getByLabelText('接口文档摘要');
    const cards = Array.from(summary.querySelectorAll('.metric-card'));

    expect(cards).toHaveLength(4);
    cards.forEach((card) => {
      expect(card.tagName.toLowerCase()).toBe('article');
      expect(card.querySelector('.metric-label')).toBeInTheDocument();
      expect(card.querySelector('.metric-value')).toBeInTheDocument();
      expect(card.querySelector('.metric-desc')).toBeInTheDocument();
      expect(card.querySelector('strong')).not.toBeInTheDocument();
    });
    expect(within(summary).getByText('4')).toHaveClass('metric-value');
    expect(within(summary).getByText('全部运行时接口')).toHaveClass('metric-desc');
  });

  it('renders five distinct method badge classes', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(methodPaletteApiDocsData);

    render(<ApiDocsPage />);

    await screen.findByText('/api/v1/method-get');
    const table = screen.getByRole('table');

    for (const method of ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']) {
      expect(within(table).getByText(method)).toHaveClass(`method-${method.toLowerCase()}`);
    }

    const css = readFileSync(join(process.cwd(), 'src/features/admin/styles/api-docs.css'), 'utf8');
    for (const method of ['get', 'post', 'put', 'patch', 'delete']) {
      expect(css).toMatch(new RegExp(`\\.admin-shell \\.method-${method} \\{[\\s\\S]*?color:`));
    }
    expect(css).not.toContain('.method-post,\n.admin-shell .method-put,\n.admin-shell .method-patch');
  });

  it('filters by Orval method name and keeps admin table feedback stable', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);
    const { container } = render(<ApiDocsPage />);

    await screen.findByText('getApiDocsApiV1AdminApiDocsGet');

    fireEvent.change(screen.getByPlaceholderText('路径、摘要、Tag、Orval 方法名'), {
      target: { value: 'healthCheckHealthGet' },
    });

    await waitFor(() => {
      const table = screen.getByRole('table');
      expect(within(table).getByText('/health')).toBeInTheDocument();
      expect(within(table).queryByText('/api/v1/admin/api-docs')).not.toBeInTheDocument();
    });
    expect(container.querySelector('.page-summary')).toHaveTextContent('共 1 个接口');
    expect(container.querySelector('.page-summary')).not.toHaveTextContent('当前筛选');
    expect(container.querySelector('.page-right')).toBeInTheDocument();
    expect(container.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('removes the redundant route list title and renders admin-list pagination controls', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(paginatedApiDocsData);
    const { container } = render(<ApiDocsPage />);

    await screen.findByText('/api/v1/demo-01');

    const routeList = screen.getByLabelText('接口列表');
    expect(within(routeList).queryByRole('heading', { name: '系统接口' })).not.toBeInTheDocument();
    expect(within(routeList).queryByText('按路径、方法与模块排序')).not.toBeInTheDocument();
    expect(within(routeList).queryByText(/当前\s+25\s+\/\s+25/)).not.toBeInTheDocument();
    expect(container.querySelector('.page-summary')).toHaveTextContent('共 25 个接口');
    expect(container.querySelector('.page-summary')).not.toHaveTextContent('当前筛选');
    expect(container.querySelector('.page-right')).toBeInTheDocument();
    expect(container.querySelector('.page-buttons')).toBeInTheDocument();
    expect(container.querySelector('.page-size-wrap')).toBeInTheDocument();
    expect(container.querySelector('.page-size')).toBeInTheDocument();
    expect(container.querySelector('.page-btn.active')).toHaveTextContent('1');
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '搜索' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: '重置' })).toBeInTheDocument();

    const hero = container.querySelector('.page-hero');
    const summary = container.querySelector('.summary-grid');
    const filter = container.querySelector('.filter-card');
    const table = container.querySelector('[aria-label="接口列表"]');
    expect(
      (hero?.compareDocumentPosition(summary as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      (summary?.compareDocumentPosition(filter as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      (filter?.compareDocumentPosition(table as Element) ?? 0) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it('limits clickable page numbers to five', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue({
      ...apiDocsData,
      routes: Array.from({ length: 130 }, (_, index) => createRoute(index + 1)),
      summary: {
        total_routes: 130,
        protected_routes: 1,
        orval_mapped_routes: 130,
        non_api_v1_routes: 0,
      },
    });

    const { container } = render(<ApiDocsPage />);

    await screen.findByText('/api/v1/demo-01');

    const numericButtons = Array.from(container.querySelectorAll('.page-btn')).filter((button) =>
      /^\d+$/.test(button.textContent ?? ''),
    );
    expect(numericButtons).toHaveLength(5);
  });

  it('uses 20 as default page size and provides the same page-size options as SKU lists', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(paginatedApiDocsData);

    render(<ApiDocsPage />);

    await screen.findByText('/api/v1/demo-01');

    const pageSizeSelect = screen.getByLabelText('每页显示条数') as HTMLSelectElement;
    expect(pageSizeSelect.value).toBe('20');
    expect(Array.from(pageSizeSelect.options).map((option) => option.value)).toEqual([
      '10',
      '20',
      '50',
      '100',
    ]);
  });

  it('shows only the current page routes when pagination changes', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(paginatedApiDocsData);

    render(<ApiDocsPage />);

    const table = await screen.findByRole('table');
    expect(within(table).getByText('/api/v1/demo-01')).toBeInTheDocument();
    expect(within(table).getByText('/api/v1/demo-20')).toBeInTheDocument();
    expect(within(table).queryByText('/api/v1/demo-21')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '下一页' }));

    await waitFor(() => {
      expect(within(table).queryByText('/api/v1/demo-01')).not.toBeInTheDocument();
      expect(within(table).getByText('/api/v1/demo-21')).toBeInTheDocument();
      expect(within(table).getByText('/api/v1/demo-25')).toBeInTheDocument();
    });
    expect(screen.getByRole('button', { current: 'page' })).toHaveTextContent('2');
  });

  it('resets pagination to page 1 when filters change', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(paginatedApiDocsData);

    render(<ApiDocsPage />);

    const table = await screen.findByRole('table');
    fireEvent.click(screen.getByRole('button', { name: '下一页' }));

    await waitFor(() => {
      expect(screen.getByRole('button', { current: 'page' })).toHaveTextContent('2');
    });

    fireEvent.change(screen.getByLabelText('每页显示条数'), {
      target: { value: '10' },
    });

    await waitFor(() => {
      expect(screen.getByRole('button', { current: 'page' })).toHaveTextContent('1');
      expect(within(table).getByText('/api/v1/demo-01')).toBeInTheDocument();
      expect(within(table).queryByText('/api/v1/demo-11')).not.toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '下一页' }));

    await waitFor(() => {
      expect(screen.getByRole('button', { current: 'page' })).toHaveTextContent('2');
    });

    fireEvent.change(screen.getByPlaceholderText('路径、摘要、Tag、Orval 方法名'), {
      target: { value: 'demo-25' },
    });

    await waitFor(() => {
      expect(screen.getByRole('button', { current: 'page' })).toHaveTextContent('1');
      expect(screen.getByText('共 1 个接口')).toBeInTheDocument();
      expect(within(table).getByText('/api/v1/demo-25')).toBeInTheDocument();
      expect(within(table).queryByText('/api/v1/demo-11')).not.toBeInTheDocument();
    });
  });

  it('renders same-origin readonly Swagger link without the Swagger policy panel', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    const openApiLink = await screen.findByRole('link', { name: 'OpenAPI JSON' });
    expect(openApiLink).toHaveAttribute('href', '/openapi.json');

    const readonlyLink = await screen.findByRole('link', { name: 'Swagger 只读' });
    expect(readonlyLink).toHaveAttribute('href', '/docs');
    expect(readonlyLink).not.toHaveAttribute('href', expect.stringContaining('localhost:8000'));
    expect(screen.queryByText('SWAGGER POLICY')).not.toBeInTheDocument();
    expect(screen.queryByText('src/web/orval.config.ts')).not.toBeInTheDocument();
    expect(screen.queryByText('src/web/src/shared/api/generated.ts')).not.toBeInTheDocument();
    expect(screen.queryByText('Try It Out 已隐藏')).not.toBeInTheDocument();
  });

  it('uses same-origin Swagger UI link when Try It Out is allowed', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue({
      ...apiDocsData,
      environment: {
        app_env: 'development',
        allow_try_it_out: true,
        label: '开发环境调试',
        description: '开发环境允许 Swagger Try It Out。',
      },
    });

    render(<ApiDocsPage />);

    const swaggerLink = await screen.findByRole('link', { name: 'Swagger UI' });
    expect(swaggerLink).toHaveAttribute('href', '/docs');
    expect(swaggerLink).not.toHaveAttribute('href', expect.stringContaining('localhost:8000'));
    expect(screen.queryByText('Try It Out 可用')).not.toBeInTheDocument();
    expect(screen.queryByText('SWAGGER POLICY')).not.toBeInTheDocument();
  });
});
