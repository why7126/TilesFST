# Tasks

- [x] 确认 BUG-0057 的当前 OpenAPI tags 漂移基线，记录多 tag、重复 tag、非 kebab-case tag 统计。
- [x] 统一后端 route tag 单一事实源，避免 router-level 与 decorator-level tags 叠加。
- [x] 将最终 OpenAPI operation tags 统一为 kebab-case 技术名。
- [x] 增强 `scripts/validate-api-standard.py`，校验最终 OpenAPI operation tags 的数量、重复与命名格式。
- [x] 增加回归测试，覆盖多 tag、重复 tag、非 kebab-case tag 会被校验脚本拦截。
- [x] 重新导出 `src/web/openapi.json`。
- [x] 如 Orval 生成物变化，运行 `./scripts/generate-openapi-client.sh` 并同步生成客户端。
- [x] 运行 `python scripts/validate-api-standard.py`、相关 pytest、OpenSpec 校验与目录结构校验。
- [x] 更新 BUG-0057 trace、Sprint 验收记录；如修复经验可复用，补充 `docs/knowledge-base/incidents/`。
