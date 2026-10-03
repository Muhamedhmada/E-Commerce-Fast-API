import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database", "ecommerce.db")

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
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
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        total_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL UNIQUE,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        payment_method TEXT,
        paid_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """,
]

INDEX_STATEMENTS = [
    "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);",
]

users_data = [
    ("Alice Smith", "alice@example.com", "hashed_pw_alice"),
    ("Bob Jones", "bob@example.com", "hashed_pw_bob"),
    ("Charlie Brown", "charlie@example.com", "hashed_pw_charlie"),
    ("Diana Prince", "diana@example.com", "hashed_pw_diana"),
    ("Evan Wright", "evan@example.com", "hashed_pw_evan")
]

categories_data = [
    ("Electronics",),
    ("Clothing",),
    ("Books",),
    ("Home & Kitchen",),
    ("Sports",)
]

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

orders_data = [
    (1, "pending", 99.98),
    (2, "confirmed", 749.98),
    (3, "shipped", 39.99),
    (4, "delivered", 114.98),
    (5, "cancelled", 129.99)
]

order_items_data = [
    (1, 1, 1, 79.99),
    (1, 3, 1, 19.99),
    (2, 2, 1, 699.99),
    (2, 4, 1, 49.99),
    (3, 7, 1, 39.99),
    (4, 8, 1, 89.99),
    (4, 9, 1, 24.99),
    (5, 11, 1, 129.99)
]

payments_data = [
    (1, 99.98, "pending", "Credit Card", None),
    (2, 749.98, "paid", "PayPal", "2026-06-01 12:30:00"),
    (3, 39.99, "paid", "Credit Card", "2026-06-02 14:15:00"),
    (4, 114.98, "paid", "Apple Pay", "2026-06-03 09:00:00"),
    (5, 129.99, "refunded", "Credit Card", "2026-06-04 16:45:00")
]

SEED_STATEMENTS = [
    ("users", "INSERT INTO users (name, email, password) VALUES (?, ?, ?);", users_data),
    ("categories", "INSERT INTO categories (name) VALUES (?);", categories_data),
    (
        "products",
        """
        INSERT INTO products (category_id, name, description, price, stock_quantity)
        VALUES (?, ?, ?, ?, ?);
        """,
        products_data
    ),
    (
        "orders",
        "INSERT INTO orders (user_id, status, total_amount) VALUES (?, ?, ?);",
        orders_data
    ),
    (
        "order_items",
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?);",
        order_items_data
    ),
    (
        "payments",
        "INSERT INTO payments (order_id, amount, status, payment_method, paid_at) VALUES (?, ?, ?, ?, ?);",
        payments_data
    ),
]


def get_connection():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    for statement in SCHEMA_STATEMENTS:
        cursor.execute(statement)
    for statement in INDEX_STATEMENTS:
        cursor.execute(statement)
    conn.commit()

    for table, statement, rows in SEED_STATEMENTS:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(statement, rows)
            conn.commit()

    conn.close()


def reset_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()


def print_verification_report():
    conn = get_connection()
    cursor = conn.cursor()

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
    print(f"Success! '{DB_FILE}' is ready for FastAPI.")


init_db()

if __name__ == "__main__":
    reset_database()
    print_verification_report()