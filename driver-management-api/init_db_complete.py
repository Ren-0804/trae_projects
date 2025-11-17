#!/usr/bin/env python3
"""
司机管理系统数据库初始化脚本
包含完整的表结构创建和数据初始化
"""

import sqlite3
import os
from datetime import datetime, timedelta
import json
from pathlib import Path

def init_database():
    """初始化数据库"""
    db_path = "driver_management.db"
    
    # 如果数据库已存在，先备份
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(db_path, backup_path)
        print(f"已备份现有数据库到: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100),
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'employee',
                is_active BOOLEAN DEFAULT 1,
                last_login_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建司机表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name VARCHAR(50) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                id_card VARCHAR(18) UNIQUE NOT NULL,
                license_number VARCHAR(20) UNIQUE NOT NULL,
                license_type VARCHAR(20) NOT NULL,
                main_route VARCHAR(200) NOT NULL,
                vehicle_type VARCHAR(50) NOT NULL,
                vehicle_length VARCHAR(20),
                price_per_km DECIMAL(10, 2) DEFAULT 0.00,
                experience_years INTEGER DEFAULT 0,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                region_type VARCHAR(10) NOT NULL DEFAULT '国内',
                emergency_contact VARCHAR(50),
                emergency_phone VARCHAR(20),
                remark TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建司机照片表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS driver_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                photo_type VARCHAR(50) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_name VARCHAR(200) NOT NULL,
                file_size INTEGER,
                mime_type VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建车辆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate_number VARCHAR(20) UNIQUE NOT NULL,
                vehicle_type VARCHAR(50) NOT NULL,
                brand VARCHAR(50),
                model VARCHAR(50),
                year INTEGER,
                color VARCHAR(20),
                engine_number VARCHAR(50),
                vin_number VARCHAR(50) UNIQUE,
                purchase_date DATETIME,
                registration_date DATETIME,
                insurance_expiry DATETIME,
                annual_inspection_date DATETIME,
                maintenance_due_date DATETIME,
                mileage DECIMAL(10, 2) DEFAULT 0.00,
                fuel_type VARCHAR(20),
                fuel_consumption DECIMAL(5, 2) DEFAULT 0.00,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                current_driver_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (current_driver_id) REFERENCES drivers(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建车辆分配表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                driver_id INTEGER NOT NULL,
                assignment_type VARCHAR(20) NOT NULL,
                start_date DATETIME NOT NULL,
                end_date DATETIME,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建排班表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                vehicle_id INTEGER,
                schedule_date DATETIME NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                route VARCHAR(200),
                task_type VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建司机证书表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS driver_certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                certificate_type VARCHAR(50) NOT NULL,
                certificate_number VARCHAR(100) NOT NULL,
                issue_date DATETIME,
                expiry_date DATETIME NOT NULL,
                issuing_authority VARCHAR(100),
                status VARCHAR(20) NOT NULL DEFAULT 'valid',
                file_path VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建维护记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                maintenance_type VARCHAR(50) NOT NULL,
                description TEXT,
                cost DECIMAL(10, 2) DEFAULT 0.00,
                mileage_at_service DECIMAL(10, 2),
                service_date DATETIME NOT NULL,
                next_service_date DATETIME,
                service_provider VARCHAR(100),
                invoice_number VARCHAR(50),
                status VARCHAR(20) NOT NULL DEFAULT 'completed',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建GPS记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gps_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                driver_id INTEGER,
                latitude DECIMAL(10, 7) NOT NULL,
                longitude DECIMAL(10, 7) NOT NULL,
                speed DECIMAL(5, 2) DEFAULT 0.00,
                heading DECIMAL(5, 2),
                altitude DECIMAL(8, 2),
                accuracy DECIMAL(5, 2),
                timestamp DATETIME NOT NULL,
                address VARCHAR(200),
                status VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建驾驶行为表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS driving_behaviors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                vehicle_id INTEGER,
                behavior_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) NOT NULL,
                latitude DECIMAL(10, 7),
                longitude DECIMAL(10, 7),
                speed_at_event DECIMAL(5, 2),
                timestamp DATETIME NOT NULL,
                description TEXT,
                processed BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建紧急警报表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER NOT NULL,
                vehicle_id INTEGER,
                alert_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) NOT NULL,
                latitude DECIMAL(10, 7),
                longitude DECIMAL(10, 7),
                description TEXT,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                responded_by INTEGER,
                response_time DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL,
                FOREIGN KEY (responded_by) REFERENCES users(id) ON DELETE SET NULL
            )
        ''')
        
        # 创建操作日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                operation_type VARCHAR(50) NOT NULL,
                table_name VARCHAR(50) NOT NULL,
                record_id INTEGER NOT NULL,
                old_data TEXT,
                new_data TEXT,
                ip_address VARCHAR(50),
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_user_created ON drivers(user_id, created_at DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_name ON drivers(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vehicles_plate_number ON vehicles(plate_number)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_schedules_date ON schedules(schedule_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_schedules_driver_date ON schedules(driver_id, schedule_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_certificates_driver_expiry ON driver_certificates(driver_id, expiry_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gps_records_vehicle_timestamp ON gps_records(vehicle_id, timestamp DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_driving_behaviors_driver_timestamp ON driving_behaviors(driver_id, timestamp DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emergency_alerts_status ON emergency_alerts(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation_logs_user_created ON operation_logs(user_id, created_at DESC)')
        
        # 插入测试数据
        print("正在插入测试数据...")
        
        # 插入测试用户
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active) VALUES 
            ('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin', 1),
            ('manager1', 'manager1@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'employee', 1),
            ('manager2', 'manager2@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'employee', 1)
        ''')
        
        # 插入测试司机
        cursor.execute('''
            INSERT INTO drivers (
                user_id, name, phone, id_card, license_number, license_type, 
                main_route, vehicle_type, experience_years, status, region_type,
                emergency_contact, emergency_phone
            ) VALUES 
            (1, '张三', '13800138001', '110101199001011234', 'A123456789', 'A1', '北京-上海', '厢式货车', 5, 'active', '国内', '李四', '13900139001'),
            (1, '王五', '13800138002', '110101198902022345', 'B987654321', 'B2', '广州-深圳', '平板货车', 8, 'active', '国内', '赵六', '13900139002'),
            (2, '李明', '13800138003', '110101198803033456', 'C555555555', 'C1', '成都-重庆', '冷藏车', 3, 'active', '国内', '王芳', '13900139003'),
            (2, '刘强', '13800138004', '110101198707044567', 'D777777777', 'A2', '西安-兰州', '集装箱车', 10, 'active', '国内', '陈静', '13900139004'),
            (3, '赵敏', '13800138005', '110101198606065678', 'E999999999', 'B1', '武汉-长沙', '普通货车', 6, 'active', '国内', '孙华', '13900139005')
        ''')
        
        # 插入测试车辆
        cursor.execute('''
            INSERT INTO vehicles (
                plate_number, vehicle_type, brand, model, year, color, 
                engine_number, vin_number, insurance_expiry, annual_inspection_date,
                maintenance_due_date, mileage, fuel_type, fuel_consumption, status
            ) VALUES 
            ('京A12345', '厢式货车', '东风', 'DFL5160XXYBX1', 2020, '蓝色', 'ABC123456', 'LGAH4C2N0K1234567', 
             '2024-12-31', '2024-12-31', '2024-11-30', 125000.50, '柴油', 15.5, 'active'),
            ('粤B67890', '平板货车', '解放', 'CA5160TPB40K2L2E5A84', 2019, '红色', 'DEF789012', 'LFNMVXSB8K1E23456', 
             '2024-11-30', '2024-11-30', '2024-10-31', 98000.75, '柴油', 18.2, 'active'),
            ('川C11111', '冷藏车', '福田', 'BJ5169XLC-F2', 2021, '白色', 'GHI345678', 'LVBV6PBB8LW123456', 
             '2025-01-31', '2025-01-31', '2024-12-31', 75000.25, '柴油', 20.8, 'active'),
            ('陕D22222', '集装箱车', '重汽', 'ZZ4257N3247C1H', 2018, '绿色', 'JKL901234', 'LZZ5CLNB9K1234567', 
             '2024-10-31', '2024-10-31', '2024-09-30', 185000.00, '柴油', 22.1, 'maintenance'),
            ('鄂E33333', '普通货车', '江淮', 'HFC5161CCYKR1ZT', 2022, '银色', 'MNO567890', 'LJ11R4EH2N1234567', 
             '2025-02-28', '2025-02-28', '2025-01-31', 45000.50, '柴油', 16.7, 'active')
        ''')
        
        # 插入测试证书
        cursor.execute('''
            INSERT INTO driver_certificates (
                driver_id, certificate_type, certificate_number, issue_date, expiry_date,
                issuing_authority, status
            ) VALUES 
            (1, '驾驶证', 'A123456789', '2019-01-15', '2025-01-15', '北京市公安局公安交通管理局', 'valid'),
            (1, '危险品运输证', 'DG20200101', '2020-03-01', '2024-12-01', '北京市交通委员会', 'expiring_soon'),
            (2, '驾驶证', 'B987654321', '2018-06-20', '2024-06-20', '广东省公安厅交通管理局', 'expired'),
            (3, '驾驶证', 'C555555555', '2021-08-10', '2027-08-10', '四川省公安厅交通管理局', 'valid'),
            (4, '驾驶证', 'D777777777', '2016-11-05', '2024-11-05', '陕西省公安厅交通管理局', 'expiring_soon'),
            (5, '驾驶证', 'E999999999', '2017-04-12', '2025-04-12', '湖北省公安厅交通管理局', 'valid')
        ''')
        
        # 插入测试排班
        today = datetime.now()
        for i in range(7):
            schedule_date = today + timedelta(days=i)
            cursor.execute('''
                INSERT INTO schedules (
                    driver_id, vehicle_id, schedule_date, start_time, end_time,
                    route, task_type, status, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                (i % 5) + 1,  # driver_id
                (i % 5) + 1,  # vehicle_id
                schedule_date,
                schedule_date.replace(hour=8, minute=0),
                schedule_date.replace(hour=18, minute=0),
                f"路线{i+1}",
                ['delivery', 'pickup', 'transport'][i % 3],
                'scheduled' if i > 0 else 'completed',
                f"测试排班{i+1}"
            ))
        
        # 插入测试GPS记录
        for i in range(20):
            timestamp = today - timedelta(hours=i)
            cursor.execute('''
                INSERT INTO gps_records (
                    vehicle_id, driver_id, latitude, longitude, speed, 
                    timestamp, address, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                (i % 5) + 1,  # vehicle_id
                (i % 5) + 1,  # driver_id
                39.9042 + (i * 0.001),  # latitude (北京附近)
                116.4074 + (i * 0.001),  # longitude (北京附近)
                60.0 + (i * 2),  # speed
                timestamp,
                f"位置{i+1}",
                ['normal', 'speeding', 'idle'][i % 3]
            ))
        
        # 插入测试驾驶行为
        cursor.execute('''
            INSERT INTO driving_behaviors (
                driver_id, vehicle_id, behavior_type, severity, latitude, longitude,
                speed_at_event, timestamp, description, processed
            ) VALUES 
            (1, 1, 'speeding', 'high', 39.9042, 116.4074, 120.5, ?, '超速行驶', 0),
            (2, 2, 'harsh_braking', 'medium', 39.9142, 116.4174, 80.0, ?, '急刹车', 1),
            (3, 3, 'sharp_turn', 'low', 39.9242, 116.4274, 45.2, ?, '急转弯', 0),
            (4, 4, 'speeding', 'high', 39.9342, 116.4374, 135.8, ?, '严重超速', 0),
            (5, 5, 'harsh_braking', 'medium', 39.9442, 116.4474, 75.3, ?, '紧急制动', 1)
        ''', (datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now()))
        
        # 插入测试紧急警报
        cursor.execute('''
            INSERT INTO emergency_alerts (
                driver_id, vehicle_id, alert_type, severity, latitude, longitude,
                description, status, created_at
            ) VALUES 
            (1, 1, 'accident', 'high', 39.9042, 116.4074, '车辆追尾事故', 'active', ?),
            (3, 3, 'medical', 'critical', 39.9242, 116.4274, '司机身体不适', 'responded', ?)
        ''', (datetime.now(), datetime.now()))
        
        conn.commit()
        print("数据库初始化成功！")
        
        # 显示统计信息
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM drivers')
        driver_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM vehicles')
        vehicle_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM schedules')
        schedule_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM driver_certificates')
        certificate_count = cursor.fetchone()[0]
        
        print(f"\n数据库统计信息:")
        print(f"用户数量: {user_count}")
        print(f"司机数量: {driver_count}")
        print(f"车辆数量: {vehicle_count}")
        print(f"排班数量: {schedule_count}")
        print(f"证书数量: {certificate_count}")
        
    except Exception as e:
        conn.rollback()
        print(f"数据库初始化失败: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()