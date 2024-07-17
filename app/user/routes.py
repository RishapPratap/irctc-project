# app/user/routes.py

from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Train, Booking
from app.auth.decorators import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/trains', methods=['GET'])
def get_trains():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({'error': 'Missing source or destination'}), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()
    if not trains:
        return jsonify({'error': 'No trains found for this route'}), 404

    train_data = [{'train_number': train.train_number, 'source': train.source, 'destination': train.destination} for train in trains]

    return jsonify(train_data), 200

@user_bp.route('/book_seat', methods=['POST'])
@token_required
def book_seat():
    data = request.get_json()
    train_number = data.get('train_number')
    seat_number = data.get('seat_number')

    if not train_number or not seat_number:
        return jsonify({'error': 'Missing train number or seat number'}), 400

    train = Train.query.filter_by(train_number=train_number).first()
    if not train:
        return jsonify({'error': 'Train not found'}), 404

    if train.total_seats <= 0:
        return jsonify({'error': 'No seats available on this train'}), 400

    existing_booking = Booking.query.filter_by(train_id=train.id, seat_number=seat_number).first()
    if existing_booking:
        return jsonify({'error': 'Seat already booked'}), 400

    booking = Booking(user_id=request.user.id, train_id=train.id, seat_number=seat_number)
    db.session.add(booking)
    db.session.commit()

    train.total_seats -= 1
    db.session.commit()

    return jsonify({'message': 'Seat booked successfully'}), 201

@user_bp.route('/my_bookings', methods=['GET'])
@token_required
def get_user_bookings():
    bookings = Booking.query.filter_by(user_id=request.user.id).all()
    if not bookings:
        return jsonify({'message': 'No bookings found for this user'}), 404

    booking_data = [{
        'booking_id': booking.id,
        'train_number': booking.train.train_number,
        'source': booking.train.source,
        'destination': booking.train.destination,
        'seat_number': booking.seat_number
    } for booking in bookings]

    return jsonify(booking_data), 200
