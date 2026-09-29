import { MediaReadStatus, type MediaReadState } from '@/shared/ui/media-read-status';

/** Review-only composition; has no API data, navigation, real player or stored credentials. */
export function MediaSkeleton() {
  const states: MediaReadState[] = ['loading', 'refreshing', 'failed', 'unavailable', 'offline'];
  return <main className="min-h-screen bg-page p-7 text-primary" data-testid="media-skeleton" style={{ color: 'var(--color-text-primary)' }}>
    <h1 className="text-xl font-normal">媒体状态布局确认</h1>
    <p className="my-4 text-sm text-secondary" style={{ color: 'var(--color-text-secondary)' }}>局部组件 · 合成占位数据 · 未连接真实媒体</p>
    <section aria-label="管理端列表容器" className="mb-6 overflow-auto border border-border-default">
      <table className="w-full text-sm"><thead><tr><th className="p-3 text-left">媒体</th><th className="text-left">商品</th><th className="text-left">状态</th></tr></thead>
      <tbody>{states.map(state => <tr key={state} className="border-t border-border-default"><td className="p-3"><div className="relative size-16"><MediaReadStatus state={state} compact onRetry={() => {}} /></div></td><td>示例商品</td><td>{state}</td></tr>)}</tbody></table>
    </section>
    <section aria-label="预览与移动端容器" className="grid gap-6 md:grid-cols-2">
      {states.map(state => <div key={state}><p className="mb-2 text-sm">{state}</p><div className="relative aspect-video border border-border-default"><MediaReadStatus state={state} onRetry={() => {}} /></div></div>)}
    </section>
  </main>;
}
