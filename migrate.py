#!/usr/bin/env python3
"""
数据库迁移工具
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.migrations.add_api_code_field import migrate_database, rollback_migration

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "migrate":
            print("执行数据库迁移...")
            migrate_database()
        elif command == "rollback":
            print("回滚数据库迁移...")
            rollback_migration()
        else:
            print("未知命令。使用方法:")
            print("  python migrate.py migrate   - 执行迁移")
            print("  python migrate.py rollback  - 回滚迁移")
            sys.exit(1)
    else:
        print("使用方法:")
        print("  python migrate.py migrate   - 执行迁移")
        print("  python migrate.py rollback  - 回滚迁移")
        sys.exit(1)

if __name__ == "__main__":
    main()
