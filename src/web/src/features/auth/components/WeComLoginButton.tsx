interface WeComLoginButtonProps {
  onClick: () => void;
}

export function WeComLoginButton({ onClick }: WeComLoginButtonProps) {
  return (
    <button type="button" onClick={onClick} className="wecom" aria-label="企业微信登录">
      <img src="/icons/wecom.svg" alt="" aria-hidden="true" />
      企业微信登录
    </button>
  );
}
