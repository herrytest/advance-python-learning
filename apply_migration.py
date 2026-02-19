import pymysql
import os

# Database configuration (matching django_settings.py)
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'laravel',
    'password': 'password',
    'database': 'laravel',
    'port': 3306,
}

def apply_migration():
    """Apply the init_db.sql migration to the MySQL database."""
    sql_file = 'init_db.sql'
    
    if not os.path.exists(sql_file):
        print(f"Error: {sql_file} not found.")
        return

    print(f"Connecting to database '{DB_CONFIG['database']}' on {DB_CONFIG['host']}...")
    
    try:
        # Connect to the database
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port'],
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
        )
        
        with connection.cursor() as cursor:
            # Read the SQL file
            with open(sql_file, 'r') as f:
                sql_script = f.read()
            
            print(f"Executing {sql_file}...")
            # Execute the multi-statement SQL script
            cursor.execute(sql_script)
            
        # Commit the changes
        connection.commit()
        print("Migration applied successfully!")
        
    except pymysql.MySQLError as e:
        print(f"Error during migration: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    apply_migration()
