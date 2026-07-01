import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ApiDocsPage } from './ApiDocsPage';
import { fetchApiDocs } from '../../features/admin/api/api-docs-api';
import type { ApiDocsData } from '../../shared/api/generated';

vi.mock('../../features/admin/api/api-docs-api', () => ({
  fetchApiDocs: vi.fn(),
}));

const apiDocsData: ApiDocsData = {
  routes: [
    {
      method: 'GET',
      path: '/api/v1/admin/api-docs',
      tag: 'admin-api-docs',
      summary: '管理端接口文档目录',
      auth_requirement: 'admin',
      included_in_openapi: true,
      operation_id: 'get_api_docs_api_v1_admin_api_docs_get',
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
  ],
  summary: {
    total_routes: 3,
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
    expect(screen.getByText(/未生成/)).toBeInTheDocument();
    expect(screen.getByText('生产环境只读')).toBeInTheDocument();
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
    expect(container.querySelector('.page-summary')).toHaveTextContent('共 3 个接口');
    expect(container.querySelector('.page-right')).toHaveTextContent('当前筛选 1 条');
    expect(container.querySelector('.admin-notice')).not.toBeInTheDocument();
  });

  it('hides Swagger Try It Out entry when production policy is read-only', async () => {
    vi.mocked(fetchApiDocs).mockResolvedValue(apiDocsData);

    render(<ApiDocsPage />);

    const readonlyLink = await screen.findByRole('link', { name: 'Swagger 只读' });
    expect(readonlyLink).toHaveAttribute('href', '/docs');
    expect(screen.getByText('src/web/orval.config.ts')).toBeInTheDocument();
    expect(screen.getByText('src/web/src/shared/api/generated.ts')).toBeInTheDocument();
    expect(screen.getByText('Try It Out 已隐藏')).toBeInTheDocument();
  });
});
