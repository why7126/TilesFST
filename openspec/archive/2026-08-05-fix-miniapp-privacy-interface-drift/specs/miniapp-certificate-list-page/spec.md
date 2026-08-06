---
change_id: fix-miniapp-privacy-interface-drift
capability: miniapp-certificate-list-page
created_at: 2026-08-05 14:42:11
updated_at: 2026-08-05 14:42:11
---

## MODIFIED Requirements

### Requirement: 证书文件预览

系统 SHALL 在证书详情页提供图片预览与 PDF/文件打开能力，并 SHALL 在失败路径中保持稳定错误提示。失败兜底不得触发剪贴板隐私接口，不得复制文件 URL。

#### Scenario: PDF 证书预览

- **WHEN** 用户在证书详情页点击 PDF 证书打开入口
- **THEN** 小程序 SHALL 优先通过受控 URL 下载并使用 `wx.openDocument` 打开 PDF 或文件
- **AND** 下载失败、状态码异常或 `wx.openDocument` 失败时 SHALL 展示稳定错误提示
- **AND** 小程序 SHALL NOT 调用 `wx.setClipboardData`
- **AND** 小程序 SHALL NOT 展示“文件链接已复制”或等价复制成功提示
- **AND** 小程序 SHALL NOT 暴露未授权对象存储直连地址或原始 object key。
