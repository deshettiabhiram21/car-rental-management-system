-- ============================================================
-- Car Rental System - MySQL Database Setup
-- ============================================================

CREATE DATABASE IF NOT EXISTS car_rental
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE car_rental;

-- Disable foreign-key checks while recreating tables
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;


-- ============================================================
-- USERS TABLE
-- utf8mb4_bin makes username comparison case-sensitive
-- so 'abhi' and 'ABHI' are treated as different usernames.
-- ============================================================

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,

    username VARCHAR(80)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_bin
        NOT NULL,

    password VARCHAR(200) NOT NULL,

    PRIMARY KEY (id),

    UNIQUE KEY uq_users_username (username)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- CARS TABLE
-- ============================================================

CREATE TABLE cars (
    id INT NOT NULL AUTO_INCREMENT,

    name VARCHAR(100) NOT NULL,

    price_per_day FLOAT NOT NULL,

    PRIMARY KEY (id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- BOOKINGS TABLE
-- ============================================================

CREATE TABLE bookings (
    id INT NOT NULL AUTO_INCREMENT,

    user_id INT NOT NULL,

    car_id INT NOT NULL,

    days INT NOT NULL,

    total_price FLOAT NOT NULL,

    kilometers INT NOT NULL,

    is_paid BOOLEAN DEFAULT FALSE,

    receipt_number VARCHAR(36) NOT NULL,

    PRIMARY KEY (id),

    UNIQUE KEY uq_bookings_receipt (receipt_number),

    CONSTRAINT fk_booking_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT fk_booking_car
        FOREIGN KEY (car_id)
        REFERENCES cars(id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- USERS DATA
-- ============================================================

INSERT INTO users
(id, username, password)
VALUES

(1,
'abhi',
'scrypt:32768:8:1$aQbpytQs7MEiMUyP$ef65226d590a1891cd2edb36870d1ea79ff6a45a2e67292af449ff610906a07f81f1580ccc649128a176a1eb03caf4c1a754c41e0509c3afeec1ac32cc6845c7'),

(2,
'ABHI',
'scrypt:32768:8:1$aQIjfRauSB9hGllm$241d3f66a8a25eefdf0aac8d540de5238db2dd3a5d20a9569268a490b6b5f70d1fd20f2daf26a0fd7dc5d3bc12a240e78311bdee2e4a4f90a00a52fa3b0f5a8c'),

(3,
'abhiram',
'scrypt:32768:8:1$7kaC1swhxYjQLNjA$93b0e442afb9129704c1b56bdea303fe52f87da9dc8e353f59490f2794ec831c0ebdd0686d992090ac3fb7e01da146f290aeb2742e7398e81ee2dd291211473a'),

(4,
'Abhiram',
'scrypt:32768:8:1$LNMujnlJsxMFSUrI$170cab3e869fea5387f07401910c7bde92016ca75f3740f19c53ef3910a89f1af40e4872b730ce30866b6adaf5866dee94655fa42e3a2eebd65af43544dae776'),

(5,
'adithya',
'scrypt:32768:8:1$cVpL4iMwTJdJEcyG$b36d4670ecb8a9e2d2ed2973f01098f13ba6fb8806e351788bc75f8c5435ec7069799f801a8630fad07336d428e27c2100585e9a9c6499340b2886c9bde77329');

ALTER TABLE users AUTO_INCREMENT = 6;


-- ============================================================
-- CARS DATA
-- ============================================================

INSERT INTO cars
(id, name, price_per_day)
VALUES

(1, 'Maruti Alto', 60.0),

(2, 'Hyundai Santro', 65.0),

(3, 'Tata Tiago', 70.0),

(4, 'Renault Kwid', 55.0),

(5, 'Volkswagen Polo', 75.0),

(6, 'Honda Amaze', 80.0),

(7, 'Ford Figo', 70.0),

(8, 'Maruti Celerio', 60.0),

(9, 'Hyundai Grand i10', 75.0),

(10, 'Tata Tigor', 70.0);

ALTER TABLE cars AUTO_INCREMENT = 11;


-- ============================================================
-- BOOKINGS DATA
-- ============================================================

INSERT INTO bookings
(id, user_id, car_id, days, total_price, kilometers, is_paid, receipt_number)
VALUES

(
1,
2,
1,
2,
870.0,
500,
1,
'62490a9a-f6ab-48e5-8147-70ece2017dba'
),

(
5,
3,
9,
2,
450.0,
200,
1,
'09c1d146-c23c-4682-8c5a-cfef00e7c48d'
),

(
6,
3,
6,
2,
610.0,
300,
1,
'4c15b62a-ba12-4c96-ba18-f2878c93309e'
),

(
7,
3,
9,
10,
15750.0,
10000,
1,
'8f05e20b-be3f-4935-85b6-d34a292662c7'
),

(
8,
3,
1,
3,
780.0,
400,
0,
'cb349175-a3ff-4534-b574-af5490a8063c'
);

ALTER TABLE bookings AUTO_INCREMENT = 9;


-- ============================================================
-- DONE
-- ============================================================

SELECT 'Database setup completed successfully!' AS message;