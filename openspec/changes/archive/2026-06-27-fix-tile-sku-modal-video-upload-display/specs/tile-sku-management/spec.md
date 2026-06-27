## ADDED Requirements

### Requirement: SKU 弹窗视频上传 UX 对齐 AC-035

SKU 管理弹窗（新增/编辑）「商品视频」能力 MUST 对齐 REQ-0006 **AC-035**：支持上传多个视频；以 **视频预览/播放器卡片** 展示缩略图与播放能力，并展示名称、大小/时长、**上传状态**；同一弹窗会话内 MUST 即时回显已上传视频。本 requirement 聚焦 **即时回显与上传状态**；保存后重开回填与列表页视频计数 MAY 在其它 change 验收。

#### Scenario: AC-035 即时回显 gate

- **WHEN** 团队在 SKU 弹窗内成功上传至少一个 MP4（同一弹窗会话，未关闭弹窗）
- **THEN** 「商品视频」区块 MUST 立即展示对应视频预览/播放器卡片（文件名 + 大小或占位）
- **AND** 上传过程 MUST 展示可感知上传状态
- **AND** 验收结果 MUST 记录在 fix change `trace.md`

#### Scenario: 弹窗视频区并排验收

- **WHEN** 打开新增/编辑 SKU 弹窗并排 `tile-sku-create-modal.html`「商品视频」区块
- **THEN** checklist（上传按钮、视频预览/播放器列表、移除入口、上传状态反馈）MUST pass

#### Scenario: 多视频追加验收

- **WHEN** 用户在同一弹窗会话内连续上传两个 MP4 且均成功
- **THEN** 视频列表 MUST 展示两个文件卡片
- **AND** 移除其中一个后列表 MUST 正确更新
