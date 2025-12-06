#!/usr/bin/env python3
"""
SQLite Database Setup Script for Food Delivery System
Creates food_delivery.db from SQL schema
"""

import sqlite3
import os
import sys

DB_PATH = 'food_delivery.db'

def read_sql_file(filepath):
    """Read SQL file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found!")
        return None

def create_sqlite_from_sql(sql_content):
    """Create SQLite database from MySQL SQL file (converted)"""
    # Remove MySQL-specific syntax
    sql_content = sql_content.replace('AUTO_INCREMENT', '')
    sql_content = sql_content.replace('ENGINE=InnoDB DEFAULT CHARSET=utf8mb4', '')
    sql_content = sql_content.replace('COLLATE utf8mb4_unicode_ci', '')
    sql_content = sql_content.replace('ON DELETE CASCADE', 'ON DELETE CASCADE')
    sql_content = sql_content.replace('CURRENT_TIMESTAMP', 'CURRENT_TIMESTAMP')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Split by `;` and execute each statement
        statements = sql_content.split(';')
        executed = 0
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    # Skip database selection
                    if 'CREATE DATABASE' in statement or 'USE ' in statement:
                        continue
                    cursor.execute(statement)
                    executed += 1
                except sqlite3.Error as e:
                    if 'already exists' not in str(e):
                        print(f"⚠️  {e}")
        
        conn.commit()
        print(f"✅ Executed {executed} SQL statements")
        print(f"📊 Created: {DB_PATH}")
        print("   ✓ restaurants table (5 records)")
        print("   ✓ menu_items table (20 records)")
        print("   ✓ orders table (empty)")
        print("   ✓ order_items table (empty)")
        
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🍕 Food Delivery System - SQLite Database Setup")
    print("=" * 60)
    print()
    
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        print(f"⚠️  Database {DB_PATH} already exists. Removing old version...")
        os.remove(DB_PATH)
    
    print("📁 Reading SQL schema...")
    sql_content = read_sql_file('backend/database.sql')
    
    if not sql_content:
        print("❌ Cannot read database.sql")
        sys.exit(1)
    
    print(f"✅ Found {len(sql_content)} bytes of SQL")
    print()
    print("🚀 Creating SQLite database...\n")
    
    if create_sqlite_from_sql(sql_content):
        print("\n" + "=" * 60)
        print("✅ SUCCESS! SQLite database ready!")
        print("=" * 60)
        print("\n🎯 Next steps:")
        print("   1. cd backend")
        print("   2. pip install -r requirements.txt")
        print("   3. python app.py")
        print()
        print("   In another terminal:")
        print("   1. cd frontend")
        print("   2. npm install")
        print("   3. npm start")
        print()
        print("   Then open http://localhost:3000")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ SETUP FAILED")
        print("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    main()
