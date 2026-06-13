#!/usr/bin/env bash
set -euo pipefail
(cd src/backend && uv run pytest)
