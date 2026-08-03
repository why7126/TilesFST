import { Palette } from 'lucide-react';

import { AdminFilterSelect } from '@/shared/ui';

import { THEME_MODE_LABELS, THEME_MODES, type ThemeMode } from './theme';
import { useTheme } from './ThemeContext';
import './theme-switcher.css';

interface ThemeSwitcherProps {
  compact?: boolean;
}

export function ThemeSwitcher({ compact = false }: ThemeSwitcherProps) {
  const { mode, setMode } = useTheme();
  const label = compact ? '主题' : '界面主题';
  const options = THEME_MODES.map((item) => ({
    value: item,
    label: THEME_MODE_LABELS[item],
  }));

  return (
    <div className={compact ? 'theme-switcher compact' : 'theme-switcher'}>
      <span className="theme-switcher-label">
        <Palette size={14} aria-hidden />
        {label}
      </span>
      <AdminFilterSelect
        value={mode}
        ariaLabel={label}
        listLabel="界面主题选项"
        options={options}
        onChange={(value) => void setMode(value as ThemeMode)}
        className="theme-switcher-select"
      />
    </div>
  );
}
