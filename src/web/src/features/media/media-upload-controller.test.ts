import { describe, expect, it, vi } from 'vitest';
import type { UploadAuthorization, UploadSessionStatus } from '@/shared/api/generated';
import { MediaUploadTask, type UploadControlTransport, type UploadSnapshot, type PutUpload } from './media-upload-controller';
const PART = 8 * 1024 * 1024;
function setup(size = 24) {
  const file = new File([new Uint8Array(size)], 'synthetic.mp4', { type: 'video/mp4' });
  const states: UploadSnapshot[] = [];
  let status: UploadSessionStatus = { session_id: 'one', state: 'uploading', expires_at: '2099-01-01T00:00:00Z', part_size: PART, part_count: Math.ceil(size / PART) };
  const grant = (part = 1): UploadAuthorization => ({ url: 'https://cos.invalid/private?signature=secret', length: Math.min(PART, size - (part - 1) * PART), expires_at: '2099-01-01T00:00:00Z', part_number: part });
  const transport: UploadControlTransport = {
    create: vi.fn(async () => ({ mode: 'cos_direct' as const, session: status })), query: vi.fn(async () => status),
    renew: vi.fn(async () => ({ session: status, authorization: grant() })),
    authorizePart: vi.fn(async (_id, part) => grant(part)),
    confirm: vi.fn(async () => { status = { ...status, state: 'ready', media: { object_key: 'videos/stable', url: '/media/videos/stable', size, mime_type: 'video/mp4' } }; return status; }),
    cancel: vi.fn(async () => { status = { ...status, state: 'cancelled' }; return status; }),
  };
  const put = vi.fn<PutUpload>(async (_grant, bytes, _signal, progress) => { progress(bytes.size); });
  const proxy = vi.fn(async () => ({ object_key: 'legacy/file', url: '/media/legacy/file' }));
  const wait = vi.fn(async () => {});
  const task = new MediaUploadTask(file, undefined, transport, value => states.push(value), proxy, put, wait);
  return { task, transport, states, put, proxy, wait, setState: (state: string) => { status = { ...status, state }; } };
}
describe('authorized upload controller', () => {
  it('separates byte completion from readiness without leaking credentials', async () => {
    const e = setup(); await e.task.run();
    expect(e.states.some(s => s.stage === 'verifying' && s.progress === 100)).toBe(true);
    expect(e.states.at(-1)?.stage).toBe('uploaded');
    expect(e.proxy).not.toHaveBeenCalled(); expect(JSON.stringify(e.states)).not.toContain('signature=');
  });
  it('limits concurrency to two parts and signs exact final bytes', async () => {
    const e = setup(PART * 2 + 1); let active = 0; let max = 0;
    e.put.mockImplementation(async (grant, bytes, _signal, progress) => {
      active++; max = Math.max(max, active); expect(grant.length).toBe(bytes.size);
      await new Promise(resolve => setTimeout(resolve, 1)); progress(bytes.size); active--;
    });
    await e.task.run(); expect(max).toBe(2); expect(e.put.mock.calls.at(-1)?.[1].size).toBe(1);
  });
  it('keeps completed parts when retrying the same in-memory task', async () => {
    const e = setup(PART + 1); let fail = true;
    e.put.mockImplementation(async (grant, bytes, _signal, progress) => {
      if (grant.part_number === 2 && fail) throw new Error('synthetic failure'); progress(bytes.size);
    });
    await expect(e.task.run()).rejects.toThrow(); fail = false; await e.task.run();
    expect(e.transport.create).toHaveBeenCalledTimes(1);
    expect(e.put.mock.calls.filter(c => c[0].part_number === 1)).toHaveLength(1);
    expect(e.put.mock.calls.filter(c => c[0].part_number === 2)).toHaveLength(5);
  });
  it('never silently switches a failing direct upload to proxy', async () => {
    const e = setup(); e.put.mockRejectedValue(new Error('synthetic failure'));
    await expect(e.task.run()).rejects.toThrow(); expect(e.proxy).not.toHaveBeenCalled();
    expect(e.transport.renew).toHaveBeenCalledTimes(4); expect(e.wait).toHaveBeenCalledTimes(3);
  });
  it('uses proxy only on explicit server capability', async () => {
    const e = setup(); vi.mocked(e.transport.create).mockResolvedValue({ mode: 'proxy' });
    expect((await e.task.run()).object_key).toBe('legacy/file'); expect(e.put).not.toHaveBeenCalled();
  });
  it('ignores late upload completion after cancellation', async () => {
    const e = setup(); let release!: () => void;
    e.put.mockImplementation(() => new Promise<void>(resolve => { release = resolve; }));
    const running = e.task.run(); const rejected = expect(running).rejects.toMatchObject({ name: 'AbortError' });
    await vi.waitFor(() => expect(e.put).toHaveBeenCalled()); await e.task.cancel(); release(); await rejected;
    expect(e.transport.cancel).toHaveBeenCalledWith('one'); expect(e.states.at(-1)?.stage).toBe('cancelled');
    expect(e.transport.confirm).not.toHaveBeenCalled();
  });
  it('periodically confirms to reclaim a crashed verification worker', async () => {
    const e = setup(); e.setState('verifying');
    expect((await e.task.run()).object_key).toBe('videos/stable');
    expect(e.transport.confirm).toHaveBeenCalledTimes(1); expect(e.put).not.toHaveBeenCalled();
  });
});


