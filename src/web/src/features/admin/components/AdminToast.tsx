type AdminToastProps = {
  message: string | null;
};

export function AdminToast({ message }: AdminToastProps) {
  if (!message) {
    return null;
  }

  return (
    <div className="admin-toast-region" aria-live="polite" aria-atomic="true">
      <p className="admin-toast" role="status">
        {message}
      </p>
    </div>
  );
}
