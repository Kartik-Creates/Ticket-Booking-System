Ticket Booking System (Flask + SQLite)

A simple Ticket Booking System built using Flask and SQLite.
Users can Signup/Login, view available movies/shows, select seats, and confirm bookings.
All user data and bookings are stored in the database.

Features

User Signup & Login (Session-based authentication)

Logout functionality

View available shows/movies

View seats for a selected show

Seat booking with availability check

Booking stored in SQLite database

User can view their bookings (My Bookings)

Prevents booking already booked seats

🛠 Tech Stack

Python

Flask

SQLite

HTML (Jinja Templates)

📂 Project Structure
Ticket-Booking-System/
│
├── app.py
├── tickets.db
├── schema.sql
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── shows.html
│   ├── show_details.html
│   ├── payment.html
│   ├── mybookings.html
│
└── static/   (optional)

Database Tables
users

Stores user credentials.

Column	Type
id	INTEGER (PK)
username	TEXT (unique)
password	TEXT
shows

Stores movies/shows.

Column	Type
id	INTEGER (PK)
title	TEXT
show_time	TEXT
seats

Stores seats for each show.

Column	Type
id	INTEGER (PK)
show_id	INTEGER (FK)
seat_number	TEXT
is_booked	INTEGER (0/1)
bookings

Stores confirmed bookings.

Column	Type
id	INTEGER (PK)
user_id	INTEGER (FK)
show_id	INTEGER (FK)
seat_id	INTEGER (FK)
status	TEXT (default confirmed)
🚀 How to Run the Project
1️⃣ Install Python dependencies

Run this in terminal:

pip install flask

2️⃣ Run the Flask App
python app.py

3️⃣ Open in Browser

Go to:

http://127.0.0.1:5000/

Booking Flow

Signup / Login

View Shows (/shows)

Click a show → view seats (/show/<show_id>)

Click seat → goes to payment page

Confirm payment → booking stored in database

View bookings in My Bookings

 Testing Database (Optional)

You can inspect your database using:

Option 1: DB Browser for SQLite (Recommended)

Open tickets.db in DB Browser and check tables:

users

shows

seats

bookings

Option 2: Terminal
sqlite3 tickets.db
.tables
SELECT * FROM users;
SELECT * FROM shows;
SELECT * FROM seats;
SELECT * FROM bookings;

 Notes / Limitations

Passwords are stored as plain text (not secure for real-world apps).

No admin panel (shows/seats are dummy or manually inserted).

Payment is dummy (only confirmation button).

 Future Improvements (Optional)

Password hashing (bcrypt)

Real payment gateway integration

Multi-seat booking in one transaction

Admin panel to add shows and seats

Better UI with Bootstrap

Cancel booking feature

👨‍💻 Author

Built by Kartik using Flask & SQLite.
