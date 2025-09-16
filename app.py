from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

# ---------------- Flask Config ----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session login system


# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    
    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Shows
    c.execute("""
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    
    # Seats
    c.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_id INTEGER,
            seat_number TEXT,
            is_booked INTEGER DEFAULT 0,
            FOREIGN KEY(show_id) REFERENCES shows(id)
        )
    """)
    
    # Bookings
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
    
    # Insert dummy shows + seats (only first time)
    c.execute("SELECT COUNT(*) FROM shows")
    if c.fetchone()[0] == 0:
        shows = [
            ("Avengers: Endgame", "18:00"),
            ("Inception", "21:00"),
            ("Interstellar", "15:00")
        ]
        c.executemany("INSERT INTO shows (title, time) VALUES (?, ?)", shows)

        c.execute("SELECT id FROM shows")
        show_ids = [row[0] for row in c.fetchall()]
        for show_id in show_ids:
            seats = [(show_id, f"A{i}", 0) for i in range(1, 11)]  # 10 seats per show
            c.executemany("INSERT INTO seats (show_id, seat_number, is_booked) VALUES (?, ?, ?)", seats)

    conn.commit()
    conn.close()



# ---------------- Routes ----------------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return f"Welcome {session['username']}! <a href='/logout'>Logout</a>"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("tickets.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
        finally:
            conn.close()

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("tickets.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))
@app.route("/shows")
def shows():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM shows")
    shows = c.fetchall()
    conn.close()
    return render_template("shows.html", shows=shows)


@app.route("/show/<int:show_id>")
def show_details(show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM shows WHERE id=?", (show_id,))
    show = c.fetchone()
    c.execute("SELECT * FROM seats WHERE show_id=?", (show_id,))
    seats = c.fetchall()
    conn.close()

    return render_template("show_details.html", show=show, seats=seats)


@app.route("/book/<int:seat_id>/<int:show_id>")
def book(seat_id, show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM seats WHERE id=?", (seat_id,))
    seat = c.fetchone()
    c.execute("SELECT * FROM shows WHERE id=?", (show_id,))
    show = c.fetchone()
    conn.close()

    if seat["is_booked"]:
        flash("Seat already booked!", "danger")
        return redirect(url_for("show_details", show_id=show_id))

    # Redirect to payment page
    return render_template("payment.html", seat=seat, show=show)


@app.route("/confirm_payment/<int:seat_id>/<int:show_id>", methods=["POST"])
def confirm_payment(seat_id, show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()

    # Check if already booked
    c.execute("SELECT is_booked FROM seats WHERE id=?", (seat_id,))
    if c.fetchone()[0] == 1:
        flash("Seat already booked!", "danger")
    else:
        # Mark seat booked
        c.execute("UPDATE seats SET is_booked=1 WHERE id=?", (seat_id,))
        # Save booking
        c.execute("INSERT INTO bookings (user_id, show_id, seat_id) VALUES (?, ?, ?)",
                  (session["user_id"], show_id, seat_id))
        conn.commit()
        flash("Payment successful! Seat booked 🎉", "success")

    conn.close()
    return redirect(url_for("my_bookings"))


@app.route("/mybookings")
def my_bookings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT b.id, s.seat_number, sh.title, sh.time
        FROM bookings b
        JOIN seats s ON b.seat_id = s.id
        JOIN shows sh ON b.show_id = sh.id
        WHERE b.user_id=?
    """, (session["user_id"],))
    bookings = c.fetchall()
    conn.close()

    return render_template("mybookings.html", bookings=bookings)


# ---------------- Run ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
