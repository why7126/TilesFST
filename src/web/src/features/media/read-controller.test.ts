import { afterEach, describe, expect, it, vi } from 'vitest';
import { MediaReadController } from './read-controller';
import type { MediaReadReference } from '@/shared/api/generated';

const ref: MediaReadReference = { resource_type: 'brand_logo', resource_id: '1', variant: 'original' };
const response = (items: MediaReadReference[]) => ({ server_time: '2026-09-08T00:00:00Z', items: items.map(reference => ({ reference, status: 'ready' as const, descriptor: { media_ref: reference.resource_id, variant: 'original' as const, url: 'https://storage.example.test/object', read_mode: 'direct' as const, expires_at: '2026-09-08T00:05:00Z' } })) });
afterEach(() => vi.useRealTimers());
describe('media authorization controller', () => {
  it('deduplicates, batches, and refreshes 30 seconds before expiry using server time', async () => {
    let now = 0;
    const transport = vi.fn(async items => response(items));
    const controller = new MediaReadController(transport, () => now);
    await Promise.all([controller.read(ref), controller.read(ref), controller.read({ ...ref, resource_id: '2' })]);
    expect(transport).toHaveBeenCalledTimes(1);
    expect(transport.mock.calls[0][0]).toHaveLength(2);
    now = 269999;
    await controller.read(ref);
    expect(transport).toHaveBeenCalledTimes(1);
    now = 270000;
    await controller.read(ref);
    expect(transport).toHaveBeenCalledTimes(2);
  });
  it('limits concurrency to four and batches to fifty', async () => {
    const resolvers: (() => void)[] = [];
    const transport = vi.fn(items => new Promise(resolve => resolvers.push(() => resolve(response(items)))));
    const controller = new MediaReadController(transport as never);
    const promises = Array.from({ length: 251 }, (_, index) => controller.read({ ...ref, resource_id: String(index) }));
    await Promise.resolve();
    expect(transport).toHaveBeenCalledTimes(4);
    expect(transport.mock.calls.every(([items]) => items.length <= 50)).toBe(true);
    while (resolvers.length) { resolvers.shift()!(); await new Promise(resolve => setTimeout(resolve, 0)); }
    await Promise.all(promises);
    expect(transport).toHaveBeenCalledTimes(6);
  });
  it('discards late responses after disposal and isolates a new identity', async () => {
    let resolve!: (value: ReturnType<typeof response>) => void;
    const old = new MediaReadController(() => new Promise(done => { resolve = done; }));
    const promise = old.read(ref);
    const assertion = expect(promise).rejects.toHaveProperty('name', 'AbortError');
    await Promise.resolve();
    old.dispose();
    resolve(response([ref]));
    await assertion;
    const transport = vi.fn(async items => response(items));
    await new MediaReadController(transport).read(ref);
    expect(transport).toHaveBeenCalledTimes(1);
  });
  it('cancels one subscriber without invalidating another', async () => {
    const transport = vi.fn(async items => response(items));
    const controller = new MediaReadController(transport);
    const abort = new AbortController();
    const first = controller.read(ref, { signal: abort.signal });
    const assertion = expect(first).rejects.toHaveProperty('name', 'AbortError');
    const second = controller.read(ref);
    abort.abort();
    await assertion;
    await expect(second).resolves.toHaveProperty('read_mode', 'direct');
    expect(transport).toHaveBeenCalledTimes(1);
  });
  it('stops after two recovery attempts and permits bounded manual retry', async () => {
    vi.useFakeTimers();
    const transport = vi.fn(async items => response(items));
    const controller = new MediaReadController(transport);
    const one = controller.recover(ref);
    await vi.advanceTimersByTimeAsync(1000); await one;
    const two = controller.recover(ref);
    await vi.advanceTimersByTimeAsync(3000); await two;
    await expect(controller.recover(ref)).rejects.toThrow('媒体加载失败');
    expect(transport).toHaveBeenCalledTimes(2);
    await controller.manualRetry(ref);
    expect(transport).toHaveBeenCalledTimes(3);
  });
  it('times out transport that ignores cancellation', async () => {
    vi.useFakeTimers();
    const controller = new MediaReadController(() => new Promise(() => {}));
    const promise = controller.read(ref);
    const assertion = expect(promise).rejects.toThrow('媒体加载失败');
    await vi.advanceTimersByTimeAsync(10000);
    await assertion;
    controller.dispose();
  });
});

it('does not automatically retry a denied reference or reuse its earlier URL', async () => {
  const transport = vi.fn(async (items: MediaReadReference[]) => ({ server_time: '2026-09-08T00:00:00Z', items: items.map(reference => ({ reference, status: 'unavailable' as const })) }));
  const controller = new MediaReadController(transport);
  await expect(controller.read(ref)).rejects.toHaveProperty('terminal', true);
  await expect(controller.recover(ref)).rejects.toHaveProperty('terminal', true);
  await expect(controller.read(ref)).rejects.toHaveProperty('terminal', true);
  expect(transport).toHaveBeenCalledTimes(1);
});

it('coalesces concurrent recoveries into one budgeted attempt', async () => {
  vi.useFakeTimers();
  const transport = vi.fn(async items => response(items));
  const controller = new MediaReadController(transport);
  const first = controller.recover(ref);
  const second = controller.recover(ref);
  expect(first).toBe(second);
  await vi.advanceTimersByTimeAsync(1000);
  await Promise.all([first, second]);
  expect(transport).toHaveBeenCalledTimes(1);
});

it('cancels a recovery subscriber without cancelling another or sharing its abort signal', async () => {
  vi.useFakeTimers();
  const transport = vi.fn(async items => response(items));
  const controller = new MediaReadController(transport);
  const abort = new AbortController();
  const first = controller.recover(ref, abort.signal);
  const assertion = expect(first).rejects.toHaveProperty('name', 'AbortError');
  const second = controller.recover(ref);
  abort.abort(); await assertion;
  await vi.advanceTimersByTimeAsync(1000);
  await expect(second).resolves.toHaveProperty('read_mode', 'direct');
  expect(transport).toHaveBeenCalledTimes(1);
});

it('keeps telemetry enums compatible and ignores collection failure', async () => {
  const observations: any[] = [];
  const controller = new MediaReadController(async items => response(items), () => 0, event => { observations.push(event); throw Error('collector unavailable'); });
  await expect(controller.read(ref)).resolves.toHaveProperty('read_mode','direct');
  controller.report(ref,'play','started');
  controller.report(ref,'authorization','unavailable');
  expect(observations.map(event=>[event.result,event.outcome])).toEqual([['success','success'],['success','started'],['failed','unavailable']]);
  expect(observations.every(event=>!('url' in event)&&!('object_key' in event))).toBe(true);
});
