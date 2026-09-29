import { createContext, useContext, useEffect, useMemo, useRef, useState, type ImgHTMLAttributes, type VideoHTMLAttributes, type ReactNode } from 'react';
import { useAuthStore } from '@/features/auth/store/auth-store';
import type { MediaReadReference } from '@/shared/api/generated';
import { MediaReadStatus, type MediaReadState } from '@/shared/ui/media-read-status';
import { createMediaReadController } from './media-read-api';
import { MediaReadFailure, type MediaReadObservation } from './read-controller';

const MediaContext = createContext<ReturnType<typeof createMediaReadController> | null>(null);
export function MediaReadProvider({ children, scope = 'admin' }: { children: ReactNode; scope?: 'admin' | 'public' }) {
  const token = useAuthStore(state => state.token);
  const [foreground, setForeground] = useState(0);
  const controller = useMemo(() => createMediaReadController(scope), [scope, token, foreground]);
  useEffect(() => () => controller.dispose(), [controller]);
  useEffect(() => {
    const changed = () => { if (document.hidden) controller.dispose(); else setForeground(value => value + 1); };
    document.addEventListener('visibilitychange', changed);
    return () => document.removeEventListener('visibilitychange', changed);
  }, [controller]);
  return <MediaContext.Provider value={controller}>{children}</MediaContext.Provider>;
}

export function useAuthorizedMedia(reference?: MediaReadReference, localUrl?: string) {
  const shared = useContext(MediaContext);
  const controller = useMemo(() => shared ?? createMediaReadController('admin'), [shared]);
  useEffect(() => () => { if (!shared) controller.dispose(); }, [controller, shared]);
  const identity = JSON.stringify([reference ?? null, localUrl ?? null]);
  const [value, setValue] = useState<{ identity: string; owner: typeof controller; url?: string; state: MediaReadState }>({ identity, owner: controller, state: 'loading' });
  const generation = useRef(0);
  const abort = useRef(new AbortController());
  const safeLocal = localUrl?.startsWith('blob:') || localUrl?.startsWith('/assets/') ? localUrl : undefined;
  async function load(mode: 'initial' | 'recover' | 'manual') {
    const epoch = generation.current;
    if (!reference) { setValue({ identity, owner: controller, url: safeLocal, state: safeLocal ? 'ready' : 'unavailable' }); return; }
    setValue({ identity, owner: controller, state: mode === 'recover' ? 'refreshing' : 'loading' });
    try {
      const descriptor = await (mode === 'recover' ? controller.recover(reference, abort.current.signal)
        : mode === 'manual' ? controller.manualRetry(reference, abort.current.signal)
        : controller.read(reference, { force: true, signal: abort.current.signal }));
      if (epoch === generation.current && !abort.current.signal.aborted) setValue({ identity, owner: controller, url: descriptor.url, state: descriptor.degraded ? 'degraded' : 'ready' });
    } catch (error) {
      if (epoch !== generation.current || abort.current.signal.aborted || (error as Error)?.name === 'AbortError') return;
      setValue({ identity, owner: controller, state: error instanceof MediaReadFailure && error.terminal ? 'unavailable' : navigator.onLine ? 'failed' : 'offline' });
    }
  }
  useEffect(() => {
    generation.current++;
    abort.current = new AbortController();
    void load('initial');
    return () => { generation.current++; abort.current.abort(); };
  }, [identity, safeLocal, controller]);
  return { url: value.identity === identity && value.owner === controller ? value.url : undefined, state: value.identity === identity && value.owner === controller ? value.state : 'loading' as MediaReadState,
    report: (phase: MediaReadObservation['phase'], result: MediaReadObservation['outcome']) => { if (reference) controller.report(reference, phase, result); },
    recover: () => load('recover'), retry: () => load('manual') };
}

export function AuthorizedImage({ reference, src, file, ...props }: ImgHTMLAttributes<HTMLImageElement> & { reference?: MediaReadReference; file?: File }) {
  const local = useMemo(() => file && typeof URL.createObjectURL === 'function' ? URL.createObjectURL(file) : undefined, [file]);
  useEffect(() => () => { if (local) URL.revokeObjectURL(local); }, [local]);
  const media = useAuthorizedMedia(local ? undefined : reference, local ?? src);
  const restoring = useRef(false);
  useEffect(() => { restoring.current = false; }, [JSON.stringify(reference)]);
  return <span className="relative block size-full">
    {media.url && <img {...props} src={media.url} onLoad={event => {
      media.report(restoring.current ? 'recovery' : 'load', 'success'); restoring.current = false; props.onLoad?.(event);
    }} onError={() => { media.report('load', 'failed'); restoring.current = true; void media.recover(); }} />}
    <MediaReadStatus state={media.state} compact onRetry={() => void media.retry()} />
  </span>;
}

