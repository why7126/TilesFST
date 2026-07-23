---
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
status: approved
created_at: 2026-07-21 15:21:40
updated_at: 2026-07-21 22:55:15
related_requirement:
related_change: fix-prod-miniapp-video-upstream-502
---

# Acceptance - BUG-0076 生产环境微信小程序提示视频暂时无法播放

## 回归验收

| AC | 验收项 | 验收标准 | 证据 |
|---|---|---|---|
| AC-001 | 生产入口恢复 | `https://tilesfst.wjoyhappy.site/` 不返回 502 | 2026-07-21 22:53:19 未通过：返回 `HTTP/1.1 502 Bad Gateway`，Server `nginx/1.26.2` |
| AC-002 | 后端健康检查恢复 | `https://tilesfst.wjoyhappy.site/api/v1/health` 返回 200 与健康响应 | 2026-07-21 22:53:18 未通过：返回 `HTTP/1.1 502 Bad Gateway`，Server `nginx/1.26.2` |
| AC-003 | SKU 详情接口正常 | 实际反馈 SKU 的 `/api/v1/miniapp/skus/<SKU ID>` 返回 200，且视频项 `media[].url` 不为空 | 2026-07-21 22:53:20 未通过：`/api/v1/miniapp/skus/1` 返回 `HTTP/1.1 502 Bad Gateway`，尚无法读取实际 `media[].url` |
| AC-004 | 视频媒体 URL 可读 | 实际视频 `/media/{object_key}` 返回 200，`Content-Type` 为小程序可播放视频类型，且不是 Nginx 502 页面 | curl 响应头 |
| AC-005 | 小程序真机可播放 | 生产微信小程序中实际反馈页面的视频可加载并播放，不再显示「视频暂时无法播放」 | 真机截图或录屏 |
| AC-006 | 失败兜底仍可诊断 | 对不存在或权限异常的视频对象，页面仍显示可理解提示，后端日志能定位对象或存储错误 | 人工验证记录 |
| AC-007 | BUG-0069 回归覆盖 | `tile_videos.object_key` 与 `file_name` 不同时，详情接口仍使用 object_key 生成 `/media/...` | 后端测试或生产抽样 |

## Apply Evidence - 2026-07-21

- 生产 smoke 仍未通过：根路径、`/api/v1/health`、`/api/v1/miniapp/skus/1` 均返回 Nginx 502。
- 本地指定回归通过：`uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states`，结果 `2 passed, 3 warnings`。
- 当前无法完成实际反馈 SKU、实际 `/media/{object_key}` 与微信真机播放验收；需先恢复生产外层 Nginx upstream 或生产容器运行状态。

## 建议测试

```bash
uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states
```

## 生产 Smoke 建议

1. `curl -I https://tilesfst.wjoyhappy.site/`
2. `curl -i https://tilesfst.wjoyhappy.site/api/v1/health`
3. `curl -i https://tilesfst.wjoyhappy.site/api/v1/miniapp/skus/<实际 SKU ID>`
4. `curl -I https://tilesfst.wjoyhappy.site/media/<实际视频 object_key>`
5. 使用微信真机打开同一 SKU 页面并播放视频。

## 出口标准

- 所有必选 AC 均通过。
- 若修复仅涉及生产部署或配置，需在验收记录中说明未修改 API、数据库、Web、小程序代码，不需要 Orval。
- 若发现需要代码修复，应在 `BUG-0076` 评审通过后创建 OpenSpec Change，再进入 Sprint 实现。
