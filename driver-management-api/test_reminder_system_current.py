#!/usr/bin/env python3
"""
测试驾照有效期自动提醒功能 - 更新版本
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

async def create_test_data_with_current_dates():
    """创建带有当前日期的测试数据"""
    async with AsyncSessionLocal() as session:
        # 创建测试用户
        user_data = {
            "username": "test_driver_current",
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
            "name": "测试司机当前",
            "phone": "13800138001",
            "id_card": "110101199001011235",
            "license_number": "A123456780",
            "license_type": "A1",
            "main_route": "北京-上海",
            "vehicle_type": "货车",
            "vehicle_length": "17.5米",
            "price_per_km": 8.5,
            "experience_years": 5,
            "status": "active",
            "region_type": "国内",
            "emergency_contact": "紧急联系人",
            "emergency_phone": "13900139001",
            "remark": "测试司机当前日期"
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
        
        # 创建即将到期的证书 - 使用当前日期匹配提醒系统
        today = datetime.now().date()
        
        # 创建不同到期日期的证书来测试提醒系统
        test_dates = [
            today + timedelta(days=30),   # 30天后到期
            today + timedelta(days=15),   # 15天后到期  
            today + timedelta(days=7),    # 7天后到期
            today + timedelta(days=3),    # 3天后到期
            today + timedelta(days=1),    # 1天后到期
        ]
        
        certificates = []
        for i, expiry_date in enumerate(test_dates):
            cert_data = {
                "driver_id": driver.id,
                "certificate_type": f"测试证书类型{i+1}",
                "certificate_number": f"TESTCERT{i+1:03d}",
                "issue_date": today - timedelta(days=365),
                "expiry_date": expiry_date,
                "issuing_authority": "测试发证机构",
                "status": "valid"
            }
            
            # 检查证书是否已存在
            existing_cert = await session.execute(
                select(DriverCertificate).where(DriverCertificate.certificate_number == cert_data["certificate_number"])
            )
            existing_cert = existing_cert.scalar_one_or_none()
            
            if not existing_cert:
                cert = DriverCertificate(**cert_data)
                session.add(cert)
                await session.commit()
                await session.refresh(cert)
                certificates.append(cert)
                print(f"✓ 创建测试证书 {i+1}: {cert.certificate_type} (到期日期: {cert.expiry_date})")
            else:
                certificates.append(existing_cert)
                print(f"✓ 使用现有证书 {i+1}: {existing_cert.certificate_type} (到期日期: {existing_cert.expiry_date})")
        
        # 创建测试车辆
        vehicle_data = {
            "plate_number": "京A54321",
            "vehicle_type": "货车",
            "brand": "东风",
            "model": "天龙",
            "year": 2022,
            "color": "蓝色",
            "engine_number": "TEST123456",
            "vin_number": "TESTVIN123456789",
            "purchase_date": today - timedelta(days=365),
            "registration_date": today - timedelta(days=365),
            "insurance_expiry": today + timedelta(days=20),  # 20天后到期
            "annual_inspection_date": today + timedelta(days=25),  # 25天后到期
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
            "certificates": certificates,
            "vehicle": vehicle
        }

async def test_reminder_check_with_current_dates():
    """使用当前日期测试提醒检查功能"""
    print("\n" + "="*50)
    print("使用当前日期测试提醒检查功能")
    print("="*50)
    
    try:
        # 执行提醒检查
        reminders = await reminder_service.check_expiring_licenses()
        
        print(f"\n✓ 发现 {len(reminders)} 个即将到期的项目:")
        
        # 按类型分组显示
        cert_reminders = [r for r in reminders if r['type'] == 'certificate_expiry']
        insurance_reminders = [r for r in reminders if r['type'] == 'insurance_expiry']
        inspection_reminders = [r for r in reminders if r['type'] == 'inspection_expiry']
        
        if cert_reminders:
            print(f"\n📄 证书到期提醒 ({len(cert_reminders)} 个):")
            for reminder in cert_reminders:
                print(f"  - {reminder['certificate_type']}: {reminder['days_before']} 天后到期")
        
        if insurance_reminders:
            print(f"\n🚗 车辆保险到期提醒 ({len(insurance_reminders)} 个):")
            for reminder in insurance_reminders:
                print(f"  - 车牌 {reminder['vehicle_plate']}: {reminder['days_before']} 天后到期")
        
        if inspection_reminders:
            print(f"\n🔧 车辆年检到期提醒 ({len(inspection_reminders)} 个):")
            for reminder in inspection_reminders:
                print(f"  - 车牌 {reminder['vehicle_plate']}: {reminder['days_before']} 天后到期")
        
        return reminders
        
    except Exception as e:
        print(f"✗ 提醒检查失败: {e}")
        import traceback
        traceback.print_exc()
        return []

async def test_dashboard():
    """测试仪表板功能"""
    print("\n" + "="*50)
    print("测试提醒仪表板功能")
    print("="*50)
    
    try:
        # 模拟API调用获取仪表板数据
        from app.api.v1.reminders import get_reminder_dashboard
        from app.models import User
        
        # 创建一个模拟用户
        async with AsyncSessionLocal() as session:
            from app.crud import get_user_by_username
            user = await get_user_by_username(session, "test_driver_current")
            
            if user:
                # 调用仪表板函数
                result = await get_reminder_dashboard(30, user)
                
                print(f"\n✓ 仪表板数据获取成功:")
                data = result.get("data", {})
                print(f"  - 总计到期项目: {data.get('total_count', 0)}")
                print(f"  - 证书到期: {data.get('statistics', {}).get('certificate_expiry', 0)}")
                print(f"  - 保险到期: {data.get('statistics', {}).get('insurance_expiry', 0)}")
                print(f"  - 年检到期: {data.get('statistics', {}).get('inspection_expiry', 0)}")
                
                timeline = data.get('timeline', {})
                if timeline:
                    print(f"  - 时间线统计:")
                    for days, counts in sorted(timeline.items()):
                        total = sum(counts.values())
                        if total > 0:
                            print(f"    {days} 天后: {total} 个项目到期")
                
            else:
                print("⚠ 未找到测试用户")
                
    except Exception as e:
        print(f"✗ 仪表板测试失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主测试函数"""
    print("司机管理系统 - 驾照有效期自动提醒功能测试 (当前日期版本)")
    print("="*60)
    
    # 设置测试数据
    test_data = await create_test_data_with_current_dates()
    
    # 测试提醒检查
    reminders = await test_reminder_check_with_current_dates()
    
    # 测试仪表板
    await test_dashboard()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)

if __name__ == "__main__":
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 运行测试
    asyncio.run(main())