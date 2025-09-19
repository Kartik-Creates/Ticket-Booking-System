-- Users table (customers + admins)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'  -- user or admin
);

-- Shows table (movies/events)
CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    show_time TEXT NOT NULL
);

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER,
    seat_number TEXT NOT NULL,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY (show_id) REFERENCES shows(id)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    show_id INTEGER,
    seat_id INTEGER,
    status TEXT DEFAULT 'confirmed',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (show_id) REFERENCES shows(id),
    FOREIGN KEY (seat_id) REFERENCES seats(id)
);

-- Insert dummy users
INSERT INTO users (username, password, role) VALUES
('kartik', 'pass123', 'user'),
('admin', 'admin123', 'admin');

-- Insert dummy shows (3 movies)
INSERT INTO shows (title, show_time) VALUES
('Avengers: Endgame', '2025-09-20 18:00'),
('Inception', '2025-09-20 21:00'),
('Interstellar', '2025-09-21 19:00');

-- Insert 10 seats per show
-- Avengers: Endgame (id = 1)
INSERT INTO seats (show_id, seat_number) VALUES
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5');

-- Inception (id = 2)
INSERT INTO seats (show_id, seat_number) VALUES
(2, 'A1'), (2, 'A2'), (2, 'A3'), (2, 'A4'), (2, 'A5'),
(2, 'B1'), (2, 'B2'), (2, 'B3'), (2, 'B4'), (2, 'B5');

-- Interstellar (id = 3)
INSERT INTO seats (show_id, seat_number) VALUES
(3, 'A1'), (3, 'A2'), (3, 'A3'), (3, 'A4'), (3, 'A5'),
(3, 'B1'), (3, 'B2'), (3, 'B3'), (3, 'B4'), (3, 'B5');

