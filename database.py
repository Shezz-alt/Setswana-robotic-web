import sqlite3
import hashlib
import hmac
import secrets
from tkinter import simpledialog, messagebox


DATABASE_NAME = "robotics_learning.db"

PIN_MIN_LENGTH = 4
PIN_MAX_LENGTH = 6
PBKDF2_ITERATIONS = 200000

TOTAL_LESSONS = 4
TOTAL_ACTIVITIES = 5
TOTAL_PROGRESS_ITEMS = TOTAL_LESSONS + TOTAL_ACTIVITIES


# ============================================================
# ACTIVE USER INFORMATION
# ============================================================

active_learner_id = None
active_learner_name = None

active_teacher_id = None
active_teacher_name = None

active_user_role = None


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    return sqlite3.connect(
        DATABASE_NAME
    )


# ============================================================
# PIN SECURITY
# ============================================================

def validate_pin(pin):

    if pin is None:
        return False

    pin = str(pin).strip()

    return (
        pin.isdigit()
        and PIN_MIN_LENGTH <= len(pin) <= PIN_MAX_LENGTH
    )


def hash_pin(
    pin,
    salt=None
):

    if salt is None:

        salt = secrets.token_hex(
            16
        )

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        str(pin).encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS
    )

    return (
        salt,
        digest.hex()
    )


def verify_pin(
    pin,
    salt,
    stored_hash
):

    if (
        not validate_pin(pin)
        or not salt
        or not stored_hash
    ):

        return False

    _, candidate_hash = hash_pin(
        pin,
        salt
    )

    return hmac.compare_digest(
        candidate_hash,
        stored_hash
    )


# ============================================================
# PIN INPUT
# ============================================================

def prompt_new_pin(title):

    while True:

        pin = simpledialog.askstring(
            title,
            (
                "Tlhama PIN ya dinomoro tse 4 go ya go 6.\n\n"
                "Create a 4-6 digit PIN:"
            ),
            show="*"
        )

        if pin is None:
            return None

        pin = pin.strip()

        if not validate_pin(pin):

            messagebox.showwarning(
                "PIN",
                (
                    "PIN e tshwanetse go nna dinomoro fela "
                    "tse 4 go ya go 6."
                )
            )

            continue

        confirm_pin = simpledialog.askstring(
            title,
            (
                "Netefatsa PIN.\n\n"
                "Confirm PIN:"
            ),
            show="*"
        )

        if confirm_pin is None:
            return None

        confirm_pin = confirm_pin.strip()

        if pin != confirm_pin:

            messagebox.showwarning(
                "PIN",
                (
                    "Di-PIN ga di tshwane. "
                    "Leka gape."
                )
            )

            continue

        return pin


def prompt_login_pin(title):

    pin = simpledialog.askstring(
        title,
        "Kwala PIN ya gago:",
        show="*"
    )

    if pin is None:
        return None

    return pin.strip()


# ============================================================
# DATABASE COLUMN CHECK
# ============================================================

def column_exists(
    cursor,
    table_name,
    column_name
):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    return column_name in columns


