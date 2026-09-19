import sqlite3
import os

DB_FILE = "app/database/ecommerce.db"

def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection

# Remove existing database file if re-running
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 1. Enable foreign key enforcement in SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# 2. Create Tables with Proper Constraints
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);
""")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL UNIQUE,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    payment_method TEXT,
    paid_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
""")

# 3. Add Indexes for Foreign Key Columns
cursor.execute("CREATE INDEX idx_products_category_id ON products(category_id);")
cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id);")
cursor.execute("CREATE INDEX idx_order_items_order_id ON order_items(order_id);")
cursor.execute("CREATE INDEX idx_order_items_product_id ON order_items(product_id);")
cursor.execute("CREATE INDEX idx_payments_order_id ON payments(order_id);")

# 4. Insert Realistic Sample Data
# Users (5)
users_data = [
    ("Alice Smith", "alice@example.com", "hashed_pw_alice"),
    ("Bob Jones", "bob@example.com", "hashed_pw_bob"),
    ("Charlie Brown", "charlie@example.com", "hashed_pw_charlie"),
    ("Diana Prince", "diana@example.com", "hashed_pw_diana"),
    ("Evan Wright", "evan@example.com", "hashed_pw_evan")
]
cursor.executemany("INSERT INTO users (name, email, password) VALUES (?, ?, ?);", users_data)

# Categories (5)
categories_data = [
    ("Electronics",),
    ("Clothing",),
    ("Books",),
    ("Home & Kitchen",),
    ("Sports",)
]
cursor.executemany("INSERT INTO categories (name) VALUES (?);", categories_data)

# Products (11 items distributed across categories)
products_data = [
    (1, "Wireless Bluetooth Headphones", "Active noise cancelling over-ear headphones", 79.99, 50),
    (1, "Smartphone 128GB", "Latest 5G smartphone with OLED display", 699.99, 25),
    (1, "USB-C Fast Charger", "20W wall charger adapter", 19.99, 150),
    (2, "Men's Casual Cotton T-Shirt", "100% breathable cotton crewneck", 14.99, 100),
    (2, "Women's Denim Jeans", "Classic high-waist slim fit jeans", 49.99, 60),
    (3, "Python Programming for Beginners", "Comprehensive guide to learning Python", 29.99, 40),
    (3, "FastAPI Web Development", "Build modern high-performance web APIs", 39.99, 30),
    (4, "Stainless Steel Blender", "1000W multi-speed countertop blender", 89.99, 20),
    (4, "Non-Stick Chef Knife", "8-inch professional kitchen knife", 24.99, 75),
    (5, "Yoga Mat with Strap", "Eco-friendly non-slip exercise mat", 22.99, 85),
    (5, "Adjustable Dumbbells Set", "Pair of adjustable weights for home workouts", 129.99, 15)
]
cursor.executemany("""
INSERT INTO products (category_id, name, description, price, stock_quantity) 
VALUES (?, ?, ?, ?, ?);
""", products_data)

# Orders (5 orders with required statuses)
orders_data = [
    (1, "pending", 99.98),
    (2, "confirmed", 749.98),
    (3, "shipped", 39.99),
    (4, "delivered", 114.98),
    (5, "cancelled", 129.99)
]
cursor.executemany("""
INSERT INTO orders (user_id, status, total_amount) 
VALUES (?, ?, ?);
""", orders_data)

# Order Items
order_items_data = [
    (1, 1, 1, 79.99),   # Order 1: Headphones
    (1, 3, 1, 19.99),   # Order 1: Charger
    (2, 2, 1, 699.99),  # Order 2: Smartphone
    (2, 4, 1, 49.99),   # Order 2: T-Shirt
    (3, 7, 1, 39.99),   # Order 3: FastAPI Book
    (4, 8, 1, 89.99),   # Order 4: Blender
    (4, 9, 1, 24.99),   # Order 4: Knife
    (5, 11, 1, 129.99)  # Order 5: Dumbbells
]
cursor.executemany("""
INSERT INTO order_items (order_id, product_id, quantity, unit_price) 
VALUES (?, ?, ?, ?);
""", order_items_data)

# Payments (pending, paid, refunded statuses)
payments_data = [
    (1, 99.98, "pending", "Credit Card", None),
    (2, 749.98, "paid", "PayPal", "2026-06-01 12:30:00"),
    (3, 39.99, "paid", "Credit Card", "2026-06-02 14:15:00"),
    (4, 114.98, "paid", "Apple Pay", "2026-06-03 09:00:00"),
    (5, 129.99, "refunded", "Credit Card", "2026-06-04 16:45:00")
]
cursor.executemany("""
INSERT INTO payments (order_id, amount, status, payment_method, paid_at) 
VALUES (?, ?, ?, ?, ?);
""", payments_data)

conn.commit()

# 5. Verification Checks
print("==========================================")
print("       DATABASE VERIFICATION REPORT       ")
print("==========================================")

cursor.execute("PRAGMA foreign_keys;")
print(f"✔ Foreign Key Enforcement: {cursor.fetchone()[0] == 1}")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"✔ Tables Created: {', '.join(tables)}")

for table in ["users", "categories", "products", "orders", "order_items", "payments"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table};")
    print(f"  - Table '{table}': {cursor.fetchone()[0]} rows")


conn.close()
print("==========================================")
print("Success! 'ecommerce.db' is ready for FastAPI.")
