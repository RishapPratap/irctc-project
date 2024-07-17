# app/models.py

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(128))  # Add token field for token-based authentication
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')  # Relationship with Booking model

    def __repr__(self):
        return f'<User {self.username}>'

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String(10), index=True, unique=True)
    source = db.Column(db.String(64), index=True)
    destination = db.Column(db.String(64), index=True)
    total_seats = db.Column(db.Integer, default=100)
    bookings = db.relationship('Booking', backref='train', lazy='dynamic')

    def __repr__(self):
        return f'<Train {self.train_number} from {self.source} to {self.destination}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))
    seat_number = db.Column(db.Integer)

    def __repr__(self):
        return f'<Booking {self.id} by User {self.user_id} for Train {self.train_id}>'
