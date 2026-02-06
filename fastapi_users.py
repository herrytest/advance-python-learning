from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from db import (create_user, get_all_users, get_user_by_id, 
                update_user, delete_user)

app = FastAPI(title="User Management API", version="1.0.0")

# Enable CORS to allow Flask frontend to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    password: str

# API Endpoints

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "User Management API", "version": "1.0.0"}

# ===== TEST API ENDPOINTS =====

@app.get("/api/test/hello")
def test_hello():
    """Simple hello world test endpoint"""
    return {
        "message": "Hello from FastAPI!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test/echo/{text}")
def test_echo(text: str):
    """Echo back the text you send"""
    return {
        "original": text,
        "reversed": text[::-1],
        "uppercase": text.upper(),
        "lowercase": text.lower(),
        "length": len(text)
    }

@app.post("/api/test/calculate")
def test_calculate(num1: float, num2: float, operation: str = "add"):
    """Simple calculator API"""
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else "Cannot divide by zero"
    }
    
    if operation not in operations:
        raise HTTPException(status_code=400, detail="Invalid operation. Use: add, subtract, multiply, divide")
    
    return {
        "num1": num1,
        "num2": num2,
        "operation": operation,
        "result": operations[operation]
    }

@app.get("/api/test/status")
def test_status():
    """Check API and database status"""
    try:
        from db import get_db_connection
        conn = get_db_connection()
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "api_status": "running",
        "database_status": db_status,
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "users": "/api/users",
            "test_hello": "/api/test/hello",
            "test_echo": "/api/test/echo/{text}",
            "test_calculate": "/api/test/calculate",
            "test_status": "/api/test/status"
        }
    }

# ===== USER MANAGEMENT ENDPOINTS =====


@app.post("/api/users", response_model=dict, status_code=201)
def create_user_endpoint(user: UserCreate):
    """Create a new user"""
    created_at = datetime.now()
    updated_at = datetime.now()
    user_id = create_user(user.name, user.email, user.password,created_at,updated_at)
    if user_id:
        return {"success": True, "id": user_id, "message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Name or Email already exists")

@app.get("/api/users", response_model=List[UserResponse])
def get_users_endpoint():
    """Get all users"""
    users = get_all_users()
    return users

@app.get("/api/users/{user_id}", response_model=UserDetailResponse)
def get_user_endpoint(user_id: int):
    """Get user by ID"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}", response_model=dict)
def update_user_endpoint(user_id: int, user: UserUpdate):
    """Update user"""
    updated_at = datetime.now()
    success = update_user(user_id, user.name, user.email, user.password, updated_at)
    if success:
        return {"success": True, "message": "User updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Name or Email already exists or user not found")

@app.delete("/api/users/{user_id}", response_model=dict)
def delete_user_endpoint(user_id: int):
    """Delete user"""
    success = delete_user(user_id)
    if success:
        return {"success": True, "message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
