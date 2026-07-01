import { RotateCcw } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';

import { fetchApiDocs } from '@/features/admin/api/api-docs-api';
import { AdminToast } from '@/features/admin/components/AdminToast';
import '@/features/admin/styles/user-management.css';
import '@/features/admin/styles/api-docs.css';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { ApiDocsData, ApiDocsRouteItem } from '@/shared/api/generated';

const ALL_VALUE = 'all';

const methodOrder = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'];

const authLabels: Record<string, string> = {
  public: '公开',
  login: '登录用户',
  admin: '仅 admin',
  'admin/employee': 'admin / employee',
};

function getAuthLabel(value: string) {
  return authLabels[value] ?? value;
}

function compareRoutes(a: ApiDocsRouteItem, b: ApiDocsRouteItem) {
  const pathCompare = a.path.localeCompare(b.path);
  if (pathCompare !== 0) {
    return pathCompare;
  }

  return methodOrder.indexOf(a.method) - methodOrder.indexOf(b.method);
}

function matchesKeyword(route: ApiDocsRouteItem, keyword: string) {
  if (!keyword) {
    return true;
  }

  const target = [
    route.method,
    route.path,
    route.tag,
    route.summary,
    route.auth_requirement,
    route.operation_id,
    route.orval_method_name,
    route.source,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  return target.includes(keyword.toLowerCase());
}

export function ApiDocsPage() {
  const [data, setData] = useState<ApiDocsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);
  const [keyword, setKeyword] = useState('');
  const [method, setMethod] = useState(ALL_VALUE);
  const [tag, setTag] = useState(ALL_VALUE);
  const [auth, setAuth] = useState(ALL_VALUE);

  const loadDocs = useCallback(async () => {
    setLoading(true);
    try {
      const docs = await fetchApiDocs();
      setData(docs);
    } catch (error) {
      setNotice(getErrorMessage(error, '加载接口文档失败'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDocs();
  }, [loadDocs]);

  useEffect(() => {
    if (!notice) {
      return;
    }

    const timer = window.setTimeout(() => setNotice(null), 3200);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const routes = useMemo(() => data?.routes.slice().sort(compareRoutes) ?? [], [data]);
  const methods = useMemo(() => {
    const values = Array.from(new Set(routes.map((route) => route.method)));
    return values.sort((a, b) => methodOrder.indexOf(a) - methodOrder.indexOf(b));
  }, [routes]);
  const tags = useMemo(() => Array.from(new Set(routes.map((route) => route.tag))).sort(), [routes]);
  const authOptions = useMemo(
    () => Array.from(new Set(routes.map((route) => route.auth_requirement))).sort(),
    [routes],
  );

  const filteredRoutes = useMemo(
    () =>
      routes.filter((route) => {
        if (!matchesKeyword(route, keyword.trim())) {
          return false;
        }
        if (method !== ALL_VALUE && route.method !== method) {
          return false;
        }
        if (tag !== ALL_VALUE && route.tag !== tag) {
          return false;
        }
        if (auth !== ALL_VALUE && route.auth_requirement !== auth) {
          return false;
        }
        return true;
      }),
    [auth, keyword, method, routes, tag],
  );

  const resetFilters = () => {
    setKeyword('');
    setMethod(ALL_VALUE);
    setTag(ALL_VALUE);
    setAuth(ALL_VALUE);
  };

  const tryItOutAllowed = data?.environment.allow_try_it_out ?? false;

  return (
    <>
      <AdminToast message={notice} />
      <section className="page-hero api-docs-hero">
        <div>
          <p className="eyebrow">SYSTEM / API DOCS</p>
          <h1 className="page-title">接口文档</h1>
          <p className="page-desc">
            汇总后端全部运行时接口，包含 OpenAPI、健康检查、媒体直出与未纳入 /api/v1 的路由。
          </p>
        </div>
        <div className="hero-actions">
          <a className="btn" href="/openapi.json" target="_blank" rel="noreferrer">
            OpenAPI JSON
          </a>
          {tryItOutAllowed ? (
            <a className="btn primary" href="/docs" target="_blank" rel="noreferrer">
              Swagger UI
            </a>
          ) : (
            <a
              className="btn primary api-docs-readonly-action"
              href="/docs"
              target="_blank"
              rel="noreferrer"
            >
              Swagger 只读
            </a>
          )}
        </div>
      </section>

      <section className="summary-grid" aria-label="接口文档摘要">
        <div className="metric-card">
          <p className="metric-label">TOTAL ROUTES</p>
          <strong>{data?.summary.total_routes ?? '--'}</strong>
          <span>全部运行时接口</span>
        </div>
        <div className="metric-card">
          <p className="metric-label">AUTH ROUTES</p>
          <strong>{data?.summary.protected_routes ?? '--'}</strong>
          <span>需要登录或管理员权限</span>
        </div>
        <div className="metric-card">
          <p className="metric-label">ORVAL</p>
          <strong>{data?.summary.orval_mapped_routes ?? '--'}</strong>
          <span>已生成前端方法名</span>
        </div>
        <div className="metric-card">
          <p className="metric-label">NON API V1</p>
          <strong>{data?.summary.non_api_v1_routes ?? '--'}</strong>
          <span>健康检查、媒体与文档路由</span>
        </div>
      </section>

      <section className="filter-card api-docs-filter" aria-label="接口筛选">
        <div className="api-docs-filter-grid">
          <label>
            <span className="field-label">SEARCH</span>
            <input
              className="input"
              value={keyword}
              onChange={(event) => setKeyword(event.target.value)}
              placeholder="路径、摘要、Tag、Orval 方法名"
            />
          </label>
          <label>
            <span className="field-label">METHOD</span>
            <select
              className="select"
              value={method}
              onChange={(event) => setMethod(event.target.value)}
            >
              <option value={ALL_VALUE}>全部方法</option>
              {methods.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">TAG</span>
            <select
              className="select"
              value={tag}
              onChange={(event) => setTag(event.target.value)}
            >
              <option value={ALL_VALUE}>全部模块</option>
              {tags.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">AUTH</span>
            <select
              className="select"
              value={auth}
              onChange={(event) => setAuth(event.target.value)}
            >
              <option value={ALL_VALUE}>全部权限</option>
              {authOptions.map((item) => (
                <option key={item} value={item}>
                  {getAuthLabel(item)}
                </option>
              ))}
            </select>
          </label>
          <button className="btn" type="button" onClick={resetFilters}>
            <RotateCcw size={14} aria-hidden />
            重置
          </button>
        </div>
      </section>

      <section className="table-card api-docs-swagger-panel" aria-label="Swagger 策略">
        <div>
          <p className="section-note">SWAGGER POLICY</p>
          <h2 className="section-title">{data?.environment.label ?? '环境策略加载中'}</h2>
          <p>{data?.environment.description ?? '正在读取当前环境的 Swagger 调试策略。'}</p>
          <ul className="api-docs-source-list" aria-label="文档与生成源">
            <li>
              长期索引：<code>docs/03-api-index.md</code>
            </li>
            <li>
              OpenAPI：<code>/openapi.json</code>
            </li>
            <li>
              Orval：<code>src/web/orval.config.ts</code> →{' '}
              <code>src/web/src/shared/api/generated.ts</code>
            </li>
          </ul>
        </div>
        <span className={`badge ${tryItOutAllowed ? 'enabled' : 'disabled'}`}>
          {tryItOutAllowed ? 'Try It Out 可用' : 'Try It Out 已隐藏'}
        </span>
      </section>

      <section className="table-card" aria-label="接口列表">
        <div className="table-toolbar">
          <div>
            <h2 className="section-title">系统接口</h2>
            <span className="section-note">按路径、方法与模块排序</span>
          </div>
          <span className="table-count">
            当前 <strong>{filteredRoutes.length}</strong> / {routes.length}
          </span>
        </div>
        <div className="api-docs-table-wrap">
          <table className="api-docs-table">
            <thead>
              <tr>
                <th>METHOD</th>
                <th>PATH</th>
                <th>TAG</th>
                <th>SUMMARY</th>
                <th>AUTH</th>
                <th>OPENAPI</th>
                <th>ORVAL METHOD</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={7} className="api-docs-empty">
                    加载接口文档中...
                  </td>
                </tr>
              ) : filteredRoutes.length > 0 ? (
                filteredRoutes.map((route) => (
                  <tr key={`${route.method}-${route.path}`}>
                    <td>
                      <span className={`api-docs-method method-${route.method.toLowerCase()}`}>
                        {route.method}
                      </span>
                    </td>
                    <td>
                      <code className="api-docs-path">{route.path}</code>
                      <span className="api-docs-source">{route.source}</span>
                    </td>
                    <td>{route.tag}</td>
                    <td>{route.summary}</td>
                    <td>{getAuthLabel(route.auth_requirement)}</td>
                    <td>
                      <span className={`badge ${route.included_in_openapi ? 'enabled' : 'disabled'}`}>
                        {route.included_in_openapi ? '已纳入' : '未纳入'}
                      </span>
                    </td>
                    <td>
                      {route.orval_method_name ? (
                        <code className="api-docs-orval">{route.orval_method_name}</code>
                      ) : (
                        <span className="api-docs-missing">
                          未生成
                          {route.missing_orval_reason ? ` · ${route.missing_orval_reason}` : ''}
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="api-docs-empty">
                    暂无匹配接口
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <span className="page-summary">共 {routes.length} 个接口</span>
          <div className="page-right">当前筛选 {filteredRoutes.length} 条</div>
        </div>
      </section>
    </>
  );
}
