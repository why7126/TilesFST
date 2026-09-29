import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import vm from 'node:vm';
import ts from 'typescript';
import { afterEach, expect, it, vi } from 'vitest';
const root = resolve(process.cwd(), existsSync(resolve(process.cwd(), 'src/miniapp/utils')) ? 'src/miniapp/utils' : '../miniapp/utils');
const ref = { resource_type: 'sku_image', resource_id: '1', variant: 'original' };
const data = (items: typeof ref[]) => ({ server_time: '2026-09-08T00:00:00Z', items: items.map(reference => ({ reference, status: 'ready', descriptor: { media_ref: '1', variant: 'original', read_mode: 'direct', url: 'https://storage.example.test/image', expires_at: '2026-09-08T00:05:00Z' } })) });
function harness(extension: string, request: ReturnType<typeof vi.fn>) {
  function load(name: string): any {
    let source = readFileSync(resolve(root, `${name}.${extension}`), 'utf8');
    if (extension === 'ts') source = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.CommonJS } }).outputText;
    const module = { exports: {} };
    vm.runInNewContext(source, { module, exports: module.exports, setTimeout, clearTimeout, Date, Promise, Map, Set,
      wx: { getPerformance: () => ({ now: () => 0 }) },
      require: (path: string) => path === '../services/api' ? { request } : load('media-read-controller'),
    });
    return module.exports;
  }
  return load('media-read');
}
afterEach(() => vi.useRealTimers());
for (const extension of ['js', 'ts']) {
  it(`${extension}: foreground reauthorizes and hide cancels late rendering`, async () => {
    let done: (value: unknown) => void = () => {};
    const abort = vi.fn();
    const request = vi.fn((_path, options) => { options.onRequestTask({ abort }); return new Promise(resolve => { done = resolve; }); });
    const { MiniappMediaScope } = harness(extension, request);
    const scope = new MiniappMediaScope(); scope.show();
    const promise = scope.read(ref); const assertion = expect(promise).rejects.toHaveProperty('name', 'AbortError');
    await Promise.resolve(); scope.hide(); done(data([ref])); await assertion;
    expect(abort).toHaveBeenCalledTimes(1);
    scope.show(); const fresh = scope.read(ref); await Promise.resolve(); done(data([ref])); await fresh;
    expect(request).toHaveBeenCalledTimes(2);
    expect(request.mock.calls[0][1]).toMatchObject({ singleAttempt: true, timeout: 10000, method: 'POST' });
    scope.hide();
  });
  it(`${extension}: switching media invalidates old subscriber`, async () => {
    let done: (value: unknown) => void = () => {};
    const request = vi.fn(() => new Promise(resolve => { done = resolve; }));
    const { MiniappMediaScope } = harness(extension, request);
    const scope = new MiniappMediaScope(); scope.show();
    const promise = scope.read(ref); const assertion = expect(promise).rejects.toHaveProperty('name', 'AbortError');
    await Promise.resolve(); scope.selectMedia(); done(data([ref])); await assertion; scope.hide();
  });
  it(`${extension}: offline failures expose safe errors and stop after two recoveries`, async () => {
    vi.useFakeTimers();
    const request = vi.fn(async () => { throw Error('internal signed URL must not escape'); });
    const { MiniappMediaScope } = harness(extension, request);
    const scope = new MiniappMediaScope(); scope.show();
    await expect(scope.read(ref)).rejects.toThrow('媒体加载失败');
    for (const delay of [1000, 3000]) {
      const recovery = scope.read(ref, true); const assertion = expect(recovery).rejects.toThrow('媒体加载失败');
      await vi.advanceTimersByTimeAsync(delay); await assertion;
    }
    await expect(scope.read(ref, true)).rejects.toThrow('媒体加载失败');
    expect(request).toHaveBeenCalledTimes(3); scope.hide();
  });
}

for (const extension of ['js', 'ts']) {
  it(`${extension}: actual request adapter preserves fallback but singleAttempt exposes abort and safe headers`, async () => {
    let source = readFileSync(resolve(root, `../services/api.${extension}`), 'utf8');
    if (extension === 'ts') source = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.CommonJS } }).outputText;
    const calls: any[] = [];
    const metrics: any[] = [];
    const abort = vi.fn();
    const module = { exports: {} as any };
    vm.runInNewContext(source, { module, exports: module.exports, Date, Promise, Math,
      getApp: () => ({ globalData: { apiBaseUrl: 'https://primary.example.test', apiFallbackBaseUrls: ['https://fallback.example.test'] } }),
      wx: { request: (options: any) => { calls.push(options); Promise.resolve().then(() => options.fail({ errMsg: 'offline' })); return { abort }; } },
      require: (name: string) => name.includes('env') ? { miniappApiConfig: { apiBaseUrl: 'https://primary.example.test' } } : { reportPerformanceMetric: (value: unknown) => metrics.push(value) },
    });
    const receive = vi.fn();
    await expect(module.exports.request('/api/v1/media/read-authorizations', { singleAttempt: true, onRequestTask: receive })).rejects.toBeDefined();
    expect(calls).toHaveLength(1);
    expect(metrics[0].page_key).toBe('/media-read');
    expect(receive).toHaveBeenCalledWith({ abort });
    expect(calls[0].header['x-client-type']).toBe('wechat_miniapp');
    expect(calls[0]).not.toHaveProperty('singleAttempt');
    expect(calls[0]).not.toHaveProperty('onRequestTask');
    calls.length = 0;
    await expect(module.exports.request('/api/v1/products')).rejects.toBeDefined();
    expect(calls).toHaveLength(2);
  });
}
