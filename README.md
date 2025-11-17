# Driver Management System

A comprehensive full-stack driver management system built with Vue 3, Python FastAPI, and modern web technologies.

## 🚀 Features

### Core Functionality
- **User Authentication**: JWT-based authentication with role-based access control
- **Driver Management**: Complete CRUD operations for driver records
- **File Upload**: Support for driver photos (ID cards, licenses, vehicle photos)
- **Route Selection**: Tree-based country/province selector with search (China + Central Asia)
- **Statistics Dashboard**: Interactive data visualization with charts and analytics
- **Search & Filtering**: Advanced search capabilities for drivers
- **Responsive Design**: Mobile-friendly interface using HeroUI components

### Technical Features
- **Modern Frontend**: Vue 3 + TypeScript + Vite + Tailwind CSS
- **Robust Backend**: Python FastAPI with async support and automatic API documentation
- **Database**: PostgreSQL with SQLAlchemy ORM (SQLite for development)
- **Caching**: Redis for session management and performance optimization
- **Security**: Bcrypt password hashing, JWT tokens, CSRF protection
- **File Storage**: Local file system with configurable storage options
- **Docker Support**: Containerized deployment with Docker Compose

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Testing](#testing)
- [Architecture](#architecture)
- [Contributing](#contributing)

## 🛠 Installation

### Prerequisites
- Node.js 20+ and pnpm/npm
- Python 3.11+ with pip
- PostgreSQL 14+ (or SQLite for development)
- Redis 7+ (optional, for caching)

### Clone Repository
```bash
git clone <repository-url>
cd driver-management-system
```

### Backend Setup
```bash
cd driver-management-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db_sqlite.py  # For development with SQLite

# Start backend server
uvicorn main:app --reload --port 8001
```

### Frontend Setup
```bash
cd driver-management-vue

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

## 🚀 Quick Start

1. **Start Backend**: Navigate to `driver-management-api` and run `uvicorn main:app --reload`
2. **Start Frontend**: Navigate to `driver-management-vue` and run `pnpm dev`
3. **Access Application**: Open http://localhost:3000 in your browser
4. **Login**: Use default admin credentials (username: `admin`, password: `admin123`)

## 📖 Development

### Project Structure
```
driver-management-system/
├── driver-management-api/          # Backend API
│   ├── app/
│   │   ├── api/v1/                # API endpoints
│   │   ├── core/                  # Core functionality (auth, database, config)
│   │   ├── models/                # Database models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── crud/                  # CRUD operations
│   │   └── utils/                 # Utility functions
│   ├── tests/                     # Backend tests
│   ├── uploads/                   # File uploads directory
│   └── requirements.txt           # Python dependencies
├── driver-management-vue/          # Frontend application
│   ├── src/
│   │   ├── api/                   # API client functions
│   │   ├── components/            # Vue components
│   │   ├── stores/                # Pinia state management
│   │   ├── views/                 # Page components
│   │   ├── layouts/               # Layout components
│   │   ├── router/                # Vue Router configuration
│   │   └── utils/                 # Utility functions
│   ├── public/                    # Static assets
│   └── package.json               # Node.js dependencies
├── docker-compose.yml             # Docker orchestration
├── DEPLOYMENT.md                  # Deployment guide
└── API_DOCUMENTATION.md          # API documentation
```

### Backend Development
The backend is built with FastAPI and includes:
- **Automatic API Documentation**: Available at http://localhost:8001/docs
- **Async Support**: Full async/await support for better performance
- **Type Safety**: Full type hints with Pydantic validation
- **Database Migrations**: SQLAlchemy Alembic for schema management

Key files:
- `main.py`: Application entry point
- `app/api/v1/`: API route definitions
- `app/models/`: SQLAlchemy database models
- `app/schemas/`: Pydantic validation schemas

### Frontend Development
The frontend uses Vue 3 with modern tooling:
- **Composition API**: Modern Vue 3 Composition API
- **TypeScript**: Full TypeScript support for type safety
- **HeroUI**: Modern component library for consistent UI
- **Pinia**: State management for Vue 3
- **Vue Router**: Client-side routing with navigation guards

Key files:
- `src/main.ts`: Application entry point
- `src/views/`: Page components
- `src/stores/`: Pinia state management
- `src/api/`: API client functions

## 📚 API Documentation

Interactive API documentation is available at:
- Development: http://localhost:8001/docs
- Production: https://your-domain.com/api/docs

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## 🐳 Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Manual Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Production environment setup
- SSL/TLS configuration
- Database migration
- Monitoring and logging
- Security hardening

## 🧪 Testing

### Backend Tests
```bash
cd driver-management-api

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

### Frontend Tests
```bash
cd driver-management-vue

# Run type checking
pnpm type-check

# Run linting
pnpm lint

# Run all checks
pnpm check
```

### API Testing
Test the API endpoints using the provided test script:
```bash
# Test authentication
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Test driver list (requires token)
curl -X GET "http://localhost:8001/api/v1/drivers" \
  -H "Authorization: Bearer <your-token>"
```

## 🏗 Architecture

### Technology Stack
**Frontend:**
- Vue 3.5+ with Composition API
- TypeScript for type safety
- Vite for build tooling
- HeroUI for component library
- Pinia for state management
- Vue Router for routing
- Axios for HTTP requests
- Tailwind CSS for styling

**Backend:**
- Python 3.11+ with FastAPI
- SQLAlchemy for database ORM
- Pydantic for data validation
- JWT for authentication
- Bcrypt for password hashing
- Async support throughout

**Database & Storage:**
- PostgreSQL 14+ (SQLite for development)
- Redis for caching and sessions
- Local file system for uploads

**Development Tools:**
- Docker for containerization
- ESLint and Prettier for code quality
- TypeScript for type checking
- Pytest for backend testing

### Security Features
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Input validation and sanitization
- CORS configuration
- Rate limiting
- File upload validation
- SQL injection prevention

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code style
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [API Documentation](API_DOCUMENTATION.md)
- Review the [Deployment Guide](DEPLOYMENT.md)
- Open an issue in the repository
- Contact the development team

## 📈 Changelog

### v1.0.0 (Current)
- Initial release with core functionality
- User authentication and authorization
- Complete driver management system
- File upload functionality
- Statistics dashboard with charts
- Docker containerization
- Comprehensive API documentation

---

**Built with ❤️ using modern web technologies**
### UI Updates
- 移除司机详情页底部的编辑/删除按钮，统一通过页面顶部操作入口进行管理
- 新增司机与编辑司机页面的“主要线路”支持使用 Ant Design TreeSelect 进行国家-省份两级选择，并支持省份模糊搜索
- 统一创建与编辑页面的保存/取消按钮尺寸、类型、布局与禁用状态，保持一致的交互体验