#!/usr/bin/env python3
"""
测试驾照有效期自动提醒功能
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models import Driver, DriverCertificate, Vehicle, User
from app.services.reminder_service import reminder_service
from app.crud import create_user

async def create_test_data():
    """创建测试数据"""
    async with AsyncSessionLocal() as session:
        # 创建测试用户
        user_data = {
            "username": "test_driver",
            "email": "test@example.com",
            "password": "test123",
            "role": "employee"
        }
        
        try:
            user = await create_user(session, user_data["username"], user_data["email"], user_data["password"], user_data["role"])
            print(f"✓ 创建测试用户: {user.username}")
        except Exception as e:
            print(f"⚠ 用户可能已存在: {e}")
            # 获取已存在的用户
            from app.crud import get_user_by_username
            user = await get_user_by_username(session, user_data["username"])
        
        # 创建测试司机
        driver_data = {
            "user_id": user.id,
            "name": "测试司机",
            "phone": "13800138000",
            "id_card": "110101199001011234",
            "license_number": "A123456789",
            "license_type": "A1",
            "main_route": "北京-上海",
            "vehicle_type": "货车",
            "vehicle_length": "17.5米",
            "price_per_km": 8.5,
            "experience_years": 5,
            "status": "active",
            "region_type": "国内",
            "emergency_contact": "紧急联系人",
            "emergency_phone": "13900139000",
            "remark": "测试司机"
        }
        
        # 检查司机是否已存在
        from sqlalchemy import select
        existing_driver = await session.execute(select(Driver).where(Driver.phone == driver_data["phone"]))
        existing_driver = existing_driver.scalar_one_or_none()
        
        if not existing_driver:
            driver = Driver(**driver_data)
            session.add(driver)
            await session.commit()
            await session.refresh(driver)
            print(f"✓ 创建测试司机: {driver.name}")
        else:
            driver = existing_driver
            print(f"✓ 使用现有司机: {driver.name}")
        
        # 创建即将到期的证书
        future_date = datetime.now().date() + timedelta(days=15)  # 15天后到期
        
        certificate_data = {
            "driver_id": driver.id,
            "certificate_type": "危险品运输证",
            "certificate_number": "DG2023001",
            "issue_date": datetime.now().date() - timedelta(days=365),  # 一年前发放
            "expiry_date": future_date,
            "issuing_authority": "交通管理局",
            "status": "valid"
        }
        
        # 检查证书是否已存在
        existing_cert = await session.execute(
            select(DriverCertificate).where(
                DriverCertificate.certificate_number == certificate_data["certificate_number"]
            )
        )
        existing_cert = existing_cert.scalar_one_or_none()
        
        if not existing_cert:
            cert = DriverCertificate(**certificate_data)
            session.add(cert)
            await session.commit()
            await session.refresh(cert)
            print(f"✓ 创建测试证书: {cert.certificate_type} (到期日期: {cert.expiry_date})")
        else:
            cert = existing_cert
            print(f"✓ 使用现有证书: {cert.certificate_type} (到期日期: {cert.expiry_date})")
        
        # 创建测试车辆
        vehicle_data = {
            "plate_number": "京A12345",
            "vehicle_type": "货车",
            "brand": "东风",
            "model": "天龙",
            "year": 2022,
            "color": "红色",
            "engine_number": "ABC123456",
            "vin_number": "LVSHCFAL8NS123456",
            "purchase_date": datetime.now().date() - timedelta(days=365),
            "registration_date": datetime.now().date() - timedelta(days=365),
            "insurance_expiry": datetime.now().date() + timedelta(days=20),  # 20天后到期
            "annual_inspection_date": datetime.now().date() + timedelta(days=25),  # 25天后到期
            "mileage": 50000.0,
            "fuel_type": "柴油",
            "fuel_consumption": 25.0,
            "status": "active",
            "current_driver_id": driver.id
        }
        
        # 检查车辆是否已存在
        existing_vehicle = await session.execute(select(Vehicle).where(Vehicle.plate_number == vehicle_data["plate_number"]))
        existing_vehicle = existing_vehicle.scalar_one_or_none()
        
        if not existing_vehicle:
            vehicle = Vehicle(**vehicle_data)
            session.add(vehicle)
            await session.commit()
            await session.refresh(vehicle)
            print(f"✓ 创建测试车辆: {vehicle.plate_number}")
            print(f"  - 保险到期: {vehicle.insurance_expiry}")
            print(f"  - 年检到期: {vehicle.annual_inspection_date}")
        else:
            vehicle = existing_vehicle
            print(f"✓ 使用现有车辆: {vehicle.plate_number}")
        
        return {
            "user": user,
            "driver": driver,
            "certificate": cert,
            "vehicle": vehicle
        }

async def test_reminder_check():
    """测试提醒检查功能"""
    print("\n" + "="*50)
    print("测试提醒检查功能")
    print("="*50)
    
    try:
        # 执行提醒检查
        reminders = await reminder_service.check_expiring_licenses()
        
        print(f"\n✓ 发现 {len(reminders)} 个即将到期的项目:")
        
        for reminder in reminders:
            print(f"\n  类型: {reminder['type']}")
            print(f"  提前天数: {reminder['days_before']} 天")
            
            if reminder['type'] == 'certificate_expiry':
                print(f"  司机: {reminder['driver_name']}")
                print(f"  证书类型: {reminder['certificate_type']}")
                print(f"  证书编号: {reminder['certificate_number']}")
            elif reminder['type'] in ['insurance_expiry', 'inspection_expiry']:
                print(f"  车牌号: {reminder['vehicle_plate']}")
                print(f"  司机: {reminder['driver_name']}")
            
            print(f"  到期日期: {reminder['expiry_date']}")
            print(f"  用户邮箱: {reminder.get('user_email', '无')}")
        
        return reminders
        
    except Exception as e:
        print(f"✗ 提醒检查失败: {e}")
        return []

async def test_send_reminders(reminders):
    """测试发送提醒功能"""
    print("\n" + "="*50)
    print("测试发送提醒功能")
    print("="*50)
    
    if not reminders:
        print("⚠ 没有提醒需要发送")
        return
    
    try:
        # 发送提醒
        results = await reminder_service.send_reminders(reminders)
        
        print(f"\n✓ 提醒发送结果:")
        print(f"  总计: {results['total']}")
        print(f"  成功: {results['sent']}")
        print(f"  失败: {results['failed']}")
        
        for detail in results.get('details', []):
            print(f"  - {detail.get('email', '未知')}: {detail.get('status', 'unknown')}")
            if 'error' in detail:
                print(f"    错误: {detail['error']}")
        
    except Exception as e:
        print(f"✗ 发送提醒失败: {e}")

async def test_daily_check():
    """测试每日检查功能"""
    print("\n" + "="*50)
    print("测试每日检查功能")
    print("="*50)
    
    try:
        result = await reminder_service.run_daily_check()
        print(f"\n✓ 每日检查完成:")
        print(f"  结果: {result}")
        
    except Exception as e:
        print(f"✗ 每日检查失败: {e}")

async def main():
    """主测试函数"""
    print("司机管理系统 - 驾照有效期自动提醒功能测试")
    print("="*60)
    
    # 设置测试数据
    test_data = await create_test_data()
    
    # 测试提醒检查
    reminders = await test_reminder_check()
    
    # 测试发送提醒
    await test_send_reminders(reminders)
    
    # 测试每日检查
    await test_daily_check()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)

if __name__ == "__main__":
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 运行测试
    asyncio.run(main())