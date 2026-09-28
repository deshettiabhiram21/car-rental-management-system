# Car Rental System - MySQL on Fedora

This version of the Car Rental System uses **MySQL** instead of SQLite. The Flask application connects to MySQL through **PyMySQL** and **Flask-SQLAlchemy**.

## 1. Install MySQL on Fedora

```bash
sudo dnf install mysql-server
sudo systemctl enable --now mysqld
```

Check the MySQL service:

```bash
sudo systemctl status mysqld
```

## 2. Create the Project Database and User

Open MySQL:

```bash
sudo mysql
```

Run:

```sql
CREATE DATABASE car_rental
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER 'caruser'@'localhost'
IDENTIFIED BY '<your-mysql-password>';

GRANT ALL PRIVILEGES ON car_rental.*
TO 'caruser'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

If the `caruser` account already exists, use:

```sql
ALTER USER 'caruser'@'localhost'
IDENTIFIED BY '<your-mysql-password>';

FLUSH PRIVILEGES;
```

## 3. Install Python Dependencies

Go to the backend directory:

```bash
cd "car rent/backend"
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## 4. Import the Existing Database Data

The project contains an SQL file with the existing:

* 5 users
* 10 cars
* 5 bookings

The SQL file is located at:

```text
car rent/mysql_setup.sql
```

From the `backend` directory, run:

```bash
mysql -u caruser -p car_rental < ../mysql_setup.sql
```

Enter the MySQL password that you configured for `caruser`.

The SQL file creates:

```text
car_rental
├── users
├── cars
└── bookings
```

## 5. Start the Application

Make sure the virtual environment is active:

```bash
source venv/bin/activate
```

Set the MySQL credentials as environment variables:

```bash
export MYSQL_USER=caruser
export MYSQL_PASSWORD='<your-mysql-password>'
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_DATABASE=car_rental
```

Set a Flask secret key:

```bash
export FLASK_SECRET_KEY='<your-random-secret-key>'
```

Start the application:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

## 6. MySQL Configuration

The Flask application reads the following environment variables:

| Variable           | Purpose              |
| ------------------ | -------------------- |
| `MYSQL_USER`       | MySQL username       |
| `MYSQL_PASSWORD`   | MySQL password       |
| `MYSQL_HOST`       | MySQL server host    |
| `MYSQL_PORT`       | MySQL server port    |
| `MYSQL_DATABASE`   | MySQL database name  |
| `FLASK_SECRET_KEY` | Flask session secret |

Example:

```bash
export MYSQL_USER=caruser
export MYSQL_PASSWORD='<your-mysql-password>'
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_DATABASE=car_rental
export FLASK_SECRET_KEY='<your-random-secret-key>'

python app.py
```

## 7. Verify the MySQL Database

Connect to MySQL:

```bash
mysql -u caruser -p car_rental
```

Check the tables:

```sql
SHOW TABLES;
```

Expected tables:

```text
bookings
cars
users
```

Check the number of records:

```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM cars;
SELECT COUNT(*) FROM bookings;
```

Expected values:

```text
users     → 5
cars      → 10
bookings  → 5
```

Exit MySQL:

```sql
EXIT;
```

## 8. SQLite

The original project used SQLite.

The old database:

```text
instance/car_rental.db
```

is no longer used by the application.

The current application uses:

```text
Flask
   ↓
Flask-SQLAlchemy
   ↓
PyMySQL
   ↓
MySQL
   ↓
car_rental
```

## 9. DevOps Deployment

This project is intended to be extended with the following DevOps workflow:

```text
GitHub
   ↓
Jenkins
   ↓
CI/CD Pipeline
   ↓
Docker
   ↓
Docker Compose
   ↓
Kubernetes
   ↓
Car Rental Application
```

Database credentials should be provided through environment variables, Docker secrets, Jenkins credentials, or Kubernetes Secrets rather than committed to GitHub.
