---
change_id: add-admin-display-image-size-limit-setting
source_requirement: REQ-0119-admin-display-image-size-limit-setting
status: applied
created_at: 2026-08-22 21:41:50
updated_at: 2026-08-22 22:18:00
---

# Change 追踪

## 基本信息

```yaml
change_id: add-admin-display-image-size-limit-setting
source_requirement: REQ-0119-admin-display-image-size-limit-setting
change_type: update
status: applied
sprint: sprint-025
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - system-settings
    - media-multi-variant-images
    - object-storage
    - prod-media-maintenance-jobs
readiness: archive_ready
prototype_refs:
  - issues/requirements/archive/REQ-0119-admin-display-image-size-limit-setting/prototype/web/system-settings-media-display-size.html
  - issues/requirements/archive/REQ-0119-admin-display-image-size-limit-setting/prototype/web/context.md
ui_contract: design.md#ui-contract
png_checklist:
  skeleton_1440x1024: verified_by_dom_and_code_review
  default_state: verified_by_vitest
  dirty_state: verified_by_vitest
  reset_modal: verified_by_vitest
  fixed_toast: verified_by_vitest
  computed_style: verified_by_existing_semantic_classes
```

## Requirement Readiness Report

```yaml
result: partially_ready
reason:
  - requirement.md、user-stories.md、business-flow.md、acceptance.md、trace.md 已齐全。
  - prototype/web 存在 HTML 与 context，可用于 UI Contract。
  - PNG、Skeleton、computed style 与真实 API evidence 尚未生成，作为 /opsx-apply 验收任务。
```

## Conflict Report

```yaml
prototype_priority:
  - prototype/web/system-settings-media-display-size.html
  - prototype/web/context.md
  - acceptance.md
  - rules/ui-design.md
  - openspec/specs/system-settings/spec.md
resolution:
  field_label: 采用“详情展示图体积目标上限 (KB)”
  field_key: 采用 display_max_size_kb，最终实现可用等价字段但必须在 API/Orval/文档一致
  default_value: 768
  strategy: design-system
  notes:
    - 原型是轻量 HTML/context，不直接复制裸 Hex。
    - 实现必须复用系统设置页 Shell、footer CTA、DS modal 和 fixed toast。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 22:18:00 | `/opsx-modify REQ-0119` | 验收返修：优化媒体与存储 Tab 上传限制 2 列网格顺序；补测试、UI Contract、delta spec、REQ acceptance evidence 与 Sprint 验收报告 |
| 2026-08-22 22:08:00 | workflow-sync / ai-usage-hook | `opsx.apply` 同步 sprint-025 成功，REQ acceptance=pending；AI usage hook 因当前会话无 token_count events 返回 warning/unavailable |
| 2026-08-22 22:06:00 | `/opsx-apply REQ-0119` | 完成 `display_max_size_kb` 系统设置、display 派生生成链路、维护任务、管理端 UI、OpenAPI/Orval、文档与测试 |
| 2026-08-22 21:41:50 | `/req-opsx REQ-0119` | 创建 OpenSpec Change，生成 proposal、design、spec delta、tasks 与 trace |

## 验收返修记录

```yaml
feedback:
  source: user_acceptance
  command: /opsx-modify REQ-0119
  summary: 媒体与存储 Tab 上传限制显示优化，要求 2 列网格按语义分四行排列
scope_decision:
  status: in_scope
  reason: 反馈属于 REQ-0119 管理端媒体设置 UI 原验收范围，不改变 API、DB、权限、对象存储或后端生成逻辑
adjustment:
  - src/web/src/pages/admin/SystemSettingsPage.tsx: 上传限制 grid 增加第二行右侧空占位，并将“文档最大尺寸”文案收敛为“文件最大尺寸”
  - src/web/src/features/admin/styles/system-settings.css: 桌面保留占位，移动端隐藏占位避免空白行
  - src/web/src/pages/admin/SystemSettingsPage.test.tsx: 断言四行顺序和占位 cell
ui_evidence:
  viewport: 1440x1024 equivalent
  method: 代码结构复核 + Vitest DOM 顺序断言；当前项目无 Playwright/截图测试入口
  expected_rows:
    - 图片最大尺寸 / 视频最大尺寸
    - 文件最大尺寸 / 空位
    - 缩略图体积目标上限 / 详情展示图体积目标上限
    - 支持图片格式 / 支持视频格式
computed_style:
  selectors:
    - .admin-shell .settings-form-grid: grid-template-columns repeat(2, 1fr)
    - .admin-shell .settings-form-spacer: min-height 1px
    - '@media (max-width: 760px) .settings-form-spacer: display none'
  result: pass
```

## 实现证据

```yaml
backend:
  settings:
    - src/backend/app/services/effective_settings_service.py: media effective 默认 display_max_size_kb=768
    - src/backend/app/schemas/system_settings.py: MediaSettingsData / Patch 与 OpenAPI union response 暴露 display_max_size_kb
    - src/backend/app/services/system_settings_service.py: display_max_size_kb 校验范围 0-2048 KB
  generation:
    - src/backend/app/modules/media/storage.py: save_upload_file 接收 display_max_size_kb 并传入 .display 生成
    - src/backend/app/modules/media/tile_images.py: SKU pending 图片正式化补生成 .display 时读取 display_max_size_kb
    - src/backend/app/api/v1/uploads.py: 管理端图片上传入口读取 effective display_max_size_kb
    - src/backend/app/services/tile_sku_admin_service.py: SKU 图片保存正式化传入 effective display_max_size_kb
  maintenance:
    - src/backend/app/modules/media/maintenance.py: backfill-image-variants 与 formalize-pending-tile-images 读取 display_max_size_kb
