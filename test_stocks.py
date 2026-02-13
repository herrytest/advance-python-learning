from app import fetch_stock_data
import sys

print("Testing fetch_stock_data...")
try:
    stocks = fetch_stock_data()
    print(f"Result: {stocks}")
    if not stocks:
        print("FAIL: No stocks returned")
        sys.exit(1)
    
    for s in stocks:
        print(f"Stock: {s['name']}, Price: {s['price']}")
        if s['price'] == 'N/A':
            print(f"WARNING: Price is N/A for {s['name']}")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
