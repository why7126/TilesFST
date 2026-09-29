import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { AuthorizedImage, AuthorizedVideo, MediaReadProvider, MediaPreviewButton } from './authorized-media';
const { transport } = vi.hoisted(() => ({ transport: vi.fn() }));
vi.mock('./media-read-api', async () => {
  const { MediaReadController } = await import('./read-controller');
  return { createMediaReadController: () => new MediaReadController(transport) };
});
const ref = { resource_type: 'sku_image' as const, resource_id: '7', media_id: 1, variant: 'display' as const };
const answer = (items: typeof ref[], url = 'https://storage.example.test/authorized') => ({ server_time: new Date().toISOString(), items: items.map(reference => ({ reference, status: 'ready', descriptor: { url, read_mode: 'direct', variant: reference.variant, media_ref: 'sku_image:7:1', expires_at: new Date(Date.now()+300000).toISOString() } })) });
afterEach(() => { vi.useRealTimers(); transport.mockReset(); });
it('batches visible images and does not display the supplied legacy URL before authorization', async () => {
  let done!: (value: unknown) => void;
  transport.mockImplementation(() => new Promise(resolve => { done = resolve; }));
  const view = render(<MediaReadProvider><AuthorizedImage reference={ref} src="/media/private-key" alt="first" /><AuthorizedImage reference={ref} alt="second" /></MediaReadProvider>);
  expect(view.container.querySelector('img')).toBeNull();
  await waitFor(() => expect(transport).toHaveBeenCalledTimes(1));
  await act(async () => done(answer([ref])));
  expect(screen.getByAltText('first')).toHaveAttribute('src', 'https://storage.example.test/authorized');
  expect(screen.getByAltText('second')).toHaveAttribute('src', 'https://storage.example.test/authorized');
});
it('refreshes on image failure without mutating form values and stops on denied media', async () => {
  transport.mockImplementation(async items => answer(items));
  const view = render(<MediaReadProvider><input aria-label="name" defaultValue="unsaved" /><AuthorizedImage reference={ref} alt="media" /></MediaReadProvider>);
  await screen.findByAltText('media');
  transport.mockImplementation(async items => ({server_time: new Date().toISOString(),items: items.map((reference: typeof ref) => ({reference,status:'unavailable'}))}));
  fireEvent.error(screen.getByAltText('media'));
  await waitFor(() => expect(view.container.querySelector('[data-media-state="unavailable"]')).not.toBeNull(), { timeout: 2000 });
  expect(screen.getByLabelText('name')).toHaveValue('unsaved');
  expect(view.container.querySelector('img')).toBeNull();
  expect(screen.queryByRole('button')).toBeNull();
});
it('does not apply a late URL after reference replacement', async () => {
  const completions: (() => void)[] = [];
  transport.mockImplementation(items => new Promise(resolve => completions.push(() => resolve(answer(items, `https://storage.example.test/${items[0].media_id}`)))));
  const view = render(<MediaReadProvider><AuthorizedImage reference={ref} alt="media" /></MediaReadProvider>);
  await waitFor(() => expect(completions).toHaveLength(1));
  view.rerender(<MediaReadProvider><AuthorizedImage reference={{...ref,media_id:2}} alt="media" /></MediaReadProvider>);
  await waitFor(() => expect(completions).toHaveLength(2));
  await act(async () => { completions[1](); });
  await act(async () => { completions[0](); });
  expect(screen.getByAltText('media')).toHaveAttribute('src','https://storage.example.test/2');
});
it('restores paused video position after a refreshed source loads metadata', async () => {
  transport.mockImplementation(async items => answer(items));
  const view = render(<MediaReadProvider><AuthorizedVideo reference={{...ref,resource_type:'sku_video',variant:'original'}} controls /></MediaReadProvider>);
  const video = view.container.querySelector('video')!;
  await waitFor(() => expect(video.src).toContain('authorized'));
  Object.defineProperty(video,'currentTime',{value:19,writable:true});
  Object.defineProperty(video,'duration',{value:100});
  Object.defineProperty(video,'paused',{value:true});
  transport.mockImplementation(async items => answer(items,'https://storage.example.test/refreshed'));
  fireEvent.error(video);
  await waitFor(() => expect(video.src).toContain('refreshed'),{timeout:2000});
  video.currentTime=0; fireEvent.loadedMetadata(video);
  expect(video.currentTime).toBe(19);
});

it('keeps selected files local and revokes their preview when removed', async () => {
  const create = vi.spyOn(URL,'createObjectURL').mockReturnValue('blob:synthetic-preview');
  const revoke = vi.spyOn(URL,'revokeObjectURL').mockImplementation(() => {});
  const view = render(<MediaReadProvider><AuthorizedImage reference={ref} file={new File(['test'],'local.png')} alt="local" /></MediaReadProvider>);
  expect(await screen.findByAltText('local')).toHaveAttribute('src','blob:synthetic-preview');
  expect(transport).not.toHaveBeenCalled();
  view.unmount(); expect(revoke).toHaveBeenCalledWith('blob:synthetic-preview');
  create.mockRestore(); revoke.mockRestore();
});
it('discards visible private URLs on identity change before the next authorization resolves', async () => {
  const {useAuthStore} = await import('@/features/auth/store/auth-store');
  transport.mockImplementation(async items => answer(items));
  const view = render(<MediaReadProvider><AuthorizedImage reference={ref} alt="private" /></MediaReadProvider>);
  await screen.findByAltText('private');
  transport.mockImplementation(() => new Promise(() => {}));
  act(() => useAuthStore.setState({token:'synthetic-new-identity'}));
  expect(view.container.querySelector('img')).toBeNull();
  view.unmount(); act(() => useAuthStore.setState({token:null}));
});

