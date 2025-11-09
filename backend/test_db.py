import psycopg2

try:
    conn = psycopg2.connect(
        dbname="device_status",
        user="postgres",
        password="Venky@123",
        host="localhost",
        port=1947  # or 5433 if you used that
    )
    print("✅ Connected successfully to PostgreSQL!")
    conn.close()

except Exception as e:
    print("Database connection error:", e)
    print("❌ Failed to connect to database.")
