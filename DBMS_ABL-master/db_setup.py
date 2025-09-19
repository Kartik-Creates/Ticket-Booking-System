import sqlite3

def setup_database():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    # Users Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Shows Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    # Seats Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0,
            FOREIGN KEY(show_id) REFERENCES shows(id)
        )
    """)

    # Bookings Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            show_id INTEGER,
            seat_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(show_id) REFERENCES shows(id),
            FOREIGN KEY(seat_id) REFERENCES seats(id)
        )
    """)

    # Seed sample data only once
    c.execute("SELECT COUNT(*) FROM shows")
    if c.fetchone()[0] == 0:
        shows = [
            ("Avengers: Endgame", "6:00 PM"),
            ("Inception", "9:00 PM"),
            ("Interstellar", "3:00 PM")
        ]
        c.executemany("INSERT INTO shows (title, time) VALUES (?, ?)", shows)

        # Insert 10 seats per show
        c.execute("SELECT id FROM shows")
        show_ids = [row[0] for row in c.fetchall()]
        for show_id in show_ids:
            seats = [(show_id, f"A{i}", 0) for i in range(1, 11)]  # A1–A10
            c.executemany("INSERT INTO seats (show_id, seat_number, is_booked) VALUES (?, ?, ?)", seats)

    conn.commit()
    conn.close()
    print("✅ Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()
