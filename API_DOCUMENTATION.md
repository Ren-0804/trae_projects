# Driver Management System - API Documentation

## Base URL
- Development: `http://localhost:8000/api`
- Production: `https://your-domain.com/api`

## Authentication
All API endpoints (except login) require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Response Format
All responses follow this structure:
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": 1699123456
}
```

## Error Codes
| Code | Description |
|------|-------------|
| 0 | Success |
| 40001 | Invalid parameters |
| 40101 | Unauthorized |
| 40301 | Forbidden |
| 40401 | Not found |
| 50001 | Internal server error |
| 50002 | Database error |

---

## Authentication Endpoints

### POST /auth/login
User login endpoint.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2025-11-16T11:58:20",
    "last_login_at": "2025-11-16T12:29:35.594318"
  }
}
```

### GET /auth/me
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true,
      "created_at": "2025-11-16T11:58:20",
      "last_login_at": "2025-11-16T12:29:35.594318"
    }
  },
  "timestamp": 1699123456
}
```

---

## Driver Management Endpoints

### GET /drivers
Get paginated list of drivers with optional filtering.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| page_size | integer | No | Items per page (default: 20, max: 100) |
| keyword | string | No | Search keyword (searches name, phone, id_card) |
| route | string | No | Filter by main route |
| status | string | No | Filter by status (active/inactive/blocked) |
| user_id | integer | No | Filter by assigned user (admin only) |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "data": [
      {
        "id": 1,
        "user_id": 1,
        "name": "张三",
        "phone": "13800138000",
        "id_card": "110101199001011234",
        "license_number": "A123456789",
        "license_type": "A1",
        "main_route": "北京-上海",
        "vehicle_type": "厢式货车",
        "vehicle_length": "9.6米",
        "price_per_km": 8.5,
        "experience_years": 10,
        "status": "active",
        "emergency_contact": "张妻",
        "emergency_phone": "13800138001",
        "remark": "经验丰富，安全可靠",
        "created_at": "2025-11-16T12:30:00",
        "updated_at": "2025-11-16T12:30:00",
        "user": {
          "id": 1,
          "username": "admin",
          "email": "admin@example.com",
          "role": "admin"
        }
      }
    ],
    "total": 25,
    "page": 1,
    "page_size": 20
  },
  "timestamp": 1699123456
}
```

### POST /drivers
Create a new driver.

**Request Body:**
```json
{
  "name": "李四",
  "phone": "13900139001",
  "id_card": "110101198503022345",
  "license_number": "B987654321",
  "license_type": "B2",
  "main_route": "广州-深圳",
  "vehicle_type": "平板货车",
  "vehicle_length": "6.8米",
  "price_per_km": 6.0,
  "experience_years": 8,
  "emergency_contact": "李妻",
  "emergency_phone": "13900139002",
  "remark": "熟悉珠三角路线"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 2,
    "user_id": 1,
    "name": "李四",
    "phone": "13900139001",
    "id_card": "110101198503022345",
    "license_number": "B987654321",
    "license_type": "B2",
    "main_route": "广州-深圳",
    "vehicle_type": "平板货车",
    "vehicle_length": "6.8米",
    "price_per_km": 6.0,
    "experience_years": 8,
    "status": "active",
    "emergency_contact": "李妻",
    "emergency_phone": "13900139002",
    "remark": "熟悉珠三角路线",
    "created_at": "2025-11-16T13:00:00",
    "updated_at": "2025-11-16T13:00:00"
  },
  "timestamp": 1699123456
}
```

### GET /drivers/{id}
Get detailed information about a specific driver.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Driver ID |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "name": "张三",
    "phone": "13800138000",
    "id_card": "110101199001011234",
    "license_number": "A123456789",
    "license_type": "A1",
    "main_route": "北京-上海",
    "vehicle_type": "厢式货车",
    "vehicle_length": "9.6米",
    "price_per_km": 8.5,
    "experience_years": 10,
    "status": "active",
    "emergency_contact": "张妻",
    "emergency_phone": "13800138001",
    "remark": "经验丰富，安全可靠",
    "created_at": "2025-11-16T12:30:00",
    "updated_at": "2025-11-16T12:30:00",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin"
    }
  },
  "timestamp": 1699123456
}
```

### PUT /drivers/{id}
Update an existing driver.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Driver ID |

**Request Body:** (All fields optional)
```json
{
  "name": "张三 Updated",
  "price_per_km": 9.0,
  "status": "inactive"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "name": "张三 Updated",
    "phone": "13800138000",
    "id_card": "110101199001011234",
    "license_number": "A123456789",
    "license_type": "A1",
    "main_route": "北京-上海",
    "vehicle_type": "厢式货车",
    "vehicle_length": "9.6米",
    "price_per_km": 9.0,
    "experience_years": 10,
    "status": "inactive",
    "emergency_contact": "张妻",
    "emergency_phone": "13800138001",
    "remark": "经验丰富，安全可靠",
    "created_at": "2025-11-16T12:30:00",
    "updated_at": "2025-11-16T14:00:00"
  },
  "timestamp": 1699123456
}
```

### DELETE /drivers/{id}
Delete a driver.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Driver ID |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": null,
  "timestamp": 1699123456
}
```

---

## File Upload Endpoints

