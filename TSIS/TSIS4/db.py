import psycopg2
from config import *

# подключение к БД
def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# создать таблицы
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions(
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER,
        level_reached INTEGER,
        played_at TIMESTAMP DEFAULT NOW()
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# получить или создать игрока
def get_player_id(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()

    if res:
        pid = res[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
        pid = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return pid


# сохранить результат
def save_score(username, score, level):
    conn = get_conn()
    cur = conn.cursor()

    pid = get_player_id(username)

    cur.execute("""
    INSERT INTO game_sessions(player_id, score, level_reached)
    VALUES(%s,%s,%s)
    """, (pid, score, level))

    conn.commit()
    cur.close()
    conn.close()


# топ 10
def get_top_scores():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT p.username, g.score, g.level_reached, g.played_at
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    ORDER BY g.score DESC
    LIMIT 10
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


# лучший результат игрока
def get_best(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT MAX(g.score)
    FROM game_sessions g
    JOIN players p ON p.id = g.player_id
    WHERE p.username=%s
    """, (username,))

    res = cur.fetchone()[0]

    cur.close()
    conn.close()
    return res if res else 0