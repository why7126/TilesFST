import { acquirePageMedia } from '../../utils/page-media';
import { MediaAbortController, MediaReadFailure } from '../../utils/media-read-controller';
import type { MediaReadReference } from '../../../web/src/shared/api/generated';
type Binding = { scope: ReturnType<typeof acquirePageMedia>; abort: MediaAbortController; epoch: number; reference?: MediaReadReference; recovering?: boolean };
const bindings = new WeakMap<object, Binding>();
Component({
  properties: {
    resourceType: { type: String, value: 'sku_image' }, resourceId: { type: String, optionalTypes: [Number], value: '' },
    mediaId: { type: Number, value: 0 }, variant: { type: String, value: 'thumbnail' },
    src: { type: String, value: '' }, mode: { type: String, value: 'aspectFit' },
    lazyLoad: { type: Boolean, value: true },
  },
  data: { signedUrl: '', readState: 'loading' },
  observers: { 'resourceType,resourceId,mediaId,variant,src': function () { this.loadMedia('initial'); } },
  lifetimes: {
    attached() { this.showMedia(); },
    detached() { this.hideMedia(); },
  },
  pageLifetimes: { show() { this.showMedia(); }, hide() { this.hideMedia(); } },
  methods: {
    showMedia() {
      this.hideMedia();
      bindings.set(this, { scope: acquirePageMedia(this), abort: new MediaAbortController(), epoch: 0 });
      this.loadMedia('initial');
    },
    hideMedia() {
      const binding = bindings.get(this);
      if (binding) { binding.abort.abort(); binding.scope.release(); bindings.delete(this); }
      this.setData({ signedUrl: '' });
    },
    async loadMedia(mode: string) {
      const binding = bindings.get(this);
      if (!binding) return;
      binding.abort.abort(); binding.abort = new MediaAbortController();
      const epoch = ++binding.epoch;
      const ref: MediaReadReference = {
        resource_type: this.properties.resourceType as MediaReadReference['resource_type'], resource_id: String(this.properties.resourceId),
        variant: this.properties.variant as MediaReadReference['variant'],
        ...(this.properties.mediaId ? { media_id: this.properties.mediaId } : {}),
      };
      binding.reference = ref;
      binding.recovering = mode === 'recover';
      if (!ref.resource_id || ref.resource_id === '0') {
        const local = this.properties.src.startsWith('/assets/') ? this.properties.src : '';
        this.setData({ signedUrl: local, readState: local ? 'ready' : 'unavailable' }); return;
      }
      this.setData({ signedUrl: '', readState: mode === 'recover' ? 'refreshing' : 'loading' });
      try {
        const descriptor = await (mode === 'recover' ? binding.scope.controller.recover(ref, binding.abort.signal)
          : mode === 'manual' ? binding.scope.controller.manualRetry(ref, binding.abort.signal)
          : binding.scope.controller.read(ref, { force: true, signal: binding.abort.signal }));
        if (bindings.get(this) === binding && binding.epoch === epoch && !binding.abort.signal.aborted) {
          this.setData({ signedUrl: descriptor.url, readState: descriptor.degraded ? 'degraded' : 'ready' });
        }
      } catch (error) {
        if (bindings.get(this) === binding && binding.epoch === epoch && !binding.abort.signal.aborted) {
          this.setData({ readState: error instanceof MediaReadFailure && error.terminal ? 'unavailable' : 'failed' });
        }
      }
    },
    onImageLoad() {
      const binding = bindings.get(this);
      if (binding?.reference) {
        binding.scope.controller.report(binding.reference, binding.recovering ? 'recovery' : 'load', 'success');
        binding.recovering = false;
      }
    },
    onImageError() {
      const binding = bindings.get(this);
      if (binding?.reference) binding.scope.controller.report(binding.reference, 'load', 'failed');
      this.loadMedia('recover');
    },
    retryMedia() { this.loadMedia('manual'); },
  },
});
