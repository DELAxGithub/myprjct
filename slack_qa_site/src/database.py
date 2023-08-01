import sqlite3
import read_slack_data

def connect_db():
    conn = sqlite3.connect('slack.db')
    print('successful connection with sqlite version ' + sqlite3.version)
    return conn

def create_table(conn):
    try:
        conn.execute('''
            CREATE TABLE slack_messages (
                text TEXT NOT NULL,
                user_id TEXT NOT NULL,
                ts TIMESTAMP NOT NULL,
                channel TEXT NOT NULL);
        ''')
        print('Table created successfully')
    except Exception as e:
        print('Error:', e)

def save_messages(data):
    conn = connect_db()
    cur = conn.cursor()
    
    for msg in data:
        if 'text' in msg and 'user' in msg and 'ts' in msg and 'channel' in msg:
            cur.execute('''
                INSERT INTO slack_messages (text, user_id, ts, channel)
                VALUES (?, ?, ?, ?)
            ''', (msg['text'], msg['user'], msg['ts'], msg['channel']))
    
    conn.commit()
    conn.close()

def main():
    conn = connect_db()
    create_table(conn)
    slack_data = read_slack_data.read_slack_data()
    save_messages(slack_data)

if __name__ == '__main__':
    main()
