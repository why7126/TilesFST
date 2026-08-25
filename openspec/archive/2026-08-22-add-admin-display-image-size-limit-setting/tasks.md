## 1. 后端系统设置

- [x] 1.1 在系统设置 media 默认配置中新增 `display_max_size_kb`，effective 默认值为 `768`。
- [x] 1.2 更新 media 分组 Pydantic Schema、GET、PATCH、reset 和字段校验，确保 display 字段与 `thumbnail_max_size_kb` 独立。
- [x] 1.3 确认系统设置持久化仍使用现有 KV 或等价事实源；如 seed/defaults 需要同步，补齐迁移或初始化逻辑。
- [x] 1.4 确认全部系统设置 media 接口继续使用管理员权限和统一 `ApiResponse`。

## 2. Display 派生生成

- [x] 2.1 将 `.display` 派生图体积目标从硬编码常量改为读取 `media.display_max_size_kb` effective 配置。
- [x] 2.2 覆盖新上传图片、SKU pending 图片正式化、品牌 Logo、Banner、品牌证书图片等实际生成 `.display` 的入口；不适用资源需记录原因。
- [x] 2.3 更新存量图片多规格维护任务，使 dry-run / apply 重生成 `.display` 时读取同一配置。
- [x] 2.4 保持 `.display` key、URL、bucket、前缀、MIME 和受控 `/media/...` 读取语义不变。
- [x] 2.5 对无法达到目标体积的 PNG、透明图或复杂纹理图片记录 warning 或失败原因，并确保不阻断原图上传、业务保存或维护任务整体执行。

## 3. 管理端 UI

- [x] 3.1 在 `/admin/settings/media` 新增「详情展示图体积目标上限 (KB)」字段，放在缩略图体积目标相邻的媒体生成策略区域。
- [x] 3.2 补齐字段帮助文案：默认 768KB、仅影响后续新生成 display 图、历史需维护任务重生成、与缩略图目标独立。
- [x] 3.3 覆盖加载、编辑 dirty、保存、保存失败、恢复默认、dirty 切换 Tab 确认和字段校验错误状态。
- [x] 3.4 保持单一 footer 保存 CTA、Design System modal、fixed toast、semantic token 和无 layout shift。

## 4. API、文档与生成物

- [x] 4.1 同步 FastAPI OpenAPI，确保系统设置 media 请求和响应 schema 包含 display 图体积目标字段。
- [x] 4.2 运行 `./scripts/generate-openapi-client.sh` 并同步 Orval 生成物。
- [x] 4.3 更新 `docs/03-api-index.md`、媒体文档、对象存储文档和维护任务说明，记录字段语义、默认值、生效范围和历史处理边界。
- [x] 4.4 更新 `.env.example` 或配置说明，仅在新增环境默认项时执行；若不新增 env，记录 N/A 理由。

## 5. 测试与验收

- [x] 5.1 补充后端系统设置测试，覆盖默认值、PATCH、reset、权限、字段范围和缩略图/display 互不影响。
- [x] 5.2 补充派生图生成测试，覆盖 `.display` 读取配置、无法达标 warning 和上传不阻断。
- [x] 5.3 补充维护任务测试，覆盖 dry-run 不写对象存储、apply 读取配置、成功/失败/跳过/重试候选摘要。
- [x] 5.4 补充管理端测试，覆盖字段展示、编辑、保存、恢复默认、dirty 确认、fixed toast 和 1440×1024 布局不被新增字段破坏。
- [x] 5.5 记录媒体四联 evidence：`.display` key、object、URL、render，以及体积目标配置变更前后的脱敏摘要。
- [x] 5.6 运行相关 pytest、Web 测试、OpenAPI / Orval 校验、`openspec validate add-admin-display-image-size-limit-setting --strict` 和 `python scripts/validate-openspec-language.py`。

## 6. 收尾

- [x] 6.1 回填 REQ-0119 acceptance、trace 和 Change trace 的实现证据、UI Contract evidence、截图和 computed style 检查。
- [x] 6.2 评估是否需要沉淀媒体配置或系统设置表单治理 follow-up；无明确复用价值时记录不沉淀。

## 执行说明

- `.env.example` 未更新：本需求新增的是系统设置 KV effective 默认值，不新增环境变量。
- 1440×1024 布局证据采用现有系统设置页 DOM/组件测试与代码复核；当前 Web 项目无 Playwright 或截图测试入口，未新增临时浏览器测试框架。

## 验收返修记录

- [x] 2026-08-22 22:18:00 `/opsx-modify REQ-0119`：按用户验收反馈优化媒体与存储 Tab「上传限制」2 列网格顺序，四行分别为图片最大尺寸 / 视频最大尺寸、文件最大尺寸 / 空位、缩略图体积目标上限 / 详情展示图体积目标上限、支持图片格式 / 支持视频格式。
- [x] 同步管理端测试，断言上传限制 grid 的 8 个子项顺序和第二行右侧占位。
- [x] 同步 Change UI Contract、system-settings delta spec、Change trace、REQ acceptance evidence 与 sprint-025 验收报告。
