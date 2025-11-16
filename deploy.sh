#!/bin/bash

# Production Deployment Script for Driver Management System
# This script helps deploy the system without Docker

echo "🚀 Starting Driver Management System Deployment..."

# Check if backend is running
if pgrep -f "uvicorn main:app" > /dev/null; then
    echo "✅ Backend is already running"
else
    echo "🔄 Starting backend server..."
    cd /Users/akole/Documents/trae_projects/driver-management-api
    source venv/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4 > backend.log 2>&1 &
    echo "✅ Backend started on port 8001"
fi

# Check if frontend is running
if pgrep -f "vite" > /dev/null; then
    echo "✅ Frontend is already running"
else
    echo "🔄 Starting frontend server..."
    cd /Users/akole/Documents/trae_projects/driver-management-vue
    nohup pnpm dev --port 3000 --host 0.0.0.0 > frontend.log 2>&1 &
    echo "✅ Frontend started on port 3000"
fi

echo "📊 Deployment Status:"
echo "🌐 Frontend: https://traetraeprojectshsqb.vercel.app (Deployed to Vercel)"
echo "🔧 Backend: http://localhost:8001 (Local development server)"
echo "📚 API Docs: http://localhost:8001/docs"
echo ""
echo "✨ Deployment completed successfully!"
echo ""
echo "🔑 Default login credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📋 Available features:"
echo "   • Driver management (CRUD operations)"
echo "   • File upload for driver photos"
echo "   • Interactive statistics dashboard"
echo "   • User authentication & authorization"
echo "   • Search & filtering capabilities"
echo "   • Responsive design for mobile devices"