import sqlite3

def create_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS your_table_name (
                        id INTEGER PRIMARY KEY,
                        date_joined DATE,
                        latest_block_number INTEGER,
                        delay INTEGER
                    )''')
    conn.commit()
    conn.close()

def add_field(field_name, field_type):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''ALTER TABLE your_table_name ADD COLUMN {} {}'''.format(field_name, field_type))
    conn.commit()
    conn.close()

def delete_field(field_name):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''ALTER TABLE your_table_name DROP COLUMN {}'''.format(field_name))
    conn.commit()
    conn.close()
    
create_db()