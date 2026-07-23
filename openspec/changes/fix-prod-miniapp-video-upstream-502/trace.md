---
change_id: fix-prod-miniapp-video-upstream-502
type: fix
status: proposed
created_at: 2026-07-21 15:32:00
updated_at: 2026-07-22 10:40:27
source_bug: BUG-0076-prod-miniapp-video-temporarily-unplayable
related_requirement:
sprint:
---

# Trace - fix-prod-miniapp-video-upstream-502

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | BUG-0076-prod-miniapp-video-temporarily-unplayable | 生产环境微信小程序提示视频暂时无法播放，生产域名多入口返回 Nginx 502 |
| Related BUG | BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 历史视频 URL 字段语义修复，作为本次回归参考 |

## 状态

```yaml
change_id: fix-prod-miniapp-video-upstream-502
status: proposed
source_bug: BUG-0076-prod-miniapp-video-temporarily-unplayable
iteration:
tasks:
  total: 18
  completed: 2
```

## Apply Evidence

| 时间 | 类型 | 结果 | 证据 |
|---|---|---|---|
| 2026-07-21 22:53:18 | production-smoke | failed | `curl -i -L --max-time 10 https://tilesfst.wjoyhappy.site/api/v1/health` 返回 `HTTP/1.1 502 Bad Gateway`，Server `nginx/1.26.2` |
| 2026-07-21 22:53:19 | production-smoke | failed | `curl -I -L --max-time 10 https://tilesfst.wjoyhappy.site/` 返回 `HTTP/1.1 502 Bad Gateway`，Server `nginx/1.26.2` |
| 2026-07-21 22:53:20 | production-smoke | failed | `curl -i -L --max-time 10 https://tilesfst.wjoyhappy.site/api/v1/miniapp/skus/1` 返回 `HTTP/1.1 502 Bad Gateway`，Server `nginx/1.26.2` |
| 2026-07-21 22:55:15 | local-regression | passed | 指定 pytest 2 passed，覆盖 SKU 详情 object_key 视频 URL 与小程序媒体失败兜底静态检查 |

## 当前阻塞

生产外层入口仍返回 Nginx 502，无法在本地仓库内确认或修复 `tilesfst-web`、`tilesfst-backend`、外层 Nginx upstream、生产端口映射、生产 DB/对象存储依赖或微信真机播放结果。继续完成 1.1-2.4、3.1、3.3、4.2、4.5 需要生产服务器运维证据或访问权限。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 10:40:27 | /sprint-propose | 因暂时无法提供生产修复与验收条件，移出 sprint-010 正式范围；保留 Change 待后续重新规划 |
| 2026-07-21 22:55:15 | /opsx-apply | 生产根路径、健康检查与 SKU 接口 smoke 仍返回 Nginx 502；本地指定回归测试通过；保留生产修复项未完成 |
| 2026-07-21 15:37:29 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 15:32:00 | /bug-opsx | 从 BUG-0076 创建 OpenSpec fix Change |
