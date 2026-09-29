#!/usr/bin/env python3
"""知识模型格式、本体与Sprint一致性只读入口。"""
import sys
from knowledge_model.cli import main
if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:] or ['model']))
