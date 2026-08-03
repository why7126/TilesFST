---
change_id: update-web-modal-disable-outside-close
type: update
status: archived
created_at: 2026-07-30 23:25:55
updated_at: 2026-07-31 00:07:41
source_requirement: REQ-0084-web-modal-disable-outside-close
iteration: sprint-014
---

# Change Trace

## 基本信息

```yaml
change_id: update-web-modal-disable-outside-close
type: update
status: archived
source_requirement: REQ-0084-web-modal-disable-outside-close
requirement_path: issues/requirements/archive/REQ-0084-web-modal-disable-outside-close
iteration: sprint-014
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - web-client
    - design-system
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
prototype:
  web:
    html: issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/prototype/web/modal-disable-outside-close.html
    context: issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/prototype/web/context.md
    png_checklist:
      - 待后续实现阶段按真实组件截图或 Playwright screenshot 补证据
```

## Requirement Readiness Report

| 项目 | 结果 |
|---|---|
| status gate | Pass：REQ trace status 为 `approved` |
| readiness | Ready |
| documents | requirement、user-stories、business-flow、acceptance、trace、review、prototype/web 已齐 |
| knowledge-base gate | Pass：admin-modal、media-upload 横切 AC 已写入 |

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
change_type: update
capabilities:
  new: []
  modified:
    - web-client
    - design-system
```

## Conflict Report

| 来源 | 冲突 / 结论 |
|---|---|
| prototype HTML | 点击遮罩或外部空白区域后弹窗保持打开，优先级最高。 |
| prototype context | 明确关闭入口关闭，上传中误点外部保持打开。 |
| acceptance.md | AC-001 至 AC-015 和 AC-XCUT-001 至 AC-XCUT-009 作为验收来源。 |
| openspec/specs/web-client | 旧规格中“遮罩关闭弹窗”与 REQ-0084 冲突，本 Change 用 MODIFIED requirements 消化。 |
| rules/ui-design.md | 视觉风格、semantic token 和弹窗 CSS 层叠约束继续有效。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-30 23:25:55 | `/req-opsx` | 从 REQ-0084 创建 OpenSpec Change，生成 proposal、design、delta specs、tasks 与 trace。 |
| 2026-07-30 23:33:30 | `/sprint-propose sprint-014` | 纳入 Sprint 014 正式范围，等待 `/opsx-apply`。 |
| 2026-07-30 23:49:26 | `/opsx-apply` | 实现 Web 标准 Modal 禁止遮罩/外部空白点击关闭，更新测试与验证证据。 |
| 2026-07-31 00:07:41 | `/opsx-archive` | Change 已归档至 `openspec/archive/2026-07-31-update-web-modal-disable-outside-close/`，delta spec 已合并。 |

## Apply Evidence

### Inventory Results

| 范围 | 结果 |
|---|---|
| SKU | `TileSkuFormModal`、SKU 上架/下架确认、删除确认均已移除 backdrop 关闭。 |
| Brand | `BrandFormModal`、品牌启用/停用确认、删除确认均已移除 backdrop 关闭。 |
| Category | `CategoryFormModal`、类目启用/停用确认、删除确认均已移除 backdrop 关闭。 |
| Certificate | 证书表单、显示/隐藏/删除确认均已移除 backdrop 关闭。 |
| Banner | `BannerFormModal`、上线/下线确认、删除确认均已移除 backdrop 关闭。 |
| User | `UserFormModal`、冻结/解冻确认、删除确认、重置密码确认、随机密码展示均已移除 backdrop 关闭。 |
| System settings | 重置/放弃修改确认、通知模板占位弹窗均已移除 backdrop 关闭。 |
| Password | `ChangePasswordModal` 已移除 backdrop 关闭，保留 Esc 与显式按钮关闭。 |
| Log-related | `LogAuditPage` 使用详情 drawer 的显式 backdrop button，不属于本 Change 的标准 Dialog / Modal 范围，保持现状。 |
| Catalog | 本次代码盘点未发现店主目录端标准 Dialog / Modal 实现；无可修改对象。 |

### Implementation Notes

- 共享标准 Modal 当前由 `modal-backdrop` / `modal-card` CSS 约定和多个 feature-local 组件共同承载；本次在各调用处移除外层 backdrop 的关闭回调，避免新增 API 或改变轻量浮层行为。
- 保留关闭图标、取消按钮、确认/保存后的业务完成关闭；密码修改弹窗保留 Esc 关闭。
- 触及上传表单：品牌 Logo、Banner 图片、证书文件/图片、用户头像、SKU 图片/视频弹窗仅改变 backdrop 行为，未修改上传 transport、Nginx、MinIO 或同会话预览逻辑。
- `TileSpecFormModal` 移除 `modal-card tile-spec-modal-card` 双类组合，并将必要卡片基础样式收敛到 `.tile-spec-modal-card`，遵循 `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`。

### Exceptions

- Popover、Dropdown、Tooltip、Select dropdown、日期选择器、SearchableSelect 等轻量浮层未修改。
- 日志详情 drawer 保持点击背景按钮关闭，原因是其语义为侧边详情抽屉，不属于 REQ-0084 标准 Dialog / Modal。

### Validation Results

| 项目 | 结果 |
|---|---|
| Functional AC | Pass：表单与确认弹窗点击 backdrop 保持打开；显式关闭/取消/确认路径保留。 |
| AC-XCUT：admin弹窗宽度级联 | Pass：`rg` 未发现触及范围存在 `modal-card` 与 feature-specific modal card 双类组合；规格弹窗专用样式补齐基础卡片规则。 |
| AC-XCUT：media-upload | Pass：未修改上传 transport、Nginx、MinIO；Docker `:3000` 上传边界验证 N/A，原因是本次仅修改 Modal 关闭交互。 |
| Tests | Pass：`pnpm --dir src/web test -- CategoryFormModal BrandManagementPage`，Vitest 57 files / 304 tests passed。 |
