from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for user session management

# ---------------- Home ----------------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


# ---------------- Signup ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("db.sqlite")
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


# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("db.sqlite")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")


# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


# ---------------- Show List ----------------
@app.route("/shows")
def shows():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM shows")
    shows = c.fetchall()
    conn.close()
    return render_template("shows.html", shows=shows)


# ---------------- Seat Layout ----------------
@app.route("/seats/<int:show_id>")
def seats(show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM shows WHERE id = ?", (show_id,))
    show = c.fetchone()
    c.execute("SELECT * FROM seats WHERE show_id = ?", (show_id,))
    seats = c.fetchall()
    conn.close()
    return render_template("seats.html", show=show, seats=seats)


# ---------------- Book Seat (Confirmation Page) ----------------
@app.route("/book/<int:seat_id>/<int:show_id>")
def book(seat_id, show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM seats WHERE id = ?", (seat_id,))
    seat = c.fetchone()
    if seat["is_booked"]:
        flash("Seat already booked!", "danger")
        return redirect(url_for("seats", show_id=show_id))
    c.execute("SELECT * FROM shows WHERE id = ?", (show_id,))
    show = c.fetchone()
    conn.close()
    return render_template("payment.html", seat=seat, show=show)


# ---------------- Confirm Payment ----------------
@app.route("/confirm_payment/<int:seat_id>/<int:show_id>", methods=["POST"])
def confirm_payment(seat_id, show_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()
    c.execute("SELECT is_booked FROM seats WHERE id = ?", (seat_id,))
    if c.fetchone()[0] == 1:
        flash("Seat already booked!", "danger")
    else:
        # Update seat status
        c.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (seat_id,))
        # Create booking
        c.execute("INSERT INTO bookings (user_id, show_id, seat_id) VALUES (?, ?, ?)",
                  (session["user_id"], show_id, seat_id))
        conn.commit()
        flash("✅ Payment successful. Your seat is booked!", "success")
    conn.close()
    return redirect(url_for("mybookings"))


# ---------------- My Bookings ----------------
@app.route("/mybookings")
def mybookings():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT s.seat_number, sh.title, sh.time
        FROM bookings b
        JOIN seats s ON b.seat_id = s.id
        JOIN shows sh ON b.show_id = sh.id
        WHERE b.user_id = ?
    """, (session["user_id"],))
    bookings = c.fetchall()
    conn.close()
    return render_template("mybookings.html", bookings=bookings)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
