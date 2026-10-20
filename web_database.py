import sqlite3
from pathlib import Path

DATABASE_NAME = Path(__file__).with_name('robotics_web.db')


def connect_database():
    con = sqlite3.connect(DATABASE_NAME, timeout=30)
    con.execute('PRAGMA journal_mode=WAL')
    return con


def create_tables():
    con = connect_database(); cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS learner (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL COLLATE NOCASE UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS teacher (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL COLLATE NOCASE UNIQUE)')
    cur.execute('''CREATE TABLE IF NOT EXISTS lesson_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id INTEGER NOT NULL,
        lesson_number INTEGER NOT NULL,
        completed INTEGER DEFAULT 0,
        UNIQUE(learner_id, lesson_number))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS activity_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner_id INTEGER NOT NULL,
        activity_number INTEGER NOT NULL,
        attempts INTEGER DEFAULT 0,
        completed INTEGER DEFAULT 0,
        UNIQUE(learner_id, activity_number))''')
    con.commit(); con.close()


def register_user(role, name):
    name = name.strip()
    if not name:
        return False, 'empty', None
    con = connect_database(); cur = con.cursor()
    if role == 'learner':
        cur.execute('SELECT id FROM teacher WHERE LOWER(TRIM(name))=LOWER(TRIM(?)) LIMIT 1', (name,))
        if cur.fetchone():
            con.close(); return False, 'teacher', None
        table = 'learner'
    else:
        table = 'teacher'
    try:
        cur.execute(f'INSERT INTO {table}(name) VALUES (?)', (name,))
        uid = cur.lastrowid
        con.commit(); con.close(); return True, 'registered', uid
    except sqlite3.IntegrityError:
        cur.execute(f'SELECT id FROM {table} WHERE LOWER(TRIM(name))=LOWER(TRIM(?)) LIMIT 1', (name,))
        row = cur.fetchone(); con.close()
        return False, 'exists', row[0] if row else None


def login_user(role, name):
    name = name.strip()
    if not name:
        return None
    con = connect_database(); cur = con.cursor()
    if role == 'learner':
        cur.execute('SELECT id FROM teacher WHERE LOWER(TRIM(name))=LOWER(TRIM(?)) LIMIT 1', (name,))
        if cur.fetchone():
            con.close(); return None
        table = 'learner'
    else:
        table = 'teacher'
    cur.execute(f'SELECT id,name FROM {table} WHERE LOWER(TRIM(name))=LOWER(TRIM(?)) LIMIT 1', (name,))
    row = cur.fetchone(); con.close(); return row


def complete_lesson(learner_id, lesson_number):
    if learner_id is None:
        return False
    con = connect_database(); cur = con.cursor()
    cur.execute('''INSERT INTO lesson_progress(learner_id,lesson_number,completed)
                   VALUES(?,?,1)
                   ON CONFLICT(learner_id,lesson_number) DO UPDATE SET completed=1''',
                (learner_id, lesson_number))
    con.commit(); con.close(); return True


def get_completed_lessons(learner_id):
    if learner_id is None:
        return []
    con = connect_database(); cur = con.cursor()
    cur.execute('SELECT lesson_number FROM lesson_progress WHERE learner_id=? AND completed=1 ORDER BY lesson_number', (learner_id,))
    rows = cur.fetchall(); con.close(); return [r[0] for r in rows]


def record_activity_attempt(learner_id, activity_number, successful=False):
    if learner_id is None:
        return False
    con = connect_database(); cur = con.cursor()
    cur.execute('INSERT OR IGNORE INTO activity_progress(learner_id,activity_number,attempts,completed) VALUES(?,?,0,0)', (learner_id, activity_number))
    cur.execute('UPDATE activity_progress SET attempts=attempts+1 WHERE learner_id=? AND activity_number=?', (learner_id, activity_number))
    if successful:
        cur.execute('UPDATE activity_progress SET completed=1 WHERE learner_id=? AND activity_number=?', (learner_id, activity_number))
    con.commit(); con.close(); return True


def get_activity_progress(learner_id):
    if learner_id is None:
        return []
    con = connect_database(); cur = con.cursor()
    cur.execute('SELECT activity_number,attempts,completed FROM activity_progress WHERE learner_id=? ORDER BY activity_number', (learner_id,))
    rows = cur.fetchall(); con.close(); return rows


def calculate_progress(learner_id):
    if learner_id is None:
        return 0
    lessons = get_completed_lessons(learner_id)
    acts = get_activity_progress(learner_id)
    done_acts = sum(1 for _,_,done in acts if done == 1)
    return round(((len(lessons)+done_acts)/7)*100)


def get_all_learners_progress():
    con = connect_database(); cur = con.cursor()
    cur.execute('''SELECT l.id,l.name FROM learner l
                   WHERE NOT EXISTS (SELECT 1 FROM teacher t WHERE LOWER(TRIM(t.name))=LOWER(TRIM(l.name)))
                   ORDER BY l.name''')
    learners = cur.fetchall(); con.close()
    out=[]
    for learner_id,name in learners:
        lessons = get_completed_lessons(learner_id)
        acts = get_activity_progress(learner_id)
        done_acts = sum(1 for _,_,done in acts if done == 1)
        out.append({'Morutwana':name,'Dithuto':f'{len(lessons)}/4','Ditiro':f'{done_acts}/3','Kgatelopele':f'{calculate_progress(learner_id)}%'})
    return out


create_tables()
