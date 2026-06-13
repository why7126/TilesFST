/**
 * STONEX Design System — Spacing Tokens
 * Source: rules/ui-design.md §4 间距与圆角 + component specs
 *
 * Values use px for Tailwind/CSS parity. Numeric keys map to Tailwind spacing scale
 * where applicable (e.g. spacing[7] → 28px → space-y-7).
 */

/** Base spacing scale — 4px grid with design-specific overrides */
export const spacingScale = {
  /** 材质拼贴缝隙 — Hero material mosaic gap */
  mosaic: '3px',
  /** 徽章行间距 — product card badge row */
  badge: '5px',
  /** 筛选标签内边距 Y — filter chip vertical */
  chipY: '5px',
  /** 筛选标签内边距 X — filter chip horizontal */
  chipX: '14px',
  /** 产品卡格间距 — product grid gap */
  grid: '12px',
  /** 产品卡信息区内边距 — compact card padding */
  cardSm: '14px',
  /** 产品卡信息区内边距 — featured card padding */
  cardMd: '20px',
  /** 区块间距 — section vertical rhythm (min) */
  sectionSm: '24px',
  /** 区块间距 — section vertical rhythm (max) */
  sectionLg: '32px',
  /** 页面内边距 — global horizontal padding */
  page: '28px',
  /** 表单项间距 — login form field gap */
  formField: '28px',
  /** 标题到表单 — login title margin */
  titleToForm: '48px',
  /** Hero 上内边距 */
  heroTop: '60px',
  /** Hero 下内边距 */
  heroBottom: '48px',
  /** 数据条内边距 Y — data strip vertical */
  dataStripY: '18px',
  /** 侧边栏内边距 Y */
  sidebarY: '24px',
  /** 侧边栏内边距 X */
  sidebarX: '20px',
  /** 纹理速览条内边距 Y */
  textureRowY: '24px',
  /** 页脚下内边距 */
  footerBottom: '20px',
  /** 主按钮到第三方登录 — login section gap */
  primaryToSocial: '56px',
  /** 主按钮内边距 Y — primary CTA vertical */
  buttonY: '11px',
  /** 主按钮内边距 X — primary CTA horizontal */
  buttonX: '24px',
  /** 产品卡信息区上内边距 */
  productInfoTop: '12px',
  /** 产品卡信息区下内边距 */
  productInfoBottom: '14px',
} as const;

/** Layout dimensions — fixed component sizes */
export const layoutSpacing = {
  /** 导航栏高度 */
  navHeight: '52px',
  /** 侧边栏宽度 */
  sidebarWidth: '200px',
  /** 搜索栏高度 */
  searchBarHeight: '44px',
  /** 输入框高度 — desktop / login */
  inputHeightLg: '64px',
  /** 输入框高度 — mobile / compact */
  inputHeightMd: '52px',
  /** 分页按钮尺寸 */
  paginationSize: '32px',
  /** 操作图标按钮 — product card actions */
  iconButtonSize: '28px',
  /** 复选框 — sidebar filter */
  checkboxSize: '13px',
  /** 复选框 — login page */
  checkboxSizeLg: '18px',
  /** 纹理色块高度 — texture row swatch */
  textureSwatchHeight: '48px',
  /** 产品卡图片区高度 */
  productImageHeight: '130px',
  /** 精选卡图片最小高度 */
  featuredImageMinHeight: '180px',
  /** 登录表单最大宽度 — mobile */
  loginFormMaxWidth: '520px',
} as const;

/** Semantic spacing aliases for common layout patterns */
export const spacing = {
  /** 4px base unit multiples for Tailwind alignment */
  px: '1px',
  0: '0px',
  0.5: '2px',
  1: '4px',
  1.5: '6px',
  2: '8px',
  2.5: '10px',
  3: '12px',
  3.5: '14px',
  4: '16px',
  5: '20px',
  6: '24px',
  7: '28px',
  8: '32px',
  9: '36px',
  10: '40px',
  11: '44px',
  12: '48px',
  14: '56px',
  15: '60px',
  /** Design-specific tokens */
  mosaic: spacingScale.mosaic,
  badge: spacingScale.badge,
  grid: spacingScale.grid,
  page: spacingScale.page,
  section: spacingScale.sectionSm,
  sectionLg: spacingScale.sectionLg,
} as const;

/** Tailwind utility class mappings for frequently used spacing */
export const spacingTailwindClasses = {
  pagePaddingX: 'px-7',
  pagePadding: 'px-7',
  sectionGap: 'gap-6',
  sectionGapLg: 'gap-8',
  gridGap: 'gap-3',
  formFieldGap: 'space-y-7',
  titleToForm: 'mb-12',
  primaryToSocial: 'pt-14',
  cardPaddingSm: 'p-3.5',
  cardPaddingMd: 'p-5',
  heroPadding: 'pt-15 px-7 pb-12',
  navHeight: 'h-[52px]',
  inputHeightLg: 'h-16',
  inputHeightMd: 'h-[52px]',
  searchBarHeight: 'h-11',
} as const;

export type SpacingKey = keyof typeof spacing;
export type SpacingScaleKey = keyof typeof spacingScale;
export type LayoutSpacingKey = keyof typeof layoutSpacing;
