#!/bin/bash
echo "=========================================="
echo "    Running Regression Test Suite        "
echo "=========================================="
echo "Starting test execution..."
echo ""

# 1. Auth Tests
echo "[1/5] Running Authentication Tests..."
./venv/bin/python3 tests/test_auth.py
if [ $? -eq 0 ]; then
    echo "✅ Auth Tests Passed"
else
    echo "❌ Auth Tests Failed"
    exit 1
fi
echo ""

# 2. Flask User CRUD Tests
echo "[2/5] Running Flask User CRUD Tests..."
./venv/bin/python3 tests/test_users_flask.py
if [ $? -eq 0 ]; then
    echo "✅ Flask User CRUD Tests Passed"
else
    echo "❌ Flask User CRUD Tests Failed"
    exit 1
fi
echo ""

# 3. Upload & OCR Tests
echo "[3/5] Running Upload & OCR Tests..."
./venv/bin/python3 tests/test_upload_ocr.py
if [ $? -eq 0 ]; then
    echo "✅ Upload & OCR Tests Passed"
else
    echo "❌ Upload & OCR Tests Failed"
    exit 1
fi
echo ""

# 4. FastAPI Tests
echo "[4/5] Running FastAPI Tests..."
./venv/bin/python3 tests/test_api.py
if [ $? -eq 0 ]; then
    echo "✅ FastAPI Tests Passed"
else
    echo "❌ FastAPI Tests Failed"
    exit 1
fi
echo ""

# 5. Dashboard Stocks Tests
echo "[5/5] Running Dashboard Stocks Tests..."
./venv/bin/python3 tests/test_dashboard_stocks.py
if [ $? -eq 0 ]; then
    echo "✅ Dashboard Stocks Tests Passed"
else
    echo "❌ Dashboard Stocks Tests Failed"
    exit 1
fi
echo ""

echo "=========================================="
echo "    ALL TESTS PASSED SUCCESSFULLY!       "
echo "=========================================="
