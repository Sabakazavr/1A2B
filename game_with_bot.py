import sqlite3

from users import conn
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS GameWithBot(
   user_id INT,
   number TEXT,
   try TEXT,
   bulls INT,
   cows INT,
   move INT);
""")
conn.commit()

def get_all_moves(user):
    cur.execute(f"select try, bulls, cows, move from GameWithBot where user_id='{user}' ORDER BY move")
    return cur

def delete_moves(user):
    cur.execute(f"DELETE FROM GameWithBot WHERE user_id='{user}'")
    conn.commit()

def move_to_base(user, num, num_try, bll, cw, mv):
    new_move = (user, num, num_try, bll, cw, mv)
    cur.execute('INSERT INTO GameWithBot values(?, ?, ?, ?, ?, ?)', new_move)
    conn.commit()

def get_last(user):
    cur.execute(f"select number, move from GameWithBot where user_id='{user}' ORDER BY move DESC")
    for i in cur:
        return i
