# add-brand-management — Trace

## 变更摘要

- **REQ**: `REQ-0005-brand-management`
- **Iteration**: `sprint-002`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `brand-management.html` + `brand-management-modal.html`）
- **Depends**: `add-admin-home`（AdminLayout）；参考 `add-user-management` 列表/弹窗模式
- **Status**: proposed

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0005-brand-management/requirement.md` |
| 验收 | `issues/requirements/REQ-0005-brand-management/acceptance.md` |
| 列表 HTML | `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html` |
| 列表 PNG | `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.png`（待补齐） |
| 弹窗 HTML | `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management-modal.html` |
| 弹窗 PNG | `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management-modal.png`（待补齐） |
| Design | `openspec/changes/add-brand-management/design.md` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 无导出/批量/标题行 | HTML 与 PRD 一致 |
| 弹窗无状态 | 创建默认 ENABLED，UI 不展示 |
| PNG 缺失 | 先 HTML 并排；PNG 后补 golden gate |
| sku_count | 本期默认 0 |
| 删除 | 物理删除 + 前后端双重校验 |

## 视觉 Diff Checklist（1280×1024）

### 列表页（brand-management.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Shell 264px + 1fr | | |
| 2 | Sidebar「瓷砖品牌」active | | |
| 3 | eyebrow MASTER DATA + 标题「瓷砖品牌」 | | |
| 4 | 主按钮「＋ 新增品牌」品牌金 | | |
| 5 | 无导出、无批量、无多余标题行 | | |
| 6 | 4 指标卡（总数/启用/停用/未关联SKU） | | |
| 7 | 筛选一行：关键词+状态+查询+重置 | | |
| 8 | 表格列：品牌/简称/英文/排序/SKU/状态/时间/操作 | | |
| 9 | Logo 占位首字母 | | |
| 10 | 删除可点/置灰四态矩阵 | | |
| 11 | 删除置灰 hover tooltip 文案 | | |
| 12 | 分页左侧共 N 条 + 页码 | | |
| 13 | 分页右侧跳页 + 每页 20/50/100 | | |
| 14 | 主内容 max-width 1080px | | |
| 15 | metric-card / table 与 admin-home 一致 | | |

### 弹窗（brand-management-modal.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 16 | 遮罩暗色半透明 | | |
| 17 | 弹窗宽 720px | | |
| 18 | 字段行：名称+排序 / 简称+英文 | | |
| 19 | Logo 与介绍 form-full 通栏同宽 | | |
| 20 | 无状态、无国家/地区、无规则说明 | | |
| 21 | 头尾固定、body 可滚动 | | |
| 22 | 主按钮「保存品牌」品牌金 | | |

## 验证命令

```bash
cd src/backend && uv run pytest tests/ -k brand
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/generate-openapi-client.sh
./scripts/docker-up.sh
```

## 错误码（实现参考）

| 码 | 场景 |
|---|---|
| `BRAND_NAME_DUPLICATED` | 名称重复 |
| `BRAND_DELETE_FORBIDDEN` | 非法删除 |
| `BRAND_INVALID_SORT_ORDER` | 排序非正整数 |
