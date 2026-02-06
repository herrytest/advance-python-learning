import mysql.connector

# Database Configuration
DB_CONFIG = {
    'user': 'laravel',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'laravel',
    'raise_on_warnings': False
}

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Gallery table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            text TEXT,
            timestamp DATETIME NOT NULL
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE
        )
    ''')
    
    # Users table - check if it already exists (might be Laravel table)
    cursor.execute("SHOW TABLES LIKE 'users'")
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    # Seed Categories
    categories = ['General', 'Hair Style']
    for cat in categories:
        cursor.execute('INSERT IGNORE INTO categories (name) VALUES (%s)', (cat,))
        
    # Add category_id to gallery if not exists
    cursor.execute("SHOW COLUMNS FROM gallery LIKE 'category_id'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('ALTER TABLE gallery ADD COLUMN category_id INT DEFAULT 1')
        cursor.execute('ALTER TABLE gallery ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id)')

    conn.commit()
    cursor.close()
    conn.close()

# ===== GALLERY FUNCTIONS =====

def save_gallery_item(filename, text, timestamp, category_id=1):
    """Save a gallery item to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gallery (filename, text, timestamp, category_id) VALUES (%s, %s, %s, %s)',
                 (filename, text, timestamp, category_id))
    inserted_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return inserted_id

def get_gallery_items():
    """Get all gallery items"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM gallery ORDER BY id DESC')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def get_gallery_count():
    """Get count of gallery items"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM gallery')
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def delete_gallery_item(item_id):
    """Delete a gallery item by ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get the filename before deleting
    cursor.execute('SELECT filename FROM gallery WHERE id = %s', (item_id,))
    item = cursor.fetchone()
    
    if not item:
        cursor.close()
        conn.close()
        return None
    
    filename = item['filename']
    
    # Delete from database
    cursor.execute('DELETE FROM gallery WHERE id = %s', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return filename

# ===== USER FUNCTIONS =====

def create_user(name, email, password,created_at,updated_at):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, password,created_at,updated_at) VALUES (%s, %s, %s,%s,%s)', (name, email, password,created_at,updated_at))
        user_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return user_id
    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        return None

def get_all_users():
    """Get all users"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY id DESC')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, email, password, created_at FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user(user_id, name, email, password, updated_at):
    """Update user information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET name = %s, email = %s, password = %s, updated_at = %s WHERE id = %s', 
                      (name, email, password, updated_at, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        return False

def delete_user(user_id):
    """Delete a user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    return affected_rows > 0

def get_categories():
    """Get all categories"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories
