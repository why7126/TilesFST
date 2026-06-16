interface ResetPasswordDialogProps {
  open: boolean;
  password: string | null;
  onClose: () => void;
}

export function ResetPasswordDialog({ open, password, onClose }: ResetPasswordDialogProps) {
  if (!open || !password) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(password);
    } catch {
      // clipboard may be unavailable
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
          <input className="input" readOnly value={password} aria-label="随机密码" />
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
