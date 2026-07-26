---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
created_at: 2026-07-23 09:00:31
updated_at: 2026-07-23 10:08:26
related_requirement:
related_change: fix-upload-proxy-timeout-config
---

# Acceptance - BUG-0081 生产环境腾讯 COS 视频上传 99% 后返回 504

## 回归验收

| AC | 验收项 | 验收标准 | 证据 |
|---|---|---|---|
| AC-001 | 外层反代上传超时 | `tilesfst.wjoyhappy.site` 的 HTTPS Nginx 对 `/api/v1/admin/uploads/` 配置 `proxy_read_timeout`、`proxy_send_timeout`、`client_body_timeout`、`send_timeout`，上传超时不低于 300s，推荐 600s | Nginx 配置片段与 `nginx -t` 输出 |
| AC-002 | 外层 body size | 外层 443 server 的 `client_max_body_size` 不小于 `MAX_VIDEO_SIZE_MB`，默认至少 512m | Nginx 配置片段 |
| AC-003 | 内层 Web Nginx 上传 location | 容器内 Web Nginx 在通用 `/api/` 前配置 `/api/v1/admin/uploads/` 专用 location，超时策略与外层一致 | `src/web/nginx.conf` 或生产等价配置 |
| AC-004 | 环境变量化 | 上传反代超时时间通过 `.env.example`、Compose、Nginx 模板渲染或启动脚本支持配置；默认值建议 600s | 配置、模板、文档与测试 |
| AC-005 | 合法视频上传成功 | 在生产管理端上传同一类视频文件，浏览器 Network 返回 200，响应体包含 `object_key` 与 `/media/{object_key}` | 浏览器截图或 curl/API 响应 |
| AC-006 | COS 对象写入一致 | 上传成功后 COS 中存在对应 `videos/default/tiles/{tile_id|pending}/{uuid}.{ext}` 对象，且该 object_key 与接口响应一致 | COS 控制台或对象列表截图 |
| AC-007 | SKU 表单保存闭环 | 上传返回的视频出现在 SKU 表单中，保存后刷新页面仍可看到该视频 | 管理端截图或接口响应 |
| AC-008 | 媒体受控读取 | 上传返回的 `/media/{object_key}` 经后端受控读取返回 200，Content-Type 为对应视频 MIME | `curl -I` 或浏览器响应头 |
| AC-009 | 不再出现超时日志 | 同类上传不再出现浏览器 504、外层 504、容器 Nginx 60 秒后 499 | Nginx access/error log |
| AC-010 | 现有上传能力回归 | 品牌 Logo、SKU 图片、品牌证书上传仍可正常返回 200，错误码和大小限制不回退 | 后端/前端回归测试或人工验证 |
| AC-011 | 孤儿对象风险可控 | 若上传接口返回失败，不应产生无法追踪的大量 COS 孤儿对象；至少文档说明清理策略或运维检查步骤 | 文档或清理验证记录 |

## 建议测试

后续进入修复实现后，建议补充或运行：

```bash
uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py
```

若实现 Nginx 模板环境变量渲染，还应增加针对模板输出的测试，验证默认 `600s` 与环境变量覆盖值能正确渲染到上传专用 location。

## 生产 Smoke 建议

1. `nginx -t` 验证外层 Nginx 配置合法。
2. `curl -I https://tilesfst.wjoyhappy.site/` 验证站点入口正常。
3. 登录管理端，上传实际失败过的视频文件。
4. 确认上传请求返回 200，而非 504。
5. 确认 COS 中对应对象存在。
6. 保存 SKU 后刷新管理端页面，确认视频仍关联在该 SKU。
7. 访问 `/media/{object_key}`，确认可通过后端读取。
8. 观察外层与容器内 Nginx 日志，确认不再出现本次 60 秒 499/504 模式。

## 出口标准

- 所有必选 AC 均通过。
- 修复若涉及 Nginx、Docker、`.env.example`、部署文档或测试，必须同步更新相应文档和测试。
- 若 API 路径、请求/响应 Schema 不变，则无需 Orval。
- 若仅调整部署配置，不涉及数据库结构变更。
- 若引入环境变量化 Nginx 模板，需在发布说明中提醒生产重建并重启 Web 镜像，同时外层 HTTPS Nginx 仍需人工或运维模板同步配置。
