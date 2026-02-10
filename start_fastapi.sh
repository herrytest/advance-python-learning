#!/bin/bash

# Start FastAPI User Management Service
# This script runs the FastAPI application on port 8000

echo "Starting FastAPI User Management Service on port 8000..."
echo "API Documentation will be available at: http://localhost:8000/docs"
echo ""

./venv/bin/uvicorn fastapi_users:app --reload --port 8000
