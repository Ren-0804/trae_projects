#!/usr/bin/env python3
import asyncio
import sys
import os
import aiosqlite
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def fix_database():
    """修复数据库表结构"""
    try:
        async with aiosqlite.connect("driver_management.db") as db:
            # 检查现有列
            cursor = await db.execute("PRAGMA table_info(tasks)")
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]

            # 需要添加的列及其定义
            columns_to_add = {
                'sort_index': 'INTEGER DEFAULT 0',
                'labels': 'TEXT',
                'custom_fields': 'TEXT',
                'task_no': 'VARCHAR(50)',
                'origin_address': 'TEXT',
                'origin_lat': 'DECIMAL(10,7)',
                'origin_lng': 'DECIMAL(10,7)',
                'destination_address': 'TEXT',
                'destination_lat': 'DECIMAL(10,7)',
                'destination_lng': 'DECIMAL(10,7)',
                'estimated_distance_km': 'DECIMAL(10,2)',
                'estimated_duration_min': 'INTEGER'
            }

            for col_name, col_def in columns_to_add.items():
                if col_name not in column_names:
                    print(f"添加{col_name}列到tasks表...")
                    await db.execute(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_def}")
                    await db.commit()
                    print(f"{col_name}列添加成功!")
                else:
                    print(f"{col_name}列已存在!")

    except Exception as e:
        print(f"修复失败: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(fix_database())