it('retries the failed image processing stage without retransferring bytes', async () => {
  const e = setup();
  e.transport.query = vi.fn(async () => ({ session_id: 'one', state: 'failed', retryable: true,
    error_code: 30084, expires_at: '2099-01-01T00:00:00Z', part_size: PART, part_count: 1 }));
  e.transport.retryProcessing = vi.fn(async () => ({ session_id: 'one', state: 'ready',
    expires_at: '2099-01-01T00:00:00Z', part_size: PART, part_count: 1,
    media: { object_key: 'images/stable', url: '/media/images/stable', mime_type: 'image/png', size: 24 } }));
  const result = await e.task.run();
  expect(result.object_key).toBe('images/stable');
  expect(e.transport.retryProcessing).toHaveBeenCalledOnce();
  expect(e.transport.confirm).not.toHaveBeenCalled();
  expect(e.put).not.toHaveBeenCalled();
});

it('records client stages once per transition without filenames, keys or authorization', async () => {
  const e = setup(); const events: unknown[] = [];
  const task = new MediaUploadTask(new File(['data'], 'private-client-name.mp4', {type:'video/mp4'}),
    undefined, e.transport, () => {}, e.proxy, e.put, e.wait, 'sku_video', value => {events.push(value);});
  await task.run();
  expect(events).toEqual(expect.arrayContaining([
    expect.objectContaining({action:'start'}),
    expect.objectContaining({action:'stage',stage:'transferring',mode:'cos_direct',file_size_bytes:4}),
    expect.objectContaining({action:'stage',stage:'uploaded'}),
  ]));
  expect(events.filter(value => (value as {stage?:string}).stage === 'transferring')).toHaveLength(1);
  const serialized=JSON.stringify(events);
  expect(serialized).not.toMatch(/private-client-name|signature|videos\/stable|https:/);
});

it('does not let a failing telemetry sink block a completed upload', async () => {
  const e=setup();
  const task=new MediaUploadTask(new File(['data'],'test.mp4',{type:'video/mp4'}), undefined,
    e.transport,()=>{},e.proxy,e.put,e.wait,'sku_video',async()=>{throw new Error('telemetry offline');});
  await expect(task.run()).resolves.toHaveProperty('object_key','videos/stable');
});

it('reports a committed save once and never cancels a published object on disposal', async () => {
  const e=setup(); const observe=vi.fn();
  const task=new MediaUploadTask(new File(['data'],'test.mp4',{type:'video/mp4'}),undefined,
    e.transport,()=>{},e.proxy,e.put,e.wait,'sku_video',observe);
  await task.run(); task.markSaved(); task.markSaved(); await task.cancel();
  expect(observe.mock.calls.filter(([value])=>value.action==='save')).toHaveLength(1);
  expect(e.transport.cancel).not.toHaveBeenCalled();
});