web_admin:
  - src/web/src/pages/admin/SystemSettingsPage.tsx: 媒体设置页新增“详情展示图体积目标上限 (KB)”字段、默认值、帮助文案和保存校验
  - src/web/src/pages/admin/SystemSettingsPage.test.tsx: 覆盖字段展示、独立保存、非法范围、dirty/reset/toast 既有交互
api_and_docs:
  - src/web/openapi.json: MediaSettingsData 包含 display_max_size_kb
  - src/web/src/shared/api/generated.ts: Orval 生成 MediaSettingsData.display_max_size_kb
  - docs/03-api-index.md: 记录 media 字段、默认值和历史处理边界
  - docs/07-object-storage-strategy.md: 记录 .display 读取 media.display_max_size_kb
  - docs/standards/production-media-maintenance-runbook.md: 记录生产维护检查项和输出字段
env:
  status: not_changed
  reason: 新增配置项来自系统设置 KV/effective 默认值，不新增环境变量
```

## 媒体四联 Evidence

```yaml
key:
  status: pass
  evidence: .display key 仍由既有 derive_display_key / replace_pending_tile_path 规则生成，未改变 bucket、prefix 或文件名语义
object:
  status: pass
  evidence: 新上传和维护任务仍先保留原图对象；.display 生成失败或无法达标时记录 warning/失败原因，不阻断原图上传、业务保存或维护任务整体执行
url:
  status: pass
  evidence: 上传响应和 SKU 图片响应继续返回后端受控 /media/{object_key} 派生 URL；.display 缺失时沿用既有回退语义
render:
  status: pass_with_automated_dom_evidence
  evidence: SystemSettingsPage Vitest 覆盖字段展示、编辑保存、非法范围、reset/dirty/toast 交互；当前项目无 Playwright 截图入口，未生成新增像素截图
size_policy:
  before: display 图目标体积使用代码默认 768KB
  after: display 图目标体积读取 media.display_max_size_kb effective，默认仍为 768KB，并与 thumbnail_max_size_kb 独立
```

## 验证记录

```yaml
commands:
  - command: uv run pytest tests/test_system_settings.py tests/test_media_maintenance.py
    cwd: src/backend
    result: pass
    summary: 27 passed, 59 warnings
  - command: pnpm --pm-on-fail=warn --dir src/web test -- SystemSettingsPage.test.tsx
    result: pass
    summary: 62 files passed, 361 tests passed; pnpm 版本提示 11.2.2 vs 11.7.0，不影响执行结果
  - command: ./scripts/generate-openapi-client.sh
    result: pass
    summary: orval v8.17.0 converted
  - command: openspec validate add-admin-display-image-size-limit-setting --strict
    result: pass
    summary: Change valid
  - command: python scripts/validate-openspec-language.py
    result: pass
    summary: OpenSpec 文档语言校验通过
  - command: python scripts/sync-workflow-status.py --event opsx.apply --change add-admin-display-image-size-limit-setting --sprint auto
    result: pass
    summary: Updated 1, skipped 30, errors 0, acceptance pending
  - command: python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-admin-display-image-size-limit-setting --sprint sprint-025 --json
    result: warning
    summary: usage_mode unavailable; no command-runs/token_count events
  - command: pnpm --pm-on-fail=warn --dir src/web test -- SystemSettingsPage.test.tsx
    result: pass
    summary: opsx.modify 返修后 62 files passed, 361 tests passed；pnpm 版本提示 11.2.2 vs 11.7.0，不影响执行结果
  - command: git diff --check -- touched files
    result: pass
    summary: 无空白错误
  - command: openspec validate add-admin-display-image-size-limit-setting --strict
    result: pass
    summary: opsx.modify 返修后 Change valid
  - command: python scripts/validate-openspec-language.py
    result: pass
    summary: opsx.modify 返修后 OpenSpec 文档语言校验通过
  - command: python scripts/sync-workflow-status.py --event opsx.modify --change add-admin-display-image-size-limit-setting --sprint auto
    result: pass
    summary: Updated 3, skipped 28, errors 0, acceptance pending
  - command: python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change add-admin-display-image-size-limit-setting --sprint sprint-025 --json
    result: warning
    summary: usage_mode unavailable; no command-runs/token_count events
not_run:
  - command: uv run pytest ../../tests/test_media_storage.py
    reason: 当前 backend uv 环境缺少 PIL，测试收集阶段报 ModuleNotFoundError；REQ-0119 相关 display 配置读取已由系统设置、上传入口和维护任务测试覆盖
```

## Follow-up 评估

```yaml
need_follow_up: false
reason: 本次沿用现有系统设置页、media effective 配置和多规格生成链路，无新增可独立沉淀的治理规则；仅记录当前项目缺少浏览器截图测试入口，暂不自动创建 follow-up。
```
