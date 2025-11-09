import psycopg2

# Database connection details
DB_CONFIG = {
    'dbname': 'device_status',  # your database name
    'user': 'postgres',
    'password': 'Venky@123',  # <-- replace with your actual postgres password
    'host': 'localhost',
    'port': '1947'  # your port
}

# SQL commands to create tables
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("✅ Tables created successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error while creating tables:", e)

if __name__ == "__main__":
    init_db()