def ensure_pin_columns(
    cursor,
    table_name
):

    if not column_exists(
        cursor,
        table_name,
        "pin_salt"
    ):

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN pin_salt TEXT
            """
        )

    if not column_exists(
        cursor,
        table_name,
        "pin_hash"
    ):

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN pin_hash TEXT
            """
        )


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS learner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    ensure_pin_columns(
        cursor,
        "learner"
    )

    ensure_pin_columns(
        cursor,
        "teacher"
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lesson_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            lesson_number INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            UNIQUE(
                learner_id,
                lesson_number
            )
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            activity_number INTEGER NOT NULL,
            attempts INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            UNIQUE(
                learner_id,
                activity_number
            )
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# CLEAR ACTIVE USER
# ============================================================

def clear_active_user():

    global active_learner_id
    global active_learner_name

    global active_teacher_id
    global active_teacher_name

    global active_user_role

    active_learner_id = None
    active_learner_name = None

    active_teacher_id = None
    active_teacher_name = None

    active_user_role = None


# ============================================================
# REGISTER LEARNER
# ============================================================

def register_learner(name):

    global active_learner_id
    global active_learner_name
    global active_user_role

    name = name.strip()

    if not name:

        return (
            False,
            "empty"
        )

    connection = connect_database()
    cursor = connection.cursor()

    # Do not use teacher name as learner
    cursor.execute(
        """
        SELECT id

        FROM teacher

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        LIMIT 1
        """,
        (name,)
    )

    if cursor.fetchone():

        connection.close()

        return (
            False,
            "teacher"
        )

    # Check existing learner
    cursor.execute(
        """
        SELECT id

        FROM learner

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (name,)
    )

    if cursor.fetchone():

        connection.close()

        return (
            False,
            "exists"
        )

    connection.close()

    pin = prompt_new_pin(
        "PIN ya Morutwana"
    )

    if pin is None:

        return (
            False,
            "cancelled"
        )

    salt, pin_hash = hash_pin(
        pin
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO learner
        (
            name,
            pin_salt,
            pin_hash
        )

        VALUES (?, ?, ?)
        """,
        (
            name,
            salt,
            pin_hash
        )
    )

    new_learner_id = cursor.lastrowid

    connection.commit()
    connection.close()

    clear_active_user()

    active_learner_id = new_learner_id
    active_learner_name = name
    active_user_role = "learner"

    return (
        True,
        "registered"
    )


# ============================================================
# LOGIN LEARNER
# ============================================================

def login_learner(name):

    global active_learner_id
    global active_learner_name
    global active_user_role

    name = name.strip()

    if not name:
        return False

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM teacher

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        LIMIT 1
        """,
        (name,)
    )

    if cursor.fetchone():

        connection.close()
        return False

    cursor.execute(
        """
        SELECT
            id,
            name,
            pin_salt,
            pin_hash

        FROM learner

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (name,)
    )

    result = cursor.fetchone()

    connection.close()

    if not result:
        return False

    learner_id = result[0]
    learner_name = result[1]
    salt = result[2]
    stored_hash = result[3]

    # ========================================================
    # OLD ACCOUNT WITHOUT PIN
    # ========================================================

    if not salt or not stored_hash:

        answer = messagebox.askyesno(
            "Tshireletso ya Akhaonto",
            (
                "Akhaonto eno e dirilwe pele ga PIN.\n\n"
                "PIN e tshwanetse go tlhamiwa pele ga "
                "kgatelopele e ka tswelela.\n\n"
                "A o batla go tlhama PIN jaanong?"
            )
        )

        if not answer:
            return False

        new_pin = prompt_new_pin(
            "Tlhama PIN ya Morutwana"
        )

        if new_pin is None:
            return False

        new_salt, new_hash = hash_pin(
            new_pin
        )

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE learner

            SET
                pin_salt = ?,
                pin_hash = ?

            WHERE id = ?
            """,
            (
                new_salt,
                new_hash,
                learner_id
            )
        )

        connection.commit()
        connection.close()

        clear_active_user()

        active_learner_id = learner_id
        active_learner_name = learner_name
        active_user_role = "learner"

        messagebox.showinfo(
            "PIN",
            (
                "PIN ya morutwana e tlhamilwe.\n\n"
                "Go tloga jaanong PIN e tla tlhokega "
                "nako nngwe le nngwe fa o tsena."
            )
        )

        return True

    # ========================================================
    # NORMAL LOGIN
    # ========================================================

    pin = prompt_login_pin(
        "PIN ya Morutwana"
    )

    if pin is None:
        return False

    if not verify_pin(
        pin,
        salt,
        stored_hash
    ):

        messagebox.showwarning(
            "Ga go a Atlega",
            (
                "Leina kgotsa PIN "
                "ga e a siama."
            )
        )

        return False

    clear_active_user()

    active_learner_id = learner_id
    active_learner_name = learner_name
    active_user_role = "learner"

    return True


# ============================================================
# REGISTER TEACHER
# ============================================================

def register_teacher(name):

    global active_teacher_id
    global active_teacher_name
    global active_user_role

    name = name.strip()

    if not name:

        return (
            False,
            "empty"
        )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM teacher

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (name,)
    )

    if cursor.fetchone():

        connection.close()

        return (
            False,
            "exists"
        )

    cursor.execute(
        """
        SELECT id

        FROM learner

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (name,)
    )

    if cursor.fetchone():

        connection.close()

        return (
            False,
            "learner"
        )

    connection.close()

    pin = prompt_new_pin(
        "PIN ya Morutabana"
    )

    if pin is None:

        return (
            False,
            "cancelled"
        )

    salt, pin_hash = hash_pin(
        pin
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO teacher
        (
            name,
            pin_salt,
            pin_hash
        )

        VALUES (?, ?, ?)
        """,
        (
            name,
            salt,
            pin_hash
        )
    )

    new_teacher_id = cursor.lastrowid

    connection.commit()
    connection.close()

    clear_active_user()

    active_teacher_id = new_teacher_id
    active_teacher_name = name
    active_user_role = "teacher"

    return (
        True,
        "registered"
    )


# ============================================================
# LOGIN TEACHER
# ============================================================

def login_teacher(name):

    global active_teacher_id
    global active_teacher_name
    global active_user_role

    name = name.strip()

    if not name:
        return False

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            pin_salt,
            pin_hash

        FROM teacher

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (name,)
    )

    result = cursor.fetchone()

    connection.close()

    if not result:
        return False

    teacher_id = result[0]
    teacher_name = result[1]
    salt = result[2]
    stored_hash = result[3]

    # ========================================================
    # OLD TEACHER WITHOUT PIN
    # ========================================================

    if not salt or not stored_hash:

        answer = messagebox.askyesno(
            "Tshireletso ya Akhaonto",
            (
                "Akhaonto eno ya morutabana "
                "e dirilwe pele ga PIN.\n\n"
                "A o batla go tlhama PIN "
                "ya morutabana jaanong?"
            )
        )

        if not answer:
            return False

        new_pin = prompt_new_pin(
            "Tlhama PIN ya Morutabana"
        )

        if new_pin is None:
            return False

        new_salt, new_hash = hash_pin(
            new_pin
        )

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE teacher

            SET
                pin_salt = ?,
                pin_hash = ?

            WHERE id = ?
            """,
            (
                new_salt,
                new_hash,
                teacher_id
            )
        )

        connection.commit()
        connection.close()

        clear_active_user()

        active_teacher_id = teacher_id
        active_teacher_name = teacher_name
        active_user_role = "teacher"

        messagebox.showinfo(
            "PIN",
            (
                "PIN ya morutabana e tlhamilwe.\n\n"
                "Go tloga jaanong PIN e tla tlhokega "
                "nako nngwe le nngwe fa o tsena."
            )
        )

        return True

    # ========================================================
    # NORMAL TEACHER LOGIN
    # ========================================================

    pin = prompt_login_pin(
        "PIN ya Morutabana"
    )

    if pin is None:
        return False

    if not verify_pin(
        pin,
        salt,
        stored_hash
    ):

        messagebox.showwarning(
            "Ga go a Atlega",
            (
                "Leina kgotsa PIN "
                "ga e a siama."
            )
        )

        return False

    clear_active_user()

    active_teacher_id = teacher_id
    active_teacher_name = teacher_name
    active_user_role = "teacher"

    return True


