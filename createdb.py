import json
import os
import sqlite3
import time

from bible import get_book_id_by_name

NT_FILE_PATH = './EN/NT'
OT_FILE_PATH = './EN/OT'

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Function to insert JSON data into the SQLite database
def insert_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
        for chapter in data['chapters']:
            for verse in chapter['verses']:
                cursor.execute('''INSERT INTO verses (book, chapter, verse, content)
                                  VALUES (?, ?, ?, ?)''', (get_book_id_by_name(data['bookName']), int(chapter['chapter']), int(verse['verse']), verse['content']))


def create_bible_db():
    # Insert data from JSON files to the SQLite database
    # Insert New Testament
    for file_name in os.listdir(NT_FILE_PATH):
        if file_name.endswith('.json'):
            insert_data(os.path.join(NT_FILE_PATH, file_name))

    # Insert Old Testament
    for file_name in os.listdir(OT_FILE_PATH):
        if file_name.endswith('.json'):
            insert_data(os.path.join(OT_FILE_PATH, file_name))


# Create a table to store Bible verses
cursor.execute('''CREATE TABLE IF NOT EXISTS verses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              book TEXT,
              bookId INTEGER,
              chapter INTEGER,
              verse INTEGER,
              content TEXT)''')


create_bible_db()

# Commit changes and close the connection
conn.commit()
conn.close()