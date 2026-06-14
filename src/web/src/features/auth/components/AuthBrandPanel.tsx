const stats = [
  { value: '12,860', label: '瓷砖 SKU' },
  { value: '38,420', label: '高清纹理图' },
  { value: '126', label: '门店同步' },
] as const;

const materialTiles = [
  { key: 'calacatta', label: 'CALACATTA / 900×1800', className: 'tile large' },
  { key: 'basalt', label: 'BASALT / 600×1200', className: 'tile dark' },
  { key: 'travertine', label: 'TRAVERTINE / 750×1500', className: 'tile gold' },
] as const;

export function AuthBrandPanel() {
  return (
    <section className="brand-panel" aria-label="品牌视觉区">
      <div className="brand-top">
        <p className="logo">TilesFST</p>
      </div>

      <div className="brand-content">
        <p className="brand-kicker">TILE DATA OPERATING SYSTEM</p>
        <h2 className="brand-title">瓷砖信息管理后台</h2>
        <p className="brand-desc">
          面向企业内部员工的瓷砖数据维护后台，集中管理产品图册、规格参数、价格体系、上下架状态与门店展示信息。
        </p>
        <div className="stats-card">
          {stats.map((item) => (
            <div key={item.label} className="stat">
              <strong>{item.value}</strong>
              <span>{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="brand-bottom">
        <p className="brand-kicker">PRECISION · MATERIAL · INVENTORY</p>
      </div>

      <div className="material-board" aria-hidden="true">
        {materialTiles.map((tile) => (
          <div key={tile.key} className={tile.className}>
            <label>{tile.label}</label>
          </div>
        ))}
      </div>
    </section>
  );
}