# ============================================================
# TEACHER RESET LEARNER PIN
# ============================================================

def reset_learner_pin(
    learner_name,
    new_pin
):

    if not teacher_is_active():

        return (
            False,
            "not_teacher"
        )

    learner_name = learner_name.strip()

    if not learner_name:

        return (
            False,
            "empty"
        )

    if not validate_pin(
        new_pin
    ):

        return (
            False,
            "invalid_pin"
        )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM learner

        WHERE LOWER(TRIM(name))
        = LOWER(TRIM(?))

        ORDER BY id

        LIMIT 1
        """,
        (learner_name,)
    )

    result = cursor.fetchone()

    if not result:

        connection.close()

        return (
            False,
            "not_found"
        )

    learner_id = result[0]

    salt, pin_hash = hash_pin(
        new_pin
    )

    cursor.execute(
        """
        UPDATE learner

        SET
            pin_salt = ?,
            pin_hash = ?

        WHERE id = ?
        """,
        (
            salt,
            pin_hash,
            learner_id
        )
    )

    connection.commit()
    connection.close()

    return (
        True,
        "reset"
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def save_learner(name):

    if login_learner(name):

        return active_learner_id

    success, status = register_learner(
        name
    )

    if success:

        return active_learner_id

    return None


# ============================================================
# ACTIVE LEARNER
# ============================================================

def get_learner():

    return active_learner_name


def get_active_learner_id():

    return active_learner_id


def learner_is_active():

    return (
        active_user_role == "learner"
        and active_learner_id is not None
    )


# ============================================================
# ACTIVE TEACHER
# ============================================================

def get_teacher():

    return active_teacher_name


def get_active_teacher_id():

    return active_teacher_id


def teacher_is_active():

    return (
        active_user_role == "teacher"
        and active_teacher_id is not None
    )


# ============================================================
# ACTIVE USER
# ============================================================

def get_active_user_role():

    return active_user_role


def get_active_user_name():

    if active_user_role == "learner":

        return active_learner_name

    if active_user_role == "teacher":

        return active_teacher_name

    return None


def clear_active_learner():

    clear_active_user()


def clear_active_teacher():

    clear_active_user()


# ============================================================
# COMPLETE LESSON
# ============================================================

def complete_lesson(
    lesson_number
):

    if not learner_is_active():
        return False

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO lesson_progress
        (
            learner_id,
            lesson_number,
            completed
        )

        VALUES (?, ?, 1)

        ON CONFLICT(
            learner_id,
            lesson_number
        )

        DO UPDATE SET
            completed = 1
        """,
        (
            active_learner_id,
            lesson_number
        )
    )

    connection.commit()
    connection.close()

    return True


