"""
数据库迁移脚本：添加 api_code 字段
将现有的 JSON 定义中的 apiCode 提取到独立字段中
"""
import os
import json
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.models import ApiDefinition, Base

def migrate_database():
    """执行数据库迁移"""
    # 数据库路径
    DB_PATH = os.getenv("API_DB_PATH", "sqlite:///ocr_api_management.db")
    
    print(f"开始迁移数据库: {DB_PATH}")
    
    # 创建引擎和会话
    engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # 1. 检查是否已经有 api_code 字段
        result = session.execute(text("PRAGMA table_info(api_definitions)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'api_code' in columns:
            print("api_code 字段已存在，跳过迁移")
            return
        
        print("添加 api_code 字段...")
        
        # 2. 添加 api_code 字段
        session.execute(text("ALTER TABLE api_definitions ADD COLUMN api_code VARCHAR(64)"))
        session.commit()
        
        # 3. 从现有记录中提取 apiCode 并更新
        print("从现有记录中提取 apiCode...")
        
        # 获取所有现有记录
        api_defs = session.query(ApiDefinition).all()
        
        updated_count = 0
        error_count = 0
        
        for api_def in api_defs:
            try:
                # 解析 JSON 定义
                definition = json.loads(api_def.definition)
                api_code = definition.get('apiCode')
                
                if api_code:
                    # 检查是否有重复的 api_code
                    existing = session.query(ApiDefinition).filter(
                        ApiDefinition.api_code == api_code,
                        ApiDefinition.id != api_def.id
                    ).first()
                    
                    if existing:
                        # 如果有重复，添加后缀
                        counter = 1
                        original_code = api_code
                        while existing:
                            api_code = f"{original_code}_{counter}"
                            existing = session.query(ApiDefinition).filter(
                                ApiDefinition.api_code == api_code,
                                ApiDefinition.id != api_def.id
                            ).first()
                            counter += 1
                        print(f"警告: API CODE 重复，将 {original_code} 改为 {api_code}")
                    
                    # 更新记录
                    session.execute(
                        text("UPDATE api_definitions SET api_code = :api_code WHERE id = :id"),
                        {"api_code": api_code, "id": api_def.id}
                    )
                    updated_count += 1
                    print(f"更新记录 ID {api_def.id}: api_code = {api_code}")
                else:
                    # 如果没有 apiCode，生成一个默认值
                    default_code = f"API_{api_def.id:03d}"
                    session.execute(
                        text("UPDATE api_definitions SET api_code = :api_code WHERE id = :id"),
                        {"api_code": default_code, "id": api_def.id}
                    )
                    updated_count += 1
                    print(f"记录 ID {api_def.id} 没有 apiCode，生成默认值: {default_code}")
                    
            except Exception as e:
                error_count += 1
                print(f"处理记录 ID {api_def.id} 时出错: {str(e)}")
                # 为出错的记录生成默认 api_code
                default_code = f"ERROR_{api_def.id:03d}"
                session.execute(
                    text("UPDATE api_definitions SET api_code = :api_code WHERE id = :id"),
                    {"api_code": default_code, "id": api_def.id}
                )
        
        session.commit()
        
        # 4. 添加唯一约束和索引
        print("添加唯一约束和索引...")
        session.execute(text("CREATE UNIQUE INDEX idx_api_definitions_api_code ON api_definitions(api_code)"))
        session.commit()
        
        print(f"迁移完成!")
        print(f"成功更新 {updated_count} 条记录")
        if error_count > 0:
            print(f"处理错误 {error_count} 条记录")
            
    except Exception as e:
        session.rollback()
        print(f"迁移失败: {str(e)}")
        raise
    finally:
        session.close()

def rollback_migration():
    """回滚迁移（删除 api_code 字段）"""
    DB_PATH = os.getenv("API_DB_PATH", "sqlite:///ocr_api_management.db")
    
    print(f"回滚数据库迁移: {DB_PATH}")
    
    engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        # SQLite 不支持 DROP COLUMN，需要重建表
        print("SQLite 不支持直接删除列，需要重建表...")
        
        # 1. 创建备份表
        session.execute(text("""
            CREATE TABLE api_definitions_backup AS 
            SELECT id, name, description, definition, created_at 
            FROM api_definitions
        """))
        
        # 2. 删除原表
        session.execute(text("DROP TABLE api_definitions"))
        
        # 3. 重命名备份表
        session.execute(text("ALTER TABLE api_definitions_backup RENAME TO api_definitions"))
        
        session.commit()
        print("回滚完成!")
        
    except Exception as e:
        session.rollback()
        print(f"回滚失败: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback_migration()
    else:
        migrate_database()
