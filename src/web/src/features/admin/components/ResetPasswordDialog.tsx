import { useEffect, useRef, useState } from 'react';

interface ResetPasswordDialogProps {
  open: boolean;
  password: string | null;
  onClose: () => void;
}

type CopyState = 'idle' | 'success' | 'fallback';

export function ResetPasswordDialog({ open, password, onClose }: ResetPasswordDialogProps) {
  const passwordInputRef = useRef<HTMLInputElement>(null);
  const [copyState, setCopyState] = useState<CopyState>('idle');

  useEffect(() => {
    setCopyState('idle');
  }, [open, password]);

  if (!open || !password) return null;

  const selectPasswordForManualCopy = () => {
    passwordInputRef.current?.focus();
    passwordInputRef.current?.select();
  };

  const handleCopy = async () => {
    const writeText = navigator.clipboard?.writeText;

    if (!writeText) {
      selectPasswordForManualCopy();
      setCopyState('fallback');
      return;
    }

    try {
      await writeText.call(navigator.clipboard, password);
      setCopyState('success');
    } catch {
      selectPasswordForManualCopy();
      setCopyState('fallback');
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="reset-pwd-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <span id="reset-pwd-title" className="modal-title">
            随机密码已生成
          </span>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <p className="form-help">请复制并安全交付给用户，关闭后不可再次查看。</p>
          <input
            ref={passwordInputRef}
            className="input"
            readOnly
            value={password}
            aria-label="随机密码"
          />
          <p className="form-help" role="status" aria-live="polite">
            {copyState === 'success'
              ? '密码已复制，请粘贴确认后再关闭弹窗。'
              : copyState === 'fallback'
                ? '自动复制失败，请使用 Command/Ctrl + C 手动复制已选中的密码。'
                : '若浏览器阻止自动复制，可手动选中密码后复制。'}
          </p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn" onClick={() => void handleCopy()}>
            复制密码
          </button>
          <button type="button" className="btn primary" onClick={onClose}>
            关闭
          </button>
        </div>
      </div>
    </div>
  );
}