# ============================================================
# GET COMPLETED LESSONS
# ============================================================

def get_completed_lessons():

    if not learner_is_active():
        return []

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT lesson_number

        FROM lesson_progress

        WHERE learner_id = ?
        AND completed = 1

        ORDER BY lesson_number
        """,
        (
            active_learner_id,
        )
    )

    results = cursor.fetchall()

    connection.close()

    return [
        row[0]
        for row in results
    ]


# ============================================================
# RECORD ACTIVITY ATTEMPT
# ============================================================

def record_activity_attempt(
    activity_number,
    successful=False
):

    # Teachers must not create learner progress
    if not learner_is_active():
        return False

    # Only activities 1-5 are valid
    if activity_number < 1 or activity_number > TOTAL_ACTIVITIES:
        return False

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO activity_progress
        (
            learner_id,
            activity_number,
            attempts,
            completed
        )

        VALUES (?, ?, 0, 0)
        """,
        (
            active_learner_id,
            activity_number
        )
    )

    cursor.execute(
        """
        UPDATE activity_progress

        SET attempts = attempts + 1

        WHERE learner_id = ?
        AND activity_number = ?
        """,
        (
            active_learner_id,
            activity_number
        )
    )

    if successful:

        cursor.execute(
            """
            UPDATE activity_progress

            SET completed = 1

            WHERE learner_id = ?
            AND activity_number = ?
            """,
            (
                active_learner_id,
                activity_number
            )
        )

    connection.commit()
    connection.close()

    return True


# ============================================================
# GET ACTIVITY PROGRESS
# ============================================================

