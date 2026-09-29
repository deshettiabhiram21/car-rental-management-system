
import os
import uuid
from urllib.parse import quote_plus

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from models import db, User, Car, Booking
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    'FLASK_SECRET_KEY',
    'change-this-secret-key'
)


# ============================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================

mysql_user = os.getenv(
    'MYSQL_USER',
    'caruser'
)

mysql_password = os.getenv(
    'MYSQL_PASSWORD',
    ''
)

mysql_host = os.getenv(
    'MYSQL_HOST',
    '127.0.0.1'
)

mysql_port = os.getenv(
    'MYSQL_PORT',
    '3306'
)

mysql_database = os.getenv(
    'MYSQL_DATABASE',
    'car_rental'
)


# MySQL connection URL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://'
    f'{mysql_user}:'
    f'{quote_plus(mysql_password)}@'
    f'{mysql_host}:'
    f'{mysql_port}/'
    f'{mysql_database}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize SQLAlchemy
db.init_app(app)


# ============================================================
# FLASK LOGIN CONFIGURATION
# ============================================================

login_manager = LoginManager()

login_manager.login_view = 'login'

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

with app.app_context():

    # Create tables if they don't already exist
    db.create_all()

    # Add sample cars only when there are no cars
    if Car.query.count() == 0:

        sample_cars = [

            Car(
                name='Maruti Alto',
                price_per_day=60
            ),

            Car(
                name='Hyundai Santro',
                price_per_day=65
            ),

            Car(
                name='Tata Tiago',
                price_per_day=70
            ),

            Car(
                name='Renault Kwid',
                price_per_day=55
            ),

            Car(
                name='Volkswagen Polo',
                price_per_day=75
            ),

            Car(
                name='Honda Amaze',
                price_per_day=80
            ),

            Car(
                name='Ford Figo',
                price_per_day=70
            ),

            Car(
                name='Maruti Celerio',
                price_per_day=60
            ),

            Car(
                name='Hyundai Grand i10',
                price_per_day=75
            ),

            Car(
                name='Tata Tigor',
                price_per_day=70
            )
        ]

        db.session.add_all(sample_cars)

        db.session.commit()


# ============================================================
# HOME / INDEX
# ============================================================

@app.route('/')
def index():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    return redirect(url_for('register'))


# ============================================================
# HOME PAGE
# ============================================================

@app.route('/home')
@login_required
def home():

    user_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'index.html',
        username=current_user.username,
        bookings=user_bookings
    )


# ============================================================
# GET ALL CARS
# ============================================================

@app.route('/api/cars')
@login_required
def get_cars():

    cars = Car.query.all()

    return jsonify({
        'cars': [
            {
                'id': car.id,
                'name': car.name,
                'price': car.price_per_day
            }
            for car in cars
        ]
    })


# ============================================================
# BOOK CAR
# ============================================================

@app.route('/api/book', methods=['POST'])
@login_required
def book_car():

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Invalid request data'
        }), 400

    car_id = data.get('car_id')
    days = data.get('days')
    kilometers = data.get('kilometers')

    # Validate input
    if not car_id or not days or not kilometers:

        return jsonify({
            'message': 'Missing booking information'
        }), 400

    try:
        car_id = int(car_id)
        days = int(days)
        kilometers = int(kilometers)

    except (ValueError, TypeError):

        return jsonify({
            'message': 'Invalid booking values'
        }), 400

    if days <= 0:

        return jsonify({
            'message': 'Days must be greater than 0'
        }), 400

    if kilometers <= 0:

        return jsonify({
            'message': 'Kilometers must be greater than 0'
        }), 400


    # Find car
    car = db.session.get(Car, car_id)

    if not car:

        return jsonify({
            'message': 'Car not found'
        }), 404


    # Calculate price
    price_per_km = 1.5

    total_price = (
        (car.price_per_day * days)
        +
        (price_per_km * kilometers)
    )


    # Generate receipt number
    receipt_number = str(uuid.uuid4())


    # Create booking
    booking = Booking(
        user_id=current_user.id,
        car_id=car_id,
        days=days,
        total_price=total_price,
        kilometers=kilometers,
        receipt_number=receipt_number
    )


    db.session.add(booking)

    db.session.commit()


    return jsonify({

        'message': 'Booking successful',

        'booking': {

            'id': booking.id,

            'car_name': car.name,

            'user_name': current_user.username,

            'days': days,

            'kilometers': kilometers,

            'total_price': total_price,

            'receipt_number': receipt_number
        }
    })


# ============================================================
# PAYMENT
# ============================================================

@app.route(
    '/payment/<int:booking_id>',
    methods=['GET', 'POST']
)
@login_required
def payment(booking_id):

    booking = db.session.get(
        Booking,
        booking_id
    )

    if not booking:

        flash('Booking not found.')

        return redirect(
            url_for('home')
        )


    # Make sure the booking belongs to current user
    if booking.user_id != current_user.id:

        flash(
            "You don't have permission to pay for this booking."
        )

        return redirect(
            url_for('home')
        )


    # Process payment
    if request.method == 'POST':

        payment_method = request.form.get(
            'payment_method'
        )

        booking.is_paid = True

        db.session.commit()

        flash(
            f'Payment successful via '
            f'{payment_method} for booking of '
            f'{booking.car.name}.'
        )

        return redirect(
            url_for('home')
        )


    return render_template(
        'payment.html',
        booking=booking
    )


# ============================================================
# CANCEL BOOKING
# ============================================================

@app.route(
    '/cancel_booking',
    methods=['GET', 'POST']
)
@login_required
def cancel_booking_page():

    if request.method == 'POST':

        receipt_number = request.form.get(
            'receipt_number'
        )


        booking = Booking.query.filter_by(
            receipt_number=receipt_number,
            user_id=current_user.id
        ).first()


        if booking:

            refund_amount = (
                booking.total_price
                if booking.is_paid
                else 0
            )


            db.session.delete(booking)

            db.session.commit()


            flash(
                f'Booking canceled successfully. '
                f'Refund amount: ${refund_amount:.2f}'
            )

            return redirect(
                url_for('home')
            )


        else:

            flash(
                'Invalid receipt number or booking not found.'
            )

            return redirect(
                url_for('cancel_booking_page')
            )


    return render_template(
        'cancel_booking.html'
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for('home')
        )


    if request.method == 'POST':

        username = request.form.get(
            'username',
            ''
        ).strip()

        password = request.form.get(
            'password',
            ''
        )


        if not username or not password:

            flash(
                'Username and password are required.'
            )

            return redirect(
                url_for('register')
            )


        # Check whether username already exists
        existing_user = User.query.filter_by(
            username=username
        ).first()


        if existing_user:

            flash(
                'Username already exists.'
            )

            return redirect(
                url_for('register')
            )


        # Hash password
        hashed_password = generate_password_hash(
            password
        )


        # Create user
        new_user = User(
            username=username,
            password=hashed_password
        )


        db.session.add(new_user)

        db.session.commit()


        flash(
            'Registration successful. Please log in.'
        )

        return redirect(
            url_for('login')
        )


    return render_template(
        'register.html'
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for('home')
        )


    if request.method == 'POST':

        username = request.form.get(
            'username',
            ''
        ).strip()

        password = request.form.get(
            'password',
            ''
        )


        # Find user
        user = User.query.filter_by(
            username=username
        ).first()


        # Check password
        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for('home')
            )


        flash(
            'Invalid username or password.'
        )


    return render_template(
        'login.html'
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Logged out successfully.'
    )

    return redirect(
        url_for('login')
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
