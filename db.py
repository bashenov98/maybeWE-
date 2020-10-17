import sys
import sqlite3
import random

def loadDB():
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS user_data
    ( 
        telegram_id INTEGER NOT NULL,
        sex TEXT 
    );
    CREATE TABLE IF NOT EXISTS applications
    ( 
        category TEXT,
        user_telegram_id INTEGER,
        sex TEXT,
        find_sex TEXT,
        time TEXT
    );
    CREATE TABLE if not EXISTS likes
    ( 
        liked_user_telegram_id INTEGER NOT NULL,
        application_id INTEGER NOT NULL
    );
    CREATE TABLE if not EXISTS codes
    (
        user_id INTEGER NOT NULL,
        code INTEGER NOT NULL
    )
    '''
    )
    conn.commit()
    conn.close()

def user_check(user_id, sex):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    if len(cur.execute('''SELECT telegram_id FROM user_data WHERE telegram_id = ?        
            ''', (user_id,)).fetchall())>0:
        # c=cur.execute('''SELECT telegram_id FROM userdata WHERE id = ?''', (user_id,)).fetchone()
        # user_data['Name']=c[0]
        # c=cur.execute('''SELECT sex FROM userdata WHERE id = ?''', (sex,)).fetchone()
        # user_data['sex']=c[0]
        print(len(cur.execute('''SELECT telegram_id FROM user_data WHERE telegram_id = ?        
            ''', (user_id,)).fetchall()))
    else:
        cur.execute('''INSERT OR IGNORE INTO user_data (telegram_id, sex) VALUES (?, ?)''', \
        (user_id, sex,))
        print(len(cur.execute('''SELECT telegram_id FROM user_data WHERE telegram_id = ?        
            ''', (user_id,)).fetchall()))
    conn.commit()
    conn.close()

def create_bid(user_id, category, sex, sex2, time):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.execute('''INSERT OR IGNORE INTO applications (user_telegram_id, category, sex, find_sex, time) VALUES (?, ?, ?, ?, ?)''', \
        (user_id, category, sex, sex2, time))
    print(cur.execute('''SELECT rowid FROM applications''').fetchall())
    conn.commit()
    conn.close()

def get_application_id(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    app_id = cur.execute('''SELECT rowid FROM applications WHERE user_telegram_id = ?''', (user_id, )).fetchone()[0]
    return app_id
    

def make_like(user_id, application_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.execute('''INSERT OR IGNORE INTO likes (liked_user_telegram_id, application_id) VALUES (?, ?)''', \
        (user_id, application_id))
    conn.commit()
    conn.close()

def check_bid(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    application = int(cur.execute('''SELECT rowid FROM applications WHERE user_telegram_id = ?''', (user_id, )).fetchone()[0])
    if len(cur.execute('''SELECT rowid FROM likes WHERE application_id = ?''', (application, )).fetchall()) > 0:
        return True
        conn.commit()
        conn.close()
    else:
        return False
        conn.commit()
        conn.close()

def get_slots(user_id, category1, sex, sex2):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    if sex2 == 'Без разницы':
        slots = cur.execute('''SELECT * FROM applications where category = ? and user_telegram_id <> ? ''', (category1, user_id)).fetchall()
        # print(slots)
        conn.commit()
        conn.close()
    else:
        slots = cur.execute('''SELECT * FROM applications where category = ? and user_telegram_id <> ?''', (category1, user_id)).fetchall()
        # print (cur.execute('''SELECT * FROM applications''').fetchall())
        conn.commit()
        conn.close()
    return slots

def delete_application(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.execute('''DELETE FROM applications WHERE user_telegram_id = ?''', (user_id, ))
    conn.commit()
    conn.close()

def get_my_slot_category(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    slot_fields = cur.execute('''SELECT category FROM applications WHERE user_telegram_id = ?''', (user_id, )).fetchone()[0]
    conn.commit()
    conn.close()
    print(str(slot_fields))
    return slot_fields

def get_my_slot_sex2(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    slot_fields = cur.execute('''SELECT find_sex FROM applications WHERE user_telegram_id = ?''', (user_id, )).fetchone()[0]
    conn.commit()
    conn.close()
    print(slot_fields)
    return slot_fields

def get_matcher_id(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    app_id = cur.execute('''SELECT application_id FROM likes WHERE liked_user_telegram_id = ?''', (user_id, )).fetchone()[0]
    app_row_id = cur.execute('''SELECT * FROM application where category = ? and find_sex = ?''', )
    matcher_id = cur.execute('''SELECT * FROM applications''').fetchall()
    print(matcher_id)
    conn.commit()
    conn.close()
    return matcher_id
    
def send_code(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.execute('''INSERT OR IGNORE INTO codes (user_id, code) VALUES (?, ?)''', (int(user_id), int(random.randrange(1000, 9999))))
    conn.commit()
    conn.close()

def get_code(user_id):
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    code = cur.execute('''SELECT code FROM codes WHERE user_id = ?''', (user_id, )).fetchone()[0]
    return code

# Требования для показа слотов:
# 1. Совпадают категории
# 2. Запросы должны быть чужими
# 3. 

# 1. я лайкнул фотку
# 2. я отправляю код
# 3. 