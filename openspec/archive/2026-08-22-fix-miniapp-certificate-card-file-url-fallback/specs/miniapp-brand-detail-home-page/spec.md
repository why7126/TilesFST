## MODIFIED Requirements

### Requirement: 品牌主页证书 Tab

证书 Tab SHALL 展示当前品牌关联且可公开的证书列表，并过滤不可展示证书和内部字段。证书 Tab 图片小图 SHALL 优先使用后端受控真实缩略图、卡片专用小图或等价轻量图片 URL；图片预览、证书详情或文件打开 SHALL 使用原图、原文件或等价安全引用。证书 Tab SHALL 对非首屏图片类证书启用懒加载或等价延迟加载策略，并在缩略图缺失、不可读或加载失败时展示统一占位或受控失败态，SHALL NOT 在卡片图片 `src` 中 fallback 到 `file_url`、原图或原始文件 URL。

#### Scenario: 证书图片使用缩略图且预览保留原图

- **WHEN** 用户查看品牌详情页证书 Tab 且证书为图片类资源
- **THEN** 证书列表小图 SHALL 优先使用同目录 `.thumb` 缩略图或等价轻量图片 URL
- **AND** 缩略图缺失、不可读、为空或图片加载失败时 SHALL 展示统一证书占位或受控失败态
- **AND** 卡片图片 SHALL NOT 使用 `file_url`、原图或原始文件 URL 作为默认 fallback
- **AND** 图片预览或证书详情 SHALL 使用原图、原文件或等价受控高清 URL
- **AND** 非首屏证书图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略。
