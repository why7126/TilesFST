import { useEffect, useRef, useState } from 'react';
import type { UploadResult } from '@/shared/api/generated';
import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { MediaUploadTask, UploadSnapshot } from './media-upload-controller';

export type ImageTaskOptions = {
  task?: MediaUploadTask;
  onTask?: (task: MediaUploadTask) => void;
  onUpdate?: (value: UploadSnapshot) => void;
};
type Uploader = (file: File, progress?: (value: number) => void, options?: ImageTaskOptions) => Promise<UploadResult>;

/** Own a single unsaved image session; business save explicitly relinquishes ownership. */
export function useImageUpload(uploader: Uploader) {
  const task = useRef<MediaUploadTask | null>(null);
  const selected = useRef<File | undefined>(undefined);
  const completed = useRef<UploadResult | undefined>(undefined);
  const epoch = useRef(0);
  const running = useRef(false);
  const [snapshot, setSnapshot] = useState<UploadSnapshot>({ stage: 'idle', progress: 0 });
  useEffect(() => () => { epoch.current++; void task.current?.cancel().catch(() => undefined); }, []);
  useEffect(() => {
    const leave = (event: BeforeUnloadEvent) => {
      if (task.current) { event.preventDefault(); event.returnValue = ''; }
    };
    window.addEventListener('beforeunload', leave);
    return () => window.removeEventListener('beforeunload', leave);
  }, []);
  const cancel = async () => {
    epoch.current++; running.current = true; setSnapshot({stage:'cancelling', progress:0});
    try {
      await task.current?.cancel(); task.current = null; selected.current = undefined; completed.current = undefined;
      setSnapshot({stage:'cancelled', progress:0}); return true;
    } catch {
      setSnapshot({stage:'failed', progress:0, retryable:false, error:'取消未成功，请重试取消'}); return false;
    } finally { running.current = false; }
  };
  const start = async (file: File | undefined, retry = false) => {
    if (!file || running.current) return;
    if (retry && file === selected.current && completed.current) return completed.current;
    if (!retry && task.current && !await cancel()) return;
    const token = ++epoch.current; selected.current = file; running.current = true;
    setSnapshot({stage:'authorizing', progress:0});
    try {
      const result = await uploader(file, progress => {
        if (token === epoch.current) setSnapshot(value => ({...value, progress,
          stage: value.stage === 'authorizing' && progress > 0 ? 'transferring' : value.stage}));
      }, {task:retry ? task.current ?? undefined : undefined,
        onTask:value => {if(token===epoch.current) task.current=value; else void value.cancel().catch(() => undefined);},
        onUpdate:value => {if(token===epoch.current) setSnapshot(value);}});
      if(token!==epoch.current) return;
      completed.current=result;
      setSnapshot(value=>({...value,stage:'uploaded',progress:100})); return result;
    } catch(error) {
      if(token===epoch.current) setSnapshot(value=>({...value,stage:'failed',
        retryable:value.retryable ?? true,error:getErrorMessage(error,'头像上传失败')}));
    } finally { if(token===epoch.current) running.current=false; }
  };
  const saved = () => { task.current?.markSaved?.(); task.current=null; selected.current=undefined; completed.current=undefined; };
  const reset = () => { void task.current?.cancel().catch(() => undefined); task.current=null; selected.current=undefined; completed.current=undefined; epoch.current++; running.current=false; setSnapshot({stage:'idle',progress:0}); };
  return {snapshot, start, cancel, saved, reset, file:selected.current, sessionId: task.current?.sessionId,
    pending:!!task.current, busy:['authorizing','transferring','verifying','processing','saving','cancelling'].includes(snapshot.stage)};
}
