## ADDED Requirements

### Requirement: 镜像构建脚本化入口
系统 SHALL 提供一个位于 `scripts/` 的 shell 脚本，用于从 env 文件读取配置并构建后端与 Web 生产镜像。

#### Scenario: 使用默认 env 文件构建镜像
- **WHEN** 操作人员执行镜像构建脚本且默认 env 文件存在
- **THEN** 系统 MUST 读取默认 env 文件中的镜像名、版本 tag、平台和构建参数，并构建后端与 Web 镜像

#### Scenario: 使用指定 env 文件构建镜像
- **WHEN** 操作人员执行镜像构建脚本并传入 env 文件路径
- **THEN** 系统 MUST 使用传入的 env 文件覆盖默认配置来源

### Requirement: 构建配置示例
系统 SHALL 提供一个可提交的 env 示例文件，说明镜像构建所需变量的用途、默认值含义和安全边界。

#### Scenario: 复制示例配置
- **WHEN** 操作人员需要准备镜像构建配置
- **THEN** 系统 MUST 提供可复制的 env 示例，且示例不得包含真实密钥、真实客户数据或敏感生产地址

### Requirement: 镜像验证与离线包导出
镜像构建脚本 SHALL 在构建后执行基础验证，并 SHALL 支持按 env 配置导出 gzip 离线镜像包与 sha256 校验文件。

#### Scenario: 构建后验证镜像
- **WHEN** 后端与 Web 镜像构建完成
- **THEN** 系统 MUST 验证镜像目标平台，并执行后端依赖导入检查与 Web Nginx 配置检查

#### Scenario: 导出离线包
- **WHEN** env 配置启用离线包导出
- **THEN** 系统 MUST 将后端与 Web 镜像导出为一个 gzip 压缩包，并生成对应的 sha256 校验文件
