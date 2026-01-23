import sqlite3
from datetime import datetime
from config import DATABASE_NAME

def get_connection():
    '''
       Create a database connection 

       why function?
       1. Reusabable: every function that needs DB calls this.
       2. Single point of change: if we switch to PostgreSQL, change only here.
    '''
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    '''
       Create all tables if they dont exist.

       This is our DATA MODEL - the schema design.

       Interview term: 'DDL' ( Data Definition Language )
    '''
    conn = get_connection()
    cursor = conn.cursor()

    # Profiles table - one row per customer.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # SESSIONS table - one row per conversation.
    # profile_id links to profiles table (FOREIGN KEY)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles (id)
        )
    ''')

    # MESSAGES table - one row per chat message.
    # session_id links to sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            sender TEXT CHECK (sender IN ('user', 'bot')),
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')

    # BOOKINGS tables - scheduled consulatations.
    # Links to both profiles and sessions.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            session_id INTEGER,
            scheduled_for TIMESTAMP,
            reminder_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles (id),
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Databse initialized successfully.")

# ============ CRUD Operations ========================

def create_session(profile_id=None):
    '''
       Create a new chat session.
       
       Returns the new session ID.
       This is the 'C' in CRUD - CREATE
    '''

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO sessions (profile_id) VALUES (?)',
        (profile_id,)
    )

    session_id = cursor.lastrowid # Get the auto-generated ID
    conn.commit()
    conn.close()
    return session_id


def save_message(session_id, sender, content):
    '''
       save a message to the database.
       
       why save every message?
       1. Analytics: What questions do customers ask most?
       2: Training: could fine-tune AI on real conversations.
       3. Audit trail: required in healthcare.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO messages (session_id, sender, content) VALUES (?, ?, ?)',
        (session_id, sender, content)
    )

    conn.commit()
    conn.close()

def get_session_messages(session_id):
    '''
       Get all messages for a session.
       
       This is the 'R' in CRUD - READ
       Used to build conversation history for AI context.
    '''
    conn = get_connection()
    cursor  = conn.cursor()

    cursor.execute(
        'SELECT sender, content FROM messages WHERE session_id = ? ORDER BY created_at',
        (session_id,)
    )

    messages = cursor.fetchall()
    conn.close()
    return messages

def create_or_update_profile(email, full_name=None, phone=None):
    '''
       Create a profile or update if email exists.
       
       this is an 'UPSERT' pattern - Update or Insert
       
       Interview term: 'Idempotent operation' - can run multiple times safely.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    # First, check if profiles exists.
    cursor.execute('SELECT id FROM profiles WHERE email = ?', (email,))
    existing = cursor.fetchone()

    if existing:
        # Update existing profile.
        profile_id = existing[0]
        cursor.execute(
            'UPDATE profiles SET full_name = ?, phone = ? WHERE id = ?',
            (full_name, phone, profile_id)
        )
    else:
        # Create new profile.
        cursor.execute(
            'INSERT INTO profiles (full_name, email, phone) VALUES (?, ?, ?)',
            (full_name, email, phone)
        )
        profile_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return profile_id

def create_booking(profile_id, session_id, scheduled_for):
    '''
       Create a consultation booking.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO bookings (profile_id, session_id, scheduled_for) VALUES(?, ?, ?)',
        (profile_id, session_id, scheduled_for)
    )

    booking_id  = cursor.lastrowid
    conn.commit()
    conn.close()
    return booking_id

def get_pending_reminders():
    ''' 
       Get bookings that need reminder emails.
       
       this is a JOIN query - combining data from multiple tables!
       this is the 'E' in ETL - Extract.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            b.id,
            b.scheduled_for,
            p.full_name,
            p.email
        FROM bookings b
        JOIN profiles p ON b.profile_id = p.id
        WHERE b.reminder_sent = 0
        AND b.scheduled_for IS NOT NULL
    ''')

    reminders = cursor.fetchall()
    conn.close()
    return reminders


def mark_reminder_sent(booking_id):
    ''' Mark a booking's reminder as sent'''

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE bookings SET reminder_sent = 1 WHERE id = ?',
        (booking_id,)
    )

    conn.commit()
    conn.close()

