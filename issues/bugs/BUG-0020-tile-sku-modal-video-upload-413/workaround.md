---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
status: pending_review
created_at: 2026-06-27 15:23:29
updated_at: 2026-06-27 15:23:29
---

# 临时规避方案

## 1. 操作规避（可部分恢复上传，非正式验收）

在正式修复并重建 Web 镜像前，运营/开发可临时绕过 Nginx 1MB 限制：

1. **直连后端上传（开发调试）**  
   将前端 API 基址指向 `http://localhost:8000`（`VITE_API_BASE_URL` 或临时改 Orval/axios baseURL），在 **Vite 5173** 或直连后端环境下上传大 MP4。  
   **限制**：与生产/Docker 演示路径不一致，**不得**作为 AC 通过依据。

2. **使用极小样例视频（< 1MB）**  
   在仍走 `localhost:3000` 时，仅当 MP4 **小于 Nginx 默认上限** 时可能成功。  
   **限制**：真实商品视频几乎无法满足；仅作连通性 smoke test。

3. **DevTools 对照**  
   Network 中若见 **413** 且 URL 为 `localhost:3000`，可确认为代理层问题而非 MinIO/后端业务错误；对照直连 `8000` 同文件验证。

## 2. 功能规避

**无产品级可靠规避。** Docker Compose 默认 Web 入口下，常规体积 MP4 无法稳定上传，REQ-0006 多视频能力不可用。

## 3. 验收规避

修复前，REQ-0006 **AC-035**（多视频上传）在 **`localhost:3000` 端到端路径** **不得标记通过**。

本 BUG `acceptance.md` 中 Docker 路径大文件上传 MUST 判失败直至修复验收完成。

## 4. 风险说明

- SKU 视频素材无法在演示/本地 Docker 环境维护，阻塞迭代验收与运营试用。
- 同一 Nginx 下大图（>1MB）Logo/图片上传亦可能 413，易被误判为「仅视频有问题」。
- 与 BUG-0018 叠加时，用户看到「上传失败」，难以区分代理 413 与 UI 回显问题。

## 5. 建议优先级

severity **high**；应与 REQ-0006 视频验收同批处理，优先于纯视觉 medium 类缺陷。修复后须 **重建 Web 容器镜像** 使 Nginx 配置生效。
