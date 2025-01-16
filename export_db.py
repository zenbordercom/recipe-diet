import sqlite3
import json

def export_db_to_json():
    # Connect to the database
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Create a dictionary to store all data
    data = {}
    
    # Export each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Get all rows
        rows = cursor.fetchall()
        
        # Convert rows to list of dictionaries
        table_data = []
        for row in rows:
            table_data.append(dict(zip(columns, row)))
            
        data[table_name] = table_data
    
    # Close the connection
    conn.close()
    
    # Write to JSON file
    with open('recipes1219.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    export_db_to_json()
