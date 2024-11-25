from datetime import datetime
from flask_login import UserMixin
from flask_mongoengine import MongoEngine
from cultivaid import app , db

# Initialize MongoEngine
class Payment(db.Document):
    user = db.ReferenceField('User', required=True)
    amount = db.FloatField(required=True)
    currency = db.StringField(default='USD', max_length=3)
    status = db.StringField(default='pending')  # pending, completed, failed, refunded
    stripe_payment_id = db.StringField(unique=True, required=True)
    service_booking = db.ReferenceField('ServiceBooking')
    equipment_rental = db.ReferenceField('EquipmentRental')
    created_at = db.DateTimeField(default=datetime.utcnow)
    
    def __repr__(self):
        return f'Payment of {self.amount} {self.currency} for {self.status}'
# User model
class User(db.Document,UserMixin):
    name = db.StringField(required=True, max_length=100)
    email = db.EmailField(required=True, unique=True, max_length=120)
    phone_number = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True, max_length=60)
    created_at = db.DateTimeField(default=datetime.utcnow)
    is_admin = db.BooleanField(default=False)

    # Relationships
    service_bookings = db.ListField(db.ReferenceField('ServiceBooking'))
    equipment_rentals = db.ListField(db.ReferenceField('EquipmentRental'))
    payments = db.ListField(db.ReferenceField('Payment'))

    def __repr__(self):
        return f'{self.name} {self.email}'

# Service model
class Service(db.Document):
    name = db.StringField(required=True, max_length=100)
    description = db.StringField(required=True)
    price = db.FloatField(required=True)
    location = db.StringField(required=True, max_length=200)

    # Relationships
    bookings = db.ListField(db.ReferenceField('ServiceBooking'))

    def __repr__(self):
        return f'{self.name} {self.description}'

# Equipment model
class Equipment(db.Document):
    name = db.StringField(required=True, max_length=100)
    description = db.StringField(required=True)
    daily_rate = db.FloatField(required=True)

    # Relationships
    rentals = db.ListField(db.ReferenceField('EquipmentRental'))

    def __repr__(self):
        return f'{self.name} {self.description}'

# ServiceBooking model
class ServiceBooking(db.Document):
    user = db.ReferenceField(User, required=True)
    service = db.ReferenceField(Service, required=True)
    booking_date = db.DateTimeField(required=True)
    status = db.StringField(default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.DateTimeField(default=datetime.utcnow)

    # Payment relationship
    payment = db.ReferenceField('Payment', reverse_delete_rule=db.CASCADE)

    def __repr__(self):
        return f'Booking for {self.service.name} on {self.booking_date} with status {self.status}'

# EquipmentRental model
class EquipmentRental(db.Document):
    user = db.ReferenceField(User, required=True)
    equipment = db.ReferenceField(Equipment, required=True)
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField(required=True)
    quantity = db.IntField(default=1, required=True)
    status = db.StringField(default='pending')  # pending, active, returned, cancelled
    total_cost = db.FloatField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)

    # Payment relationship
    payment = db.ReferenceField('Payment', reverse_delete_rule=db.CASCADE)

    def __repr__(self):
        return f'{self.start_date} to {self.end_date} for {self.quantity} {self.equipment.name}'


