## MODIFIED Requirements

### Requirement: 构建配置示例
系统 SHALL 提供一个可提交的 env 示例文件，说明镜像构建所需变量的用途、默认值含义和安全边界。构建配置示例 MUST 将 `IMAGE_BUILD_TAG` 作为常规发版路径下唯一必须修改的版本号输入，离线交付输出目录与离线镜像包文件名 MUST 可由 `IMAGE_BUILD_TAG` 和 `IMAGE_BUILD_PLATFORM` 默认推导；仅特殊路径或命名场景才需要显式覆盖。

#### Scenario: 复制示例配置
- **WHEN** 操作人员需要准备镜像构建配置
- **THEN** 系统 MUST 提供可复制的 env 示例，且示例不得包含真实密钥、真实客户数据或敏感生产地址

#### Scenario: 常规发版只填写一次构建版本
- **WHEN** 操作人员复制 `scripts/build-images.env.example` 准备常规镜像构建
- **THEN** 示例 MUST 只要求操作人员修改 `IMAGE_BUILD_TAG` 表达版本号
- **AND** `IMAGE_BUILD_RELEASE_DIR` MUST 默认推导为与 `IMAGE_BUILD_TAG` 一致的 release 目录
- **AND** `IMAGE_BUILD_TAR_NAME` MUST 默认推导为包含 `IMAGE_BUILD_TAG` 与 `IMAGE_BUILD_PLATFORM` 的离线包文件名
