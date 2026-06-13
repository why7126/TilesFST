import { WeComLoginButton } from './WeComLoginButton';

interface ThirdPartyLoginSectionProps {
  onWeComClick?: () => void;
}

export function ThirdPartyLoginSection({ onWeComClick }: ThirdPartyLoginSectionProps) {
  return (
    <div className="third-party">
      <div className="divider">或使用企业身份登录</div>
      <WeComLoginButton onClick={onWeComClick ?? (() => undefined)} />
    </div>
  );
}
