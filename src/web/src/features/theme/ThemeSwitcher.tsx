import { Palette } from 'lucide-react';

import { THEME_MODE_LABELS, THEME_MODES, type ThemeMode } from './theme';
import { useTheme } from './ThemeContext';
import './theme-switcher.css';

interface ThemeSwitcherProps {
  compact?: boolean;
}

export function ThemeSwitcher({ compact = false }: ThemeSwitcherProps) {
  const { mode, setMode } = useTheme();
  const label = compact ? '主题' : '界面主题';

  return (
    <label className={compact ? 'theme-switcher compact' : 'theme-switcher'}>
      <span className="theme-switcher-label">
        <Palette size={14} aria-hidden />
        {label}
      </span>
      <select
        className="theme-switcher-select"
        value={mode}
        aria-label={label}
        onChange={(event) => void setMode(event.target.value as ThemeMode)}
      >
        {THEME_MODES.map((item) => (
          <option key={item} value={item}>
            {THEME_MODE_LABELS[item]}
          </option>
        ))}
      </select>
    </label>
  );
}
