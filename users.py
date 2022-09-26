import sqlite3

conn = sqlite3.connect('base.db', timeout=7)
cur1 = conn.cursor()
cur1.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INT,
   nickname TEXT,
   best INT,
   wins INT,
   loses INT);
""")
conn.commit()

def find_user(user_in):
    cur1.execute("SELECT user_id FROM users;")
    for e in cur1:
        if e[0] == user_in:
            return True
    return False

def update_nickname(user, nick):
    if find_user(user):
        cur1.execute(f"UPDATE users SET nickname= ? WHERE user_id= ?", (f"{nick}", f"{user}"))
    else:
        user = (user, nick, 0, 0, 0)
        cur1.execute("INSERT INTO users values(?, ?, ?, ?, ?)", user)
    conn.commit()

def update_wins(user):
    cur1.execute(f"UPDATE users SET wins=(wins+1) WHERE user_id={user}")
    conn.commit()

def update_loses(user):
    cur1.execute(f"UPDATE users SET loses=(loses+1) WHERE user_id={user}")
    conn.commit()

def get_best(user):
    cur1.execute(f"SELECT best FROM users WHERE user_id={user}")
    for i in cur1:
        return i[0]

def update_best(user, score):
    cur1.execute(f"UPDATE users SET best={score} WHERE user_id={user}")
    conn.commit()

def get_all(user):
    cur1.execute(f"SELECT * FROM users WHERE user_id={user}")
    for i in cur1:
        return i
    return None
