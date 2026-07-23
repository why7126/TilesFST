---
bug_id: BUG-0073-video-upload-23m-file-fails
title: 上传 23M 视频文件失败
status: done
created_at: 2026-07-21 10:12:43
updated_at: 2026-07-22 09:20:59
severity_hint: high
environment: 待确认
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 项目已有媒体上传与视频资料管理能力，23M 视频文件上传失败属于既有上传链路在文件大小、后端校验、网关限制或 MinIO 写入环节上的行为偏差，倾向记录为 BUG。
related_requirement:
related_bug:
---

# 现象

用户反馈上传 23M 的视频文件失败。

# 复现步骤

1. 进入支持上传视频文件的页面或入口。
2. 选择一个约 23M 的视频文件。
3. 发起上传。
4. 观察上传请求、页面提示和后端日志。

# 期望 vs 实际

期望：符合系统限制的视频文件应能正常上传并返回可用于后续展示或播放的媒体地址；若文件不符合限制，应返回明确的错误码、大小限制说明和可操作提示。

实际：约 23M 的视频文件上传失败，暂未确认失败发生在前端校验、后端请求体限制、媒体类型校验、对象存储写入、代理层大小限制或超时环节。

# 附件

- 用户原始反馈：`上传23M的视频文件失败了`
- 暂无上传入口、文件格式、错误提示、Network 响应体、后端日志；后续 `/bug-explore` 阶段需补充。