### POST /drivers/{id}/photos
Upload driver photos (ID card, license, vehicle photos).

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Driver ID |

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| photo_type | string | Yes | Type of photo: `id_card_front`, `id_card_back`, `license`, `vehicle` |
| file | file | Yes | Image file (JPG, PNG, max 10MB) |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "driver_id": 1,
    "photo_type": "id_card_front",
    "file_path": "uploads/driver_photos/1_id_card_front_20251116_123456.jpg",
    "file_name": "1_id_card_front_20251116_123456.jpg",
    "file_size": 102400,
    "mime_type": "image/jpeg",
    "created_at": "2025-11-16T12:30:00"
  },
  "timestamp": 1699123456
}
```

### GET /drivers/{id}/photos
Get all photos for a driver.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Driver ID |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "id": 1,
      "driver_id": 1,
      "photo_type": "id_card_front",
      "file_path": "uploads/driver_photos/1_id_card_front_20251116_123456.jpg",
      "file_name": "1_id_card_front_20251116_123456.jpg",
      "file_size": 102400,
      "mime_type": "image/jpeg",
      "created_at": "2025-11-16T12:30:00"
    }
  ],
  "timestamp": 1699123456
}
```

### GET /drivers/photos/{photo_id}
Download a specific photo.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| photo_id | integer | Yes | Photo ID |

**Response:** Binary image file

---

## Statistics Endpoints

### GET /statistics
Get system statistics (admin only).

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total_drivers": 25,
    "active_drivers": 20,
    "new_drivers_this_month": 5,
    "drivers_by_route": [
      {
        "route": "北京-上海",
        "count": 8
      },
      {
        "route": "广州-深圳",
        "count": 6
      },
      {
        "route": "成都-重庆",
        "count": 4
      }
    ],
    "drivers_by_user": [
      {
        "user_id": 1,
        "username": "admin",
        "count": 15
      },
      {
        "user_id": 2,
        "username": "employee1",
        "count": 10
      }
    ]
  },
  "timestamp": 1699123456
}
```

---

## User Management Endpoints (Admin Only)

### GET /users
Get list of users (admin only).

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| page_size | integer | No | Items per page (default: 20) |
| role | string | No | Filter by role (admin/employee) |
| is_active | boolean | No | Filter by active status |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "data": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "is_active": true,
        "last_login_at": "2025-11-16T12:29:35.594318",
        "created_at": "2025-11-16T11:58:20",
        "updated_at": "2025-11-16T12:29:35.594318"
      }
    ],
    "total": 3,
    "page": 1,
    "page_size": 20
  },
  "timestamp": 1699123456
}
```

### POST /users
Create a new user (admin only).

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "newpass123",
  "role": "employee"
}
```

### PUT /users/{id}
Update user information (admin only).

**Request Body:**
```json
{
  "email": "updated@example.com",
  "role": "admin",
  "is_active": true
}
```

### DELETE /users/{id}
Delete a user (admin only).

---

## Validation Rules

### Phone Number
- Must be 11 digits
- Must start with 1 followed by 3-9
- Pattern: `^1[3-9]\d{9}$`

### ID Card
- Must be 18 characters
- First 17 digits, last character can be digit or X/x
- Pattern: `^\d{17}[\dXx]$`

### License Number
- Minimum 5 characters, maximum 20 characters
- Alphanumeric characters allowed

### License Type
- Must be one of: A1, A2, B1, B2, C1, C2

### Status
- Must be one of: active, inactive, blocked

### Price per KM
- Must be non-negative decimal number
- Maximum 2 decimal places

### Experience Years
- Must be non-negative integer

---

## Rate Limiting
- Login attempts: 5 per minute per IP
- General API requests: 100 per minute per user
- File uploads: 10 per minute per user

---

## File Upload Specifications
- **Allowed formats**: JPG, JPEG, PNG, GIF, PDF
- **Maximum file size**: 10MB
- **Recommended dimensions**: 1024x768 pixels or higher
- **File naming**: Automatically generated with timestamp

---

## Error Handling
All errors follow a consistent format:
```json
{
  "code": 40001,
  "message": "Validation error",
  "data": {
    "detail": [
      {
        "loc": ["body", "phone"],
        "msg": "Invalid phone number format",
        "type": "value_error"
      }
    ]
  },
  "timestamp": 1699123456
}
```

## Testing
Test the API using the interactive documentation:
- Development: http://localhost:8001/docs
- Production: https://your-domain.com/api/docs

## Support
For API support and questions, please contact the development team.
## Region Information Endpoints

### GET /regions/china/meta
Fetch cached China GeoJSON meta information.

### GET /regions/china/provinces
List provinces. Query params: `q` for fuzzy search by name/code.

### GET /regions/china/cities
List cities for a province. Query params: `province_code` (required), `q` for fuzzy search.

### GET /regions/china/search
Search provinces by `name`, `code`, optional `lat`, `lon`.

### GET /regions/central-asia/countries
List five Central Asia countries with divisions and major cities. Query param `q` for fuzzy search by country or city.

## Driver Region Type Endpoints

### GET /drivers/{id}/region-type
Get region type for a driver.

### PUT /drivers/{id}/region-type
Update region type. Body: `{ "region_type": "国内" | "国外" }`