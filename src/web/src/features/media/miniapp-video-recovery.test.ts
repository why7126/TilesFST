import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import vm from 'node:vm';
import ts from 'typescript';
import { expect, it, vi } from 'vitest';

function harness(extension: string) {
  let definition: any;
  const video = { seek: vi.fn(), play: vi.fn(), pause: vi.fn(), requestFullScreen: vi.fn() };
  const report = vi.fn();
  const read = vi.fn(async () => ({ url: 'https://storage.example.test/renewed' }));
  let source = readFileSync(resolve(process.cwd(), `../miniapp/pages/tile-detail/index.${extension}`), 'utf8');
  if (extension === 'ts') source = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.CommonJS } }).outputText;
  vm.runInNewContext(source, {
    exports: {}, WeakMap, Date, Promise,
    Page: (value: any) => { definition = value; },
    wx: { createVideoContext: () => video },
    require: (name: string) => name.endsWith('page-media')
      ? { readPageMedia: read, isPageMediaActive: () => true, reportPageMedia: report }
      : { track: vi.fn() },
  });
  const patches: any[] = [];
  const page = { ...definition, data: { ...definition.data, product: { product_id: 136, media: [{ media_id: 7, media_type: 'video', url: 'https://storage.example.test/old' }] } }, setData(patch: any) { patches.push(patch); Object.assign(this.data, patch); } };
  const event = (currentTime = 0) => ({ currentTarget: { dataset: { id: 7 } }, detail: { currentTime } });
  return { page, video, read, report, patches, event };
}

for (const extension of ['ts', 'js']) {
  for (const playing of [false, true]) {
    it(`${extension}: renewed video preserves ${playing ? 'playing' : 'paused'} intent and verifies the restored position`, async () => {
      const h = harness(extension);
      if (playing) h.page.onVideoPlay(h.event());
      else h.page.onVideoPause(h.event());
      h.page.onVideoTimeUpdate(h.event(121));
      h.page.onMediaError(h.event());
      await vi.waitFor(() => expect(h.patches.some(p => p['product.media[0].url']?.includes('renewed'))).toBe(true));
      // Source replacement can emit pause before metadata; it must not erase user intent.
      h.page.onVideoPause(h.event());
      h.page.onVideoMetadata(h.event());
      expect(h.video.seek).toHaveBeenCalledWith(121);
      expect(h.video.play).toHaveBeenCalledTimes(playing ? 1 : 0);
      h.page.onVideoTimeUpdate(h.event(0));
      expect(h.report.mock.calls.filter(c => c[2] === 'recovery')).toHaveLength(0);
      h.page.onVideoTimeUpdate(h.event(120.5));
      expect(h.report.mock.calls.filter(c => c[2] === 'recovery')).toHaveLength(1);
      expect(h.report).toHaveBeenCalledWith(h.page, expect.objectContaining({ media_id: 7 }), 'recovery', 'success');
    });
  }
}
