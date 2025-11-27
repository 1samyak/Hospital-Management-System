from app import db
from datetime import datetime
class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'admin', 'doctor', 'patient'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    department= db.relationship('Department',back_populate ="doctors")
class Department(db.Model):
    _tablename_ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    doctors = db.relationship('User', back_populates='department')
class Appointment(db.Model):
    _tablename_ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., 'scheduled', 'completed', 'canceled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Treatment(db.Model):
    _tablename_ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    prescribed_medication = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)