def get_activity_progress():

    if not learner_is_active():
        return []

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            activity_number,
            attempts,
            completed

        FROM activity_progress

        WHERE learner_id = ?

        ORDER BY activity_number
        """,
        (
            active_learner_id,
        )
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# CALCULATE ACTIVE LEARNER PROGRESS
# ============================================================

def calculate_progress():

    if not learner_is_active():
        return 0

    completed_lessons = (
        get_completed_lessons()
    )

    activities = (
        get_activity_progress()
    )

    completed_activities = sum(
        1
        for activity in activities
        if activity[2] == 1
        and 1 <= activity[0] <= TOTAL_ACTIVITIES
    )

    completed_items = (
        len(completed_lessons)
        + completed_activities
    )

    percentage = round(
        (
            completed_items
            / TOTAL_PROGRESS_ITEMS
        )
        * 100
    )

    return percentage


# ============================================================
# GET ALL LEARNERS
# ============================================================

def get_all_learners():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            l.id,
            l.name

        FROM learner AS l

        WHERE NOT EXISTS
        (
            SELECT 1

            FROM teacher AS t

            WHERE LOWER(TRIM(t.name))
            = LOWER(TRIM(l.name))
        )

        ORDER BY l.name
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# GET ALL TEACHERS
# ============================================================

def get_all_teachers():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name

        FROM teacher

        ORDER BY name
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# ONE LEARNER'S LESSON PROGRESS
# ============================================================

def get_completed_lessons_for_learner(
    learner_id
):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT lesson_number

        FROM lesson_progress

        WHERE learner_id = ?
        AND completed = 1

        ORDER BY lesson_number
        """,
        (
            learner_id,
        )
    )

    results = cursor.fetchall()

    connection.close()

    return [
        row[0]
        for row in results
    ]


# ============================================================
# ONE LEARNER'S ACTIVITY PROGRESS
# ============================================================

def get_activity_progress_for_learner(
    learner_id
):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            activity_number,
            attempts,
            completed

        FROM activity_progress

        WHERE learner_id = ?

        ORDER BY activity_number
        """,
        (
            learner_id,
        )
    )

    results = cursor.fetchall()

    connection.close()

    return results


# ============================================================
# CALCULATE ONE LEARNER'S PROGRESS
# ============================================================

def calculate_progress_for_learner(
    learner_id
):

    completed_lessons = (
        get_completed_lessons_for_learner(
            learner_id
        )
    )

    activities = (
        get_activity_progress_for_learner(
            learner_id
        )
    )

    completed_activities = sum(
        1
        for activity in activities
        if activity[2] == 1
        and 1 <= activity[0] <= TOTAL_ACTIVITIES
    )

    completed_items = (
        len(completed_lessons)
        + completed_activities
    )

    percentage = round(
        (
            completed_items
            / TOTAL_PROGRESS_ITEMS
        )
        * 100
    )

    return percentage


# ============================================================
# TEACHER - ALL LEARNER PROGRESS
# ============================================================

def get_all_learners_progress():

    learners = get_all_learners()

    progress_summary = []


    for (
        learner_id,
        learner_name
    ) in learners:

        completed_lessons = (
            get_completed_lessons_for_learner(
                learner_id
            )
        )

        activities = (
            get_activity_progress_for_learner(
                learner_id
            )
        )

        completed_activities = sum(
            1
            for activity in activities
            if activity[2] == 1
            and 1 <= activity[0] <= TOTAL_ACTIVITIES
        )

        percentage = (
            calculate_progress_for_learner(
                learner_id
            )
        )

        progress_summary.append(
            {
                "learner_id":
                    learner_id,

                "name":
                    learner_name,

                "completed_lessons":
                    len(
                        completed_lessons
                    ),

                "completed_activities":
                    completed_activities,

                "percentage":
                    percentage
            }
        )

    return progress_summary


# ============================================================
# INITIALISE DATABASE
# ============================================================

create_tables()