export function AuthorizedVideo({ reference, src, ...props }: VideoHTMLAttributes<HTMLVideoElement> & { reference?: MediaReadReference }) {
  const media = useAuthorizedMedia(reference, src);
  const player = useRef<HTMLVideoElement>(null);
  const saved = useRef<{ time: number; paused: boolean } | null>(null);
  const recovering = useRef(false);
  useEffect(() => { saved.current = null; recovering.current = false; }, [JSON.stringify(reference)]);
  useEffect(() => {
    const hidden = () => {
      if (document.hidden && player.current) {
        saved.current = { time: player.current.currentTime || 0, paused: true };
        player.current.pause();
      }
    };
    document.addEventListener('visibilitychange', hidden);
    return () => document.removeEventListener('visibilitychange', hidden);
  }, []);
  return <div className="relative size-full">
    <video {...props} ref={player} src={media.url} onError={event => {
      const element = event.currentTarget;
      if (!media.url) return;
      media.report('load', 'failed');
      if (!recovering.current) saved.current = { time: element.currentTime || 0, paused: element.paused };
      recovering.current = true;
      void media.recover();
    }} onLoadedMetadata={event => {
      const element = event.currentTarget;
      if (saved.current) {
        element.currentTime = Math.min(saved.current.time, Number.isFinite(element.duration) ? Math.max(0, element.duration - 0.05) : saved.current.time);
        if (!saved.current.paused) void element.play().catch(() => { /* Browser gesture policy: keep native play control. */ });
      }
      props.onLoadedMetadata?.(event);
    }} onSeeked={event => {
      if (saved.current && Math.abs(event.currentTarget.currentTime - saved.current.time) <= 2) { media.report('recovery', 'success'); saved.current = null; recovering.current = false; }
      props.onSeeked?.(event);
    }} onLoadedData={event => { media.report('load', 'success'); props.onLoadedData?.(event); }} onPlay={event => {
      media.report('play', 'started'); props.onPlay?.(event);
    }} />
    <MediaReadStatus state={media.state} onRetry={() => void media.retry()} />
  </div>;
}

export function MediaPreviewButton({ reference, file }: { reference?: MediaReadReference; file?: File }) {
  const token = useAuthStore(state => state.token);
  // 新标签页会隐藏来源页；主动预览持续到身份变化、资源替换或取消。
  const controller = useMemo(() => createMediaReadController('admin'), [token]);
  const [failed, setFailed] = useState(false);
  const pending = useRef<{abort: AbortController; target: Window | null} | null>(null);
  useEffect(() => () => { pending.current?.abort.abort(); pending.current?.target?.close(); pending.current = null; }, [controller, JSON.stringify(reference), file]);
  useEffect(() => () => controller.dispose(), [controller]);
  return <><button type="button" className="btn" onClick={async () => {
    pending.current?.abort.abort(); pending.current?.target?.close();
    setFailed(false);
    const abort = new AbortController();
    const target = window.open('about:blank', '_blank');
    pending.current = {abort,target};
    if (target) target.opener = null;
    let local: string | undefined;
    try {
      const descriptor = !file && reference ? await controller.read(reference, {force:true,signal:abort.signal}) : undefined;
      let url = file ? (local = URL.createObjectURL(file)) : descriptor?.url;
      if (url && descriptor?.content_type?.split(';')[0].trim() === 'application/pdf') {
        // COS可能强制attachment；文件主体仍直读COS，用临时地址交给浏览器PDF阅读器。
        const download = new AbortController();
        const cancel = () => download.abort();
        abort.signal.addEventListener('abort', cancel, {once:true});
        if (abort.signal.aborted) cancel();
        const timeout = setTimeout(cancel, 10000);
        try {
          const response = await fetch(url, {signal:download.signal, referrerPolicy:'no-referrer', credentials:'omit'});
          if (!response.ok) throw new MediaReadFailure([401,403,404].includes(response.status));
          const blob = await response.blob();
          if (!abort.signal.aborted) url = local = URL.createObjectURL(blob);
        } finally {
          clearTimeout(timeout);
          abort.signal.removeEventListener('abort', cancel);
        }
      }
      if (abort.signal.aborted) { if (local) URL.revokeObjectURL(local); return; }
      if (!url || !target) throw new MediaReadFailure(true);
      target.location.replace(url);
      if (reference) controller.report(reference, 'preview', 'started');
      // Delay revocation until the new document has consumed its local file.
      if (local) setTimeout(() => URL.revokeObjectURL(local!), 60000);
    } catch { target?.close(); if (local) URL.revokeObjectURL(local); if (!abort.signal.aborted) setFailed(true); }
    finally { if (pending.current?.abort === abort) pending.current = null; }
  }}>预览</button>{failed && <span role="status">文件暂不可预览，请重试</span>}</>;
}