it('keeps an explicit preview alive when its new tab hides the source page', async () => {
  const replace = vi.fn(); const close = vi.fn();
  const hidden = vi.spyOn(document, 'hidden', 'get').mockReturnValue(false);
  const open = vi.spyOn(window, 'open').mockImplementation(() => {
    hidden.mockReturnValue(true);
    document.dispatchEvent(new Event('visibilitychange'));
    return {opener: null, location: {replace}, close} as unknown as Window;
  });
  transport.mockImplementation(async items => answer(items));
  const view = render(<MediaReadProvider><MediaPreviewButton reference={ref} /></MediaReadProvider>);
  try {
    fireEvent.click(screen.getByRole('button', {name: '预览'}));
    await waitFor(() => expect(replace).toHaveBeenCalledWith('https://storage.example.test/authorized'));
    expect(close).not.toHaveBeenCalled();
  } finally { view.unmount(); open.mockRestore(); hidden.mockRestore(); }
});

it('cancels a pending preview on identity change and ignores the late URL', async () => {
  const {useAuthStore} = await import('@/features/auth/store/auth-store');
  const replace = vi.fn(); const close = vi.fn();
  const open = vi.spyOn(window, 'open').mockReturnValue({opener: null, location: {replace}, close} as unknown as Window);
  let done!: () => void;
  transport.mockImplementation(items => new Promise(resolve => { done = () => resolve(answer(items)); }));
  const view = render(<MediaReadProvider><MediaPreviewButton reference={ref} /></MediaReadProvider>);
  try {
    fireEvent.click(screen.getByRole('button', {name: '预览'}));
    await waitFor(() => expect(transport).toHaveBeenCalledTimes(1));
    act(() => useAuthStore.setState({token: 'synthetic-preview-new-identity'}));
    await act(async () => done());
    expect(close).toHaveBeenCalled();
    expect(replace).not.toHaveBeenCalled();
  } finally { view.unmount(); open.mockRestore(); act(() => useAuthStore.setState({token:null})); }
});

it('opens attachment PDFs through a local blob while omitting credentials from COS reads', async () => {
  const replace = vi.fn(); const close = vi.fn();
  const open = vi.spyOn(window,'open').mockReturnValue({opener:null,location:{replace},close} as unknown as Window);
  const create = vi.spyOn(URL,'createObjectURL').mockReturnValue('blob:pdf-preview');
  const revoke = vi.spyOn(URL,'revokeObjectURL').mockImplementation(() => {});
  const fetchFile = vi.spyOn(globalThis,'fetch').mockResolvedValue({ok:true,blob:async () => new Blob(['%PDF-test'],{type:'application/pdf'})} as Response);
  transport.mockImplementation(async items => { const response=answer(items); return {...response,items:response.items.map(item=>({...item,descriptor:{...item.descriptor,content_type:'application/pdf'}}))}; });
  const view=render(<MediaReadProvider><MediaPreviewButton reference={ref} /></MediaReadProvider>);
  try {
    fireEvent.click(screen.getByRole('button',{name:'预览'}));
    await waitFor(()=>expect(replace).toHaveBeenCalledWith('blob:pdf-preview'));
    expect(fetchFile).toHaveBeenCalledWith('https://storage.example.test/authorized',expect.objectContaining({credentials:'omit',referrerPolicy:'no-referrer',signal:expect.any(AbortSignal)}));
    expect(close).not.toHaveBeenCalled();
  } finally {view.unmount();open.mockRestore();create.mockRestore();revoke.mockRestore();fetchFile.mockRestore();}
});

it('aborts a PDF download when the signed-in identity changes', async () => {
  const {useAuthStore}=await import('@/features/auth/store/auth-store');
  const replace=vi.fn(); const close=vi.fn();
  const open=vi.spyOn(window,'open').mockReturnValue({opener:null,location:{replace},close} as unknown as Window);
  let signal: AbortSignal | undefined;
  const fetchFile=vi.spyOn(globalThis,'fetch').mockImplementation((_url,options)=>new Promise((_resolve,reject)=>{
    signal=options?.signal as AbortSignal;
    signal.addEventListener('abort',()=>reject(new DOMException('Cancelled','AbortError')),{once:true});
  }));
  transport.mockImplementation(async items=>{const response=answer(items);return {...response,items:response.items.map(item=>({...item,descriptor:{...item.descriptor,content_type:'application/pdf'}}))};});
  const view=render(<MediaReadProvider><MediaPreviewButton reference={ref} /></MediaReadProvider>);
  try {
    fireEvent.click(screen.getByRole('button',{name:'预览'}));
    await waitFor(()=>expect(fetchFile).toHaveBeenCalledTimes(1));
    await act(async()=>useAuthStore.setState({token:'synthetic-pdf-new-identity'}));
    expect(signal?.aborted).toBe(true);
    expect(close).toHaveBeenCalled();
    expect(replace).not.toHaveBeenCalled();
  } finally {view.unmount();open.mockRestore();fetchFile.mockRestore();act(()=>useAuthStore.setState({token:null}));}
});
