#!/usr/bin/env python3
"""
Database Explorer for FertiSmart
Simple script to connect and explore your database
"""

import sqlite3
import os
from datetime import datetime

def connect_to_database():
    """Connect to the FertiSmart SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), 'fertismart.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows column access by name
        print(f"✅ Connected to database: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def show_tables(conn):
    """Show all tables in the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📋 Tables in the database:")
    for table in tables:
        print(f"  - {table[0]}")
    
    return [table[0] for table in tables]

def show_table_info(conn, table_name):
    """Show information about a specific table"""
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"\n🔍 Table: {table_name}")
    print("Columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] else ''}")
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"Row count: {count}")
    
    # Show sample data if exists
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        rows = cursor.fetchall()
        print("Sample data:")
        for row in rows:
            print(f"  {dict(row)}")

def interactive_query(conn):
    """Allow interactive SQL queries"""
    print("\n💻 Interactive Query Mode (type 'exit' to quit)")
    
    while True:
        query = input("\nSQL> ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            break
        
        if not query:
            continue
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.lower().startswith('select'):
                rows = cursor.fetchall()
                if rows:
                    print(f"Results ({len(rows)} rows):")
                    for row in rows:
                        print(f"  {dict(row)}")
                else:
                    print("No results found.")
            else:
                conn.commit()
                print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
        
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function to explore the database"""
    print("🌱 FertiSmart Database Explorer")
    print("="*50)
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Show all tables
        tables = show_tables(conn)
        
        if not tables:
            print("No tables found in the database.")
            return
        
        # Show detailed info for each table
        for table in tables:
            show_table_info(conn, table)
        
        # Interactive mode
        print("\n" + "="*50)
        interactive_query(conn)
    
    finally:
        conn.close()
        print("\n👋 Database connection closed.")

if __name__ == "__main__":
    main()