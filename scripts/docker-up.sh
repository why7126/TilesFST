#!/usr/bin/env bash
# 文档用途：兼容旧 Docker Compose 启动入口
# 文档内容：转调 deploy/scripts/up.sh 的本地默认环境
# 内容来源：REQ-0093 standardize-deployment-environment-matrix
# 更新方式：默认本地环境变化时同步更新
# 备注：复杂环境解析统一维护在 deploy/scripts/up.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${ROOT_DIR}/deploy/scripts/up.sh" local sqlite-tencent-cos
