---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
status: done
created_at: 2026-08-06 10:39:49
updated_at: 2026-08-06 11:24:33
severity_hint: medium
environment: docker
related_requirement: REQ-0094-mintlify-versioned-docs-directory
related_bug:
---

# 现象

启用 `docs-site` profile 启动 `tilesfst-docs-site` 时，Mintlify 本地预览在 preparing local preview 阶段失败并反复输出：

```text
error EBUSY: resource busy or locked, rename '/home/node/.mintlify' -> '/home/node/.mintlify-last'
```

初步分析显示，当前 Compose 将 Docker named volume `tilesfst-docs-site-cache` 直接挂载到容器内 `/home/node/.mintlify`。Mintlify CLI 启动时会尝试将该目录重命名为 `/home/node/.mintlify-last`，但该路径是 volume 挂载点，导致 Linux 容器内 rename 返回 `EBUSY`。

# 复现步骤

1. 确认项目已生成 `mintlify/docs.json` 与 `mintlify/docs/**`。
2. 执行 `docker compose --profile docs-site up -d --build tilesfst-docs-site` 或通过本地启动脚本启用 docs-site profile。
3. 查看 `tilesfst-docs-site` 日志。

# 期望 vs 实际

期望：`tilesfst-docs-site` 可稳定启动 Mintlify 本地预览，文档站可通过 `HOST_PORT_MINTLIFY_DOCS` 访问；预览缓存不应依赖需要被 Mintlify CLI 重命名的 Docker volume 挂载点。

实际：Mintlify CLI 尝试重命名 `/home/node/.mintlify` 时触发 `EBUSY`，服务启动失败或反复重启。

# 附件

日志片段来自用户在 `/opsx-explore` 中提供的 `tilesfst-docs-site` 启动失败输出。
