# Driver Management System - Deployment Guide

## Overview
This guide provides instructions for deploying the Driver Management System using Docker containers.

## Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ available RAM
- 10GB+ available disk space

## Architecture
The system consists of:
- **Frontend**: Vue 3 + TypeScript + Vite (Port 3000)
- **Backend**: Python FastAPI + SQLAlchemy (Port 8001)
- **Database**: PostgreSQL 14 (Port 5432)
- **Cache**: Redis 7 (Port 6379)

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd driver-management-system

# Copy environment configuration
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

### 2. Build and Start Services
```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Initialize Database
```bash
# Run database migrations (if using Alembic)
docker-compose exec backend alembic upgrade head

# Or run the initialization script
docker-compose exec backend python init_db.py
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

## Configuration

### Environment Variables
Key environment variables in `.env`:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key (change in production!)
- `CORS_ORIGINS`: Allowed frontend origins

### Database Configuration
The PostgreSQL database is automatically initialized with:
- Database: `driver_management`
- User: `postgres`
- Password: `postgres123` (change in production!)

### File Storage
Uploaded files are stored in:
- Development: `./driver-management-api/uploads/`
- Production: Docker volume mounted at `/app/uploads/`

## Production Deployment

### 1. Security Hardening
```bash
# Generate secure secrets
openssl rand -hex 32  # For JWT_SECRET_KEY
openssl rand -hex 32  # For CSRF_SECRET_KEY

# Update .env with production values
nano .env
```

### 2. SSL/TLS Configuration
For production, use a reverse proxy like Nginx with SSL:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://backend:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Backup Strategy
```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres driver_management > backup.sql

# File backup
tar -czf uploads_backup.tar.gz driver-management-api/uploads/
```

### 4. Monitoring
```bash
# View logs
docker-compose logs -f

# Monitor resource usage
docker stats

# Health checks
curl -f http://localhost:8001/health || exit 1
```

## Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Migration
```bash
# Backup first
docker-compose exec postgres pg_dump -U postgres driver_management > pre_migration_backup.sql

# Run migrations
docker-compose exec backend alembic upgrade head
```

### Log Management
```bash
# View logs by service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Clear old logs
docker-compose logs --tail 100 > logs_backup.txt
docker-compose down && docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep -E ':(3000|8001|5432|6379)'
   
   # Modify ports in docker-compose.yml if needed
   ```

2. **Database Connection Issues**
   ```bash
   # Check database logs
   docker-compose logs postgres
   
   # Test connection
   docker-compose exec backend python -c "
   import asyncio
   from app.core.database import get_db
   async def test():
       async for db in get_db():
           print('Database connected successfully')
   asyncio.run(test())
   "
   ```

3. **Frontend Build Issues**
   ```bash
   # Clear node_modules and rebuild
   docker-compose exec frontend rm -rf node_modules
   docker-compose build frontend
   docker-compose up -d frontend
   ```

### Performance Optimization

1. **Database Optimization**
   - Add appropriate indexes
   - Configure connection pooling
   - Monitor query performance

2. **Caching Strategy**
   - Redis for session storage
   - Database query caching
   - Static asset caching

3. **Resource Limits**
   ```yaml
   # Add to docker-compose.yml services
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 2G
       reservations:
         cpus: '1.0'
         memory: 1G
   ```

## Support
For issues and questions:
- Check application logs: `docker-compose logs`
- Review API documentation: http://localhost:8001/docs
- Check system resources: `docker system df`

## Security Notes
- Change all default passwords in production
- Use environment variables for sensitive data
- Enable firewall rules for required ports only
- Regular security updates for base images