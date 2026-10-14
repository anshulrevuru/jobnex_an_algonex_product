"""
test_db.py
Script to test connection between Python and MySQL Server / MySQL Workbench.
"""

import sys
import mysql.connector
from mysql.connector import Error
import database

def test_database_connection():
    print("=" * 60)
    print("      JobNex - MySQL Database Connection Test")
    print("=" * 60)
    print(f"Target Host:     {database.DB_HOST}")
    print(f"Target Port:     {database.DB_PORT}")
    print(f"Target User:     {database.DB_USER}")
    print(f"Target Database: {database.DB_NAME}")
    print("-" * 60)

    # Step 1: Test Server Connection
    print("[1/4] Connecting to MySQL Server...")
    try:
        conn = database.get_connection(use_database=False)
        if conn.is_connected():
            server_version = conn.get_server_info()
            print(f"      SUCCESS: Connected to MySQL Server v{server_version}")
            conn.close()
    except Error as e:
        print(f"      FAILED to connect to MySQL Server: {e}")
        print("\nTroubleshooting Tips:")
        print("1. Ensure MySQL Server / MySQL Workbench service is running.")
        print("2. Check DB_PASSWORD in backend/.env file.")
        print("3. Check host and port (default 3306).")
        return False

    # Step 2: Initialize Database and Tables
    print("\n[2/4] Initializing Database & Tables (`resumes`, `resume_analyzer`)...")
    init_ok = database.init_db()
    if init_ok:
        print("      SUCCESS: Database and tables verified/created.")
    else:
        print("      FAILED: Could not initialize database/tables.")
        return False

    # Step 3: Inspect Database Tables
    print("\n[3/4] Inspecting Tables in Database...")
    try:
        conn = database.get_connection(use_database=True)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"      Tables found in '{database.DB_NAME}': {tables}")

        for table in tables:
            cursor.execute(f"DESCRIBE `{table}`;")
            columns = cursor.fetchall()
            col_names = [f"{col[0]} ({col[1]})" for col in columns]
            print(f"       -> Table '{table}': {', '.join(col_names)}")

        cursor.close()
        conn.close()
    except Error as e:
        print(f"      FAILED to inspect tables: {e}")
        return False

    # Step 4: Summary
    print("\n[4/4] Connection Verification Complete!")
    print("=" * 60)
    print(" MySQL Workbench is ready to use with JobNex Backend!")
    print(" You can open MySQL Workbench, refresh Schemas, and view:")
    print(f"   Database: `{database.DB_NAME}`")
    print("   Tables:   `resumes`, `resume_analyzer`")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
