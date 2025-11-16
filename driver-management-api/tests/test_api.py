import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.main import app
from app.core.database import get_db
from app.models import User, Driver
from app.core.security import get_password_hash, create_access_token


@pytest.fixture
async def async_client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_db():
    """Create test database session"""
    async for db in get_db():
        yield db
        break


@pytest.fixture
async def test_user(test_db: AsyncSession):
    """Create test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        role="employee",
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def admin_user(test_db: AsyncSession):
    """Create admin user"""
    user = User(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role="admin",
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def auth_headers(test_user: User):
    """Create authentication headers"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def admin_auth_headers(admin_user: User):
    """Create admin authentication headers"""
    token = create_access_token(data={"sub": str(admin_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def test_driver(test_db: AsyncSession, test_user: User):
    """Create test driver"""
    driver = Driver(
        user_id=test_user.id,
        name="Test Driver",
        phone="13800138000",
        id_card="110101199001011234",
        license_number="A123456789",
        license_type="A1",
        main_route="Beijing-Shanghai",
        vehicle_type="Box Truck",
        vehicle_length="9.6m",
        price_per_km=8.5,
        experience_years=10,
        status="active",
        emergency_contact="Test Contact",
        emergency_phone="13900139000",
        remark="Test driver for unit tests"
    )
    test_db.add(driver)
    await test_db.commit()
    await test_db.refresh(driver)
    return driver


class TestAuthAPI:
    """Test authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, test_user: User):
        """Test successful login"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, async_client: AsyncClient):
        """Test login with invalid credentials"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={"username": "invalid", "password": "wrong"}
        )
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, async_client: AsyncClient, auth_headers: dict, test_user: User):
        """Test get current user endpoint"""
        response = await async_client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["username"] == "testuser"
        assert data["user"]["id"] == test_user.id


class TestDriverAPI:
    """Test driver management endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_driver(self, async_client: AsyncClient, auth_headers: dict):
        """Test create driver"""
        driver_data = {
            "name": "New Driver",
            "phone": "13800138001",
            "id_card": "110101199001011235",
            "license_number": "B987654321",
            "license_type": "B2",
            "main_route": "Shanghai-Hangzhou",
            "vehicle_type": "Flatbed Truck",
            "vehicle_length": "6.8m",
            "price_per_km": 7.5,
            "experience_years": 8,
            "emergency_contact": "Contact Person",
            "emergency_phone": "13900139001",
            "remark": "New driver"
        }
        
        response = await async_client.post(
            "/api/v1/drivers",
            json=driver_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Driver"
        assert data["phone"] == "13800138001"
    
    @pytest.mark.asyncio
    async def test_get_driver_list(self, async_client: AsyncClient, auth_headers: dict, test_driver: Driver):
        """Test get driver list"""
        response = await async_client.get("/api/v1/drivers", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert data["total"] >= 1
        assert any(driver["id"] == test_driver.id for driver in data["data"])
    
    @pytest.mark.asyncio
    async def test_get_driver_detail(self, async_client: AsyncClient, auth_headers: dict, test_driver: Driver):
        """Test get driver detail"""
        response = await async_client.get(f"/api/v1/drivers/{test_driver.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_driver.id
        assert data["name"] == test_driver.name
    
    @pytest.mark.asyncio
    async def test_update_driver(self, async_client: AsyncClient, auth_headers: dict, test_driver: Driver):
        """Test update driver"""
        update_data = {"name": "Updated Driver Name", "price_per_km": 9.0}
        
        response = await async_client.put(
            f"/api/v1/drivers/{test_driver.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Driver Name"
        assert data["price_per_km"] == 9.0
    
    @pytest.mark.asyncio
    async def test_delete_driver(self, async_client: AsyncClient, auth_headers: dict, test_db: AsyncSession):
        """Test delete driver"""
        # Create a driver to delete
        driver = Driver(
            user_id=1,
            name="Driver to Delete",
            phone="13800138002",
            id_card="110101199001011236",
            license_number="C111222333",
            license_type="C1",
            main_route="Test Route",
            vehicle_type="Test Vehicle",
            price_per_km=6.0,
            experience_years=5,
            status="active"
        )
        test_db.add(driver)
        await test_db.commit()
        await test_db.refresh(driver)
        
        # Delete the driver
        response = await async_client.delete(
            f"/api/v1/drivers/{driver.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Verify deletion
        response = await async_client.get(f"/api/v1/drivers/{driver.id}", headers=auth_headers)
        assert response.status_code == 404


class TestStatisticsAPI:
    """Test statistics endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_statistics_admin_only(self, async_client: AsyncClient, admin_auth_headers: dict):
        """Test statistics endpoint requires admin role"""
        response = await async_client.get("/api/v1/statistics", headers=admin_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_drivers" in data
        assert "active_drivers" in data
        assert "new_drivers_this_month" in data
        assert "drivers_by_route" in data
        assert "drivers_by_user" in data
    
    @pytest.mark.asyncio
    async def test_get_statistics_non_admin(self, async_client: AsyncClient, auth_headers: dict):
        """Test statistics endpoint rejects non-admin users"""
        response = await async_client.get("/api/v1/statistics", headers=auth_headers)
        assert response.status_code == 403


class TestValidation:
    """Test input validation"""
    
    @pytest.mark.asyncio
    async def test_create_driver_invalid_phone(self, async_client: AsyncClient, auth_headers: dict):
        """Test phone number validation"""
        driver_data = {
            "name": "Invalid Phone Driver",
            "phone": "invalid_phone",
            "id_card": "110101199001011237",
            "license_number": "D444555666",
            "license_type": "D",
            "main_route": "Test Route",
            "vehicle_type": "Test Vehicle",
            "price_per_km": 5.0,
            "experience_years": 3
        }
        
        response = await async_client.post(
            "/api/v1/drivers",
            json=driver_data,
            headers=auth_headers
        )
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_create_driver_invalid_id_card(self, async_client: AsyncClient, auth_headers: dict):
        """Test ID card validation"""
        driver_data = {
            "name": "Invalid ID Card Driver",
            "phone": "13800138003",
            "id_card": "invalid_id_card",
            "license_number": "E777888999",
            "license_type": "E",
            "main_route": "Test Route",
            "vehicle_type": "Test Vehicle",
            "price_per_km": 5.0,
            "experience_years": 3
        }
        
        response = await async_client.post(
            "/api/v1/drivers",
            json=driver_data,
            headers=auth_headers
        )
        assert response.status_code == 422


class TestAuthentication:
    """Test authentication requirements"""
    
    @pytest.mark.asyncio
    async def test_driver_endpoints_require_auth(self, async_client: AsyncClient):
        """Test that driver endpoints require authentication"""
        response = await async_client.get("/api/v1/drivers")
        assert response.status_code == 401
        
        response = await async_client.post("/api/v1/drivers", json={})
        assert response.status_code == 401
        
        response = await async_client.get("/api/v1/drivers/1")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])