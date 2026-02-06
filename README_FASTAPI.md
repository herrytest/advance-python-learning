# FastAPI User Management Service

## Overview
This project now includes a FastAPI service for user management that runs alongside the Flask application.

## Architecture
- **Flask App** (port 5000): Handles UI rendering, gallery, dashboard, and stock features
- **FastAPI Service** (port 8000): Provides REST API for user CRUD operations

## Running the Applications

### Start Flask (Main App)
```bash
python app.py
```
Access at: http://localhost:5000

### Start FastAPI (User API)
```bash
# Option 1: Using the startup script
./start_fastapi.sh

# Option 2: Direct command
source venv/bin/activate
uvicorn fastapi_users:app --reload --port 8000
```
Access at: http://localhost:8000
API Docs: http://localhost:8000/docs

## FastAPI Endpoints

### User Management API
- `POST /api/users` - Create a new user
- `GET /api/users` - Get all users
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

## Features
- **Pydantic Validation**: Request/response validation with type checking
- **Email Validation**: Built-in email format validation
- **CORS Enabled**: Flask frontend can call FastAPI endpoints
- **Auto Documentation**: Interactive API docs at `/docs`
- **RESTful Design**: Proper HTTP methods and status codes

## Frontend Integration
The Users page (`/users`) now uses JavaScript fetch to call FastAPI endpoints instead of Flask form submissions. This provides:
- Real-time updates without page refresh
- Better error handling
- Modern async/await patterns
- Dynamic user list loading

## Database
Both Flask and FastAPI use the same `db.py` module, ensuring consistent database access across both applications.
