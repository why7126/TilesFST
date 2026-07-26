---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
review_result: approved
reviewed_at: 2026-07-23 09:04:56
created_at: 2026-07-23 09:04:56
updated_at: 2026-07-23 10:08:26
reviewer: AI
related_requirement:
related_change: fix-upload-proxy-timeout-config
---

# Review - BUG-0081 生产环境腾讯 COS 视频上传 99% 后返回 504

## 评审结论

确认修复，状态评审通过。

该问题发生在生产环境管理端，用户可见现象为视频上传进度卡在 99%，浏览器返回 `504 Gateway Time-out`。腾讯 COS 中已经出现对应文件，且 Nginx 日志显示请求体进入临时文件缓冲后约 60 秒记录为 `499`。现有证据足以支持“大文件上传反代/网关超时导致上传响应链路失败”的判断，应进入修复流程。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 浏览器 504、COS 已有对象、Nginx 60 秒后 499 与请求体缓冲证据构成完整链路 |
| 严重等级合理 | 通过 | 生产管理端视频上传闭环失败，并可能留下 COS 孤儿对象，`high` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖外层/内层 Nginx 超时、环境变量化、上传成功、COS 一致性与回归范围 |
| 是否需要 hotfix | 倾向需要 | 生产上传功能已受影响，可先按运维 hotfix 调整外层与内层反代超时；代码化环境变量配置需走 OpenSpec Change |

## 处理建议

1. 生产现场可先按 `workaround.md` 调整外层 HTTPS Nginx 与容器内 Web Nginx 上传专用超时，验证同一视频不再 504。
2. 执行 `/bug-opsx BUG-0081-prod-cos-video-upload-fails` 创建修复 Change，正式实现容器内 Nginx 上传 location、超时时间环境变量化、部署文档与测试。
3. 在进入 `/opsx-apply` 前，按项目门禁将该 BUG 与修复 Change 纳入 Sprint 正式范围。
4. 修复验收时同时检查 COS 是否仍产生重复孤儿对象。

## 后续命令

```bash
/bug-opsx BUG-0081-prod-cos-video-upload-fails
```
