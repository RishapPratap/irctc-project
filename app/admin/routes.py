# app/admin/routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Train
from app.auth.decorators import admin_api_key_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/add_train', methods=['POST'])
@admin_api_key_required  # Example custom decorator for admin-only access
def add_train():
    data = request.get_json()
    train_number = data.get('train_number')
    source = data.get('source')
    destination = data.get('destination')

    if not train_number or not source or not destination:
        return jsonify({'error': 'Missing train details'}), 400

    existing_train = Train.query.filter_by(train_number=train_number).first()
    if existing_train:
        return jsonify({'error': 'Train already exists'}), 400

    new_train = Train(train_number=train_number, source=source, destination=destination)
    db.session.add(new_train)
    db.session.commit()

    return jsonify({'message': 'Train added successfully'}), 201

@admin_bp.route('/update_seats/<train_id>', methods=['PUT'])
@admin_api_key_required
def update_seats(train_id):
    data = request.get_json()
    total_seats = data.get('total_seats')

    if not total_seats:
        return jsonify({'error': 'Missing total seats'}), 400

    train = Train.query.get(train_id)
    if not train:
        return jsonify({'error': 'Train not found'}), 404

    train.total_seats = total_seats
    db.session.commit()

    return jsonify({'message': 'Total seats updated successfully'}), 200
