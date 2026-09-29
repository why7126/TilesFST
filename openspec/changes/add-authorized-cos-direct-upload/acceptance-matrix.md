---
created_at: 2026-09-08 17:55:29
updated_at: '2026-09-11 09:17:10'
---

# REQ-0135验收证据矩阵

本矩阵记录实现与验证边界，不表示用户正式验收或允许归档。任务21/22完成；4.4保留待验证。完整实验数据、时间与限制以[validation.md](validation.md)及evidence内脱敏结果为事实源。

| 条目 | 当前结果 | 证据与边界 |
|---|---|---|
| AC-001 鉴权归属 | 本地通过 | test_upload_session_service.py：逐操作所有者、角色、资源、跨品牌/用户/业务拒绝 |
| AC-002 最小授权/上限 | 本地与COS通过 | test_cos_upload_gateway.py、前期真实COS长度/版本实验及compose-boundary-result.json |
| AC-003 文件直达COS | 实际隔离环境通过 | compose-entrances-result.json、既有视频Network、performance-egress.json |
| AC-004 重试/续期/取消 | 本地与COS通过 | media-upload-controller.test.ts、真实分片403恢复与取消证据 |
| AC-005 对象确认 | 本地与COS通过 | 固定版本/精确大小/分片/前缀检查；不宣称完整视频/PDF解析或恶意内容扫描 |
| AC-006 幂等/恢复 | 本地通过 | SQLite/MySQL仓储验证、worker租约恢复、重复确认与保存 |
| AC-007 取消竞态 | 本地与COS通过 | CAS、晚到结果隔离、真实分片终止及测试清理 |
| AC-008 源覆盖隔离 | 本地与COS通过 | 固定版本复制、原授权覆盖反例、正式引用事务 |
| AC-009 保存失败重试 | 本地通过 | SKU/Logo/Banner/头像/证书复制及DB写入失败；资料页仅重试业务保存 |
| AC-010 图片派生契约 | 本地与COS通过 | test_image_upload_worker.py、受限worker规格/超时验证、实际图片处理；生产2GB宿主机资源仍未验收 |
| AC-011 残留清理 | 本地与COS通过 | test_media_upload_sessions.py与精确Key/Version清理；已绑定正式媒体保护，不宣称自动回收其全部临时历史版本 |
| AC-012 灰度回滚 | 本地与隔离Compose通过 | disabling_new_uploads测试、compose-rollback-result.json；非生产回滚 |
| AC-013 展示四联 | 部分通过 | Web入口存储/API/HTTP/render见compose-four-links.json与final-modal-matrix.json；小程序新增5类直传媒体DevTools展示见sept11-four-links.json及截图；真机未证，店主Web当前无媒体入口待适用性确认 |
| AC-014 全入口接入 | 已实现并验证 | SKU视频/图片、Logo、Banner、头像、证书图片/PDF；入口权限与类型见API索引第12节 |
| AC-015 冻结性能 | 隔离环境通过 | performance-summary.json及原始配对记录；有效上限用临时1MiB验证，非默认500MiB实传，非北京生产网络 |
| AC-016 分层关联 | 本地与实际接口通过 | media_upload事件、会话Task Trace、绑定/派生/清理；duration_scope区分嵌套与来源 |
| AC-017 脱敏/保留/契约 | 本地通过 | test_upload_observability.py、统一错误、Orval、既有SQLite/MySQL schema；全局TSC仍有3项基线问题 |
| AC-018 Compose/生产/真机 | 部分通过 | 隔离Web13000映射经过Nginx，3000已被现有环境使用；生产COS规则已验证，生产应用与小程序真机未证 |
| AC-XCUT-001 弹窗类冲突 | Web通过 | 专属弹窗与通用类不混用；现有CSS回归及真实构建computed classes |
| AC-XCUT-002 视口/宽度 | Web通过 | SKU目标880px；复用Logo/Banner/用户/证书各自既有宽度；1440、矮屏、窄屏矩阵 |
| AC-XCUT-003 就近状态 | Web通过 | 共享阶段组件、失败/取消/重试/保存锁定测试与对应截图 |
| AC-XCUT-004 预览保持 | Web通过 | 就绪预览、失败保留、保存重开decode；原生端展示另由AC-013验证 |
| AC-XCUT-005 代理入口边界 | 隔离环境通过 | 13000映射替代已占用3000；精确1MiB/+1byte，无413；直传主体Nginx gate为N/A |
| AC-XCUT-006 存储/历史读取 | 本地与隔离环境通过 | 适配层与旧路径回归、COS存在性和Web渲染；测试没有新建data/uploads媒体目录 |

## 设计条件

C-001授权及C-002事务/稳定版本已有前期供应商与数据库证据。C-003冻结参数的当前客户端性能目标通过，生产链路不作推定。C-004采用后端异步Pillow并已验证受限worker，不调用付费云端图片处理。C-005的Web上传UI在真实CSS/读取链路完成验收，小程序/店主端展示回归仍独立保留在4.4。

## 剩余验证动作

小程序新SKU图片/视频、Logo、Banner和证书图已补真实DevTools四联证据，详见validation.md“9月11日小程序新直传媒体补验”。保留真机/体验版未证边界，等待用户确认可用设备或本次验收处理方式。当前Web首页只有入口占位，店主端无实际媒体展示路由；已请求用户确认当前不适用或指定目标入口，不自动删除该分项。4.4维持待验，不能据本次新增证据自动归档。

## 执行链路复盘

REQ-0135 → sprint-029 → add-authorized-cos-direct-upload保持in_progress。当前实施解决了图片异步处理及多入口事务引用，测试证明客户端开销接近最小探针且视频主体不占后端出口；不据本机结果推断生产上传改善百分比。源码和全局独立类型检查的3项基线差异已单列，未静默修改无关主题逻辑。无明显新增规范优化点，未自动创建follow-up Issue或Change。
