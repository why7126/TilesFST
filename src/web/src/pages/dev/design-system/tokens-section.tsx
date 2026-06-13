import { colorCssVariables, getColorTokens } from '@shared/design-system/tokens/colors';
import { layoutSpacing, spacingScale } from '@shared/design-system/tokens/spacing';
import { radius } from '@shared/design-system/tokens/radius';
import {
  fontSize,
  letterSpacing,
  lineHeight,
  typographyPresets,
} from '@shared/design-system/tokens/typography';
import { shadows } from '@shared/design-system/tokens/shadows';

import { DesignSection, DesignSubSection, SwatchGrid, TokenTable } from './components';

const requiredSemanticClasses = [
  'bg-page',
  'bg-surface',
  'text-primary',
  'text-secondary',
  'text-brand-gold',
] as const;

const colors = getColorTokens('dark');

export function TokensSection() {
  const backgroundSwatches = [
    { name: 'bg-page', className: 'bg-page', value: colors.background.page },
    { name: 'bg-surface', className: 'bg-surface', value: colors.background.surface },
    { name: 'bg-secondary', className: 'bg-secondary', value: colors.background.secondary },
    { name: 'bg-deep', className: 'bg-deep', value: colors.background.deep },
    { name: 'bg-brand-gold', className: 'bg-brand-gold', value: colors.brand.gold },
    { name: 'bg-brand-gold-muted', className: 'bg-brand-gold-muted', value: colors.brand.goldMuted },
    { name: 'bg-bg-overlay', className: 'bg-bg-overlay', value: colors.background.overlay },
  ];

  const textSwatches = [
    { name: 'text-primary', className: 'text-primary', value: colors.text.primary },
    { name: 'text-secondary', className: 'text-secondary', value: colors.text.secondary },
    { name: 'text-muted', className: 'text-muted', value: colors.text.muted },
    { name: 'text-subtle', className: 'text-subtle', value: colors.text.subtle },
    { name: 'text-brand-gold', className: 'text-brand-gold', value: colors.brand.gold },
    { name: 'text-hot-sale', className: 'text-hot-sale', value: colors.semantic.hotSale },
  ];

  const borderSwatches = [
    { name: 'border-default', className: 'border-default', value: colors.border.default },
    { name: 'border-emphasis', className: 'border-emphasis', value: colors.border.emphasis },
    { name: 'border-strong', className: 'border-strong', value: colors.border.strong },
    { name: 'border-hover', className: 'border-hover', value: colors.border.hover },
    { name: 'border-focus', className: 'border-focus', value: colors.border.focus },
    { name: 'border-brand', className: 'border-brand', value: colors.border.brand },
  ];

  const spacingRows = Object.entries(spacingScale).map(([key, value]) => ({
    token: `--spacing-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    cssVar: `--spacing-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    value,
  }));

  const layoutRows = Object.entries(layoutSpacing).map(([key, value]) => ({
    token: `--layout-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    cssVar: `--layout-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    value,
  }));

  const radiusRows = Object.entries(radius)
    .filter(([key]) => !['sm', 'md', 'lg', 'xl', 'full'].includes(key))
    .map(([key, value]) => ({
      token: key,
      cssVar: key === 'industrial' ? '--radius-industrial' : key === 'card' ? '--radius-card' : `--radius-${key}`,
      value,
      className: key === 'card' ? 'rounded-card bg-page' : 'rounded-industrial bg-page',
    }));

  const typographyRows = Object.entries(fontSize).map(([key, value]) => ({
    token: `--font-size-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    cssVar: `--font-size-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    value,
  }));

  const shadowRows = Object.entries(shadows).map(([key, value]) => ({
    token: `--shadow-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    cssVar: `--shadow-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`,
    value,
  }));

  return (
    <>
      <DesignSection
        id="tokens-colors"
        title="Design Tokens · 色彩"
        description="来源 globals.css + @shared/design-system/tokens/colors.ts"
      >
        <div className="space-y-6">
          <DesignSubSection title="必选 Semantic Class">
            <div className="flex flex-wrap gap-2">
              {requiredSemanticClasses.map((className) => (
                <code
                  key={className}
                  className="rounded-industrial border border-border-chip bg-page px-2 py-1 text-[11px] text-brand-gold"
                >
                  {className}
                </code>
              ))}
            </div>
          </DesignSubSection>
          <DesignSubSection title="背景色">
            <SwatchGrid items={backgroundSwatches} type="bg" />
          </DesignSubSection>
          <DesignSubSection title="文字色">
            <SwatchGrid items={textSwatches} type="text" />
          </DesignSubSection>
          <DesignSubSection title="边框色">
            <SwatchGrid items={borderSwatches} type="border" />
          </DesignSubSection>
          <DesignSubSection title="品牌 / 语义色">
            <TokenTable
              rows={[
                {
                  token: 'brand-gold-badge',
                  cssVar: colorCssVariables.brand.goldBadge,
                  value: colors.brand.goldBadge,
                  className: 'bg-brand-gold-badge',
                },
                {
                  token: 'hot-sale-muted',
                  cssVar: colorCssVariables.semantic.hotSaleMuted,
                  value: colors.semantic.hotSaleMuted,
                  className: 'bg-hot-sale-muted',
                },
                {
                  token: 'error',
                  cssVar: colorCssVariables.semantic.error,
                  value: colors.semantic.error,
                  className: 'text-hot-sale',
                },
              ]}
            />
          </DesignSubSection>
        </div>
      </DesignSection>

      <DesignSection id="tokens-typography" title="Design Tokens · 字体" description="rules/ui-design.md §3">
        <div className="space-y-6">
          <DesignSubSection title="字号 Scale">
            <TokenTable rows={typographyRows} />
          </DesignSubSection>
          <DesignSubSection title="字距 / 行高">
            <TokenTable
              rows={[
                { token: 'tracking-brand', cssVar: '--tracking-brand', value: letterSpacing.brand },
                { token: 'tracking-section', cssVar: '--tracking-section', value: letterSpacing.section },
                { token: 'tracking-eyebrow', cssVar: '--tracking-eyebrow', value: letterSpacing.eyebrow },
                { token: 'tracking-badge', cssVar: '--tracking-badge', value: letterSpacing.badge },
                { token: 'leading-body', cssVar: '--line-height-body', value: lineHeight.body },
                { token: 'leading-caption', cssVar: '--line-height-caption', value: lineHeight.caption },
              ]}
            />
          </DesignSubSection>
          <DesignSubSection title="Typography Presets">
            <div className="space-y-3">
              {Object.entries(typographyPresets).map(([name, preset]) => (
                <div key={name} className="rounded-industrial border border-border-default bg-page px-4 py-3">
                  <p className="mb-2 font-mono text-[10px] text-muted">{name}</p>
                  <p style={preset}>STONEX 石材样本 Sample</p>
                </div>
              ))}
            </div>
          </DesignSubSection>
        </div>
      </DesignSection>

      <DesignSection id="tokens-spacing" title="Design Tokens · 间距" description="rules/ui-design.md §4">
        <div className="space-y-6">
          <DesignSubSection title="Spacing Scale">
            <TokenTable rows={spacingRows} />
          </DesignSubSection>
          <DesignSubSection title="Layout Dimensions">
            <TokenTable rows={layoutRows} />
          </DesignSubSection>
        </div>
      </DesignSection>

      <DesignSection id="tokens-radius" title="Design Tokens · 圆角" description="工业切割感 1–3px">
        <TokenTable rows={radiusRows} />
      </DesignSection>

      <DesignSection id="tokens-shadows" title="Design Tokens · 阴影" description="默认无 glow，工业风克制">
        <TokenTable rows={shadowRows} />
      </DesignSection>
    </>
  );
}
