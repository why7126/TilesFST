import { dashboardRecentUpdates } from '../data/dashboard-mock';

export function DashboardRecentUpdates() {
  return (
    <section className="section" aria-labelledby="recent-title">
      <div className="section-head">
        <h2 className="section-title" id="recent-title">
          最近更新
        </h2>
        <span className="section-note">最近 7 天数据变更</span>
      </div>
      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th scope="col">更新时间</th>
              <th scope="col">类型</th>
              <th scope="col">名称</th>
              <th scope="col">操作人</th>
            </tr>
          </thead>
          <tbody>
            {dashboardRecentUpdates.map((row) => (
              <tr key={row.id}>
                <td>{row.updatedAt}</td>
                <td>
                  <span className="badge">{row.type}</span>
                </td>
                <td className="name-cell">{row.name}</td>
                <td>{row.operator}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
