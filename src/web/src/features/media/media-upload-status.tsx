import './media-upload-status.css';
import { FileVideo2, FileImage, FileText, LoaderCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/shared/lib/cn';

export type UploadStage = 'idle' | 'authorizing' | 'transferring' | 'saving' | 'verifying' | 'processing' | 'uploaded' | 'failed' | 'cancelling' | 'cancelled';

const labels: Record<UploadStage, string> = {
  idle: '', authorizing: '正在准备上传', transferring: '正在上传', saving: '正在保存视频，请稍候',
  verifying: '已传输 100% · 正在校验', processing: '正在生成图片展示版本',
  uploaded: '视频已添加', failed: '上传未完成', cancelling: '正在取消上传', cancelled: '本次上传已取消',
};

export function MediaUploadStatus({ stage, progress, fileName, error, onCancel, onRetry, mediaKind = 'video' }: {
  mediaKind?: 'video' | 'image' | 'document'; stage: UploadStage; progress: number; fileName?: string; error?: string | null;
  onCancel?: () => void; onRetry?: () => void;
}) {
  if (stage === 'idle') return null;
  const busy = ['authorizing', 'transferring', 'saving', 'verifying', 'processing', 'cancelling'].includes(stage);
  const transferred = ['verifying', 'processing', 'uploaded'].includes(stage) ? 100 : Math.min(100, Math.max(0, progress));
  return (
    <section data-testid="media-upload-status" data-upload-state={stage}
      className="media-upload-status bg-surface text-primary">
      <div className="media-upload-status__icon bg-deep text-brand-gold" aria-hidden="true">
        {busy ? <LoaderCircle className="h-6 w-6 animate-spin" /> : mediaKind === 'image' ? <FileImage className="h-6 w-6" /> : mediaKind === 'document' ? <FileText className="h-6 w-6" /> : <FileVideo2 className="h-6 w-6" />}
      </div>
      <div className="media-upload-status__body">
        {fileName ? <p className="media-upload-status__name text-primary" title={fileName}>{fileName}</p> : null}
        <p role="status" aria-live="polite" className={cn('media-upload-status__label', stage === 'failed' && 'media-upload-status__error')}>
          {stage === 'transferring' ? `上传中 ${Math.round(transferred)}%` : labels[stage].replace('视频', mediaKind === 'image' ? '图片' : mediaKind === 'document' ? '文件' : '视频')}
        </p>
        {busy && stage !== 'cancelling' ? (
          <div className="media-upload-status__progress bg-deep" role="progressbar"
            aria-label="文件传输进度" aria-valuemin={0} aria-valuemax={100} aria-valuenow={transferred}>
            <div className="media-upload-status__bar bg-brand-gold" style={{ width: `${transferred}%` }} />
          </div>
        ) : null}
        {stage === 'failed' && error ? <p role="alert" className="media-upload-status__error text-error">{error}</p> : null}
      </div>
      <div className="media-upload-status__actions">
        {stage === 'failed' && onRetry ? <Button className="media-upload-status__action" type="button" size="sm" variant="outline" onClick={onRetry}>重试上传</Button> : null}
        {onCancel && !['cancelled', 'uploaded'].includes(stage) ? (
          <Button className="media-upload-status__action" type="button" size="sm" variant="outline" disabled={stage === 'cancelling'} onClick={onCancel}>取消上传</Button>
        ) : null}
      </div>
    </section>
  );
}
