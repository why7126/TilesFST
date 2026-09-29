import { Button } from './button';
import { cn } from '@/shared/lib/cn';

export type MediaReadState = 'loading' | 'refreshing' | 'ready' | 'failed' | 'unavailable' | 'offline' | 'degraded';
const messages: Record<MediaReadState, string> = {
  loading: '正在加载…', refreshing: '正在恢复…', ready: '',
  failed: '暂时无法加载，请重试', unavailable: '该内容暂不可访问',
  offline: '网络已断开，请连接后重试', degraded: '',
};

/** Fixed media container overlay; never changes the parent layout or form values. */
export function MediaReadStatus({ state, onRetry, compact = false, className }: {
  state: MediaReadState; onRetry?: () => void; compact?: boolean; className?: string;
}) {
  if (state === 'ready' || state === 'degraded') return null;
  return <div data-media-state={state} role="status" aria-live="polite"
    style={{ color: 'var(--color-text-secondary)' }}
    aria-busy={state === 'loading' || state === 'refreshing'}
    className={cn('absolute inset-0 flex flex-col items-center justify-center gap-2 overflow-hidden bg-surface p-2 text-center text-xs text-secondary', className)}>
    <span className={cn(compact && 'sr-only')}>{messages[state]}</span>
    {compact && <span aria-hidden="true">{state === 'loading' || state === 'refreshing' ? '…' : '—'}</span>}
    {onRetry && (state === 'failed' || state === 'offline') && <Button type="button" style={{ color: 'var(--color-text-secondary)' }} size="sm" variant="outline" onClick={onRetry} aria-label="重新加载媒体" className={cn(compact && 'h-6 px-1 text-xs')}>{compact ? '重试' : '重新加载'}</Button>}
  </div>;
}
