# The Database (The Brain)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin # Helps with login management

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'admin', 'doctor', 'patient'
    
    # Link to Doctor Details (if role is doctor)
    doctor_profile = db.relationship('DoctorDetail', back_populates='user', uselist=False)
    
    # Link to Patient History (if role is patient)
    appointments = db.relationship('Appointment', foreign_keys='Appointment.patient_id', back_populates='patient')

class DoctorDetail(db.Model):
    __tablename__ = 'doctor_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100)) # From diagram
    experience = db.Column(db.Integer)         # From diagram
    
    user = db.relationship('User', back_populates='doctor_profile')
    availabilities = db.relationship('Availability', back_populates='doctor')

class Availability(db.Model):
    """To handle the time slots shown in Doctor's Dashboard"""
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_details.id'))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    
    doctor = db.relationship('DoctorDetail', back_populates='availabilities')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Completed, Cancelled
    
    # Medical Record (Diagnosis/Prescription)
    diagnosis = db.Column(db.String(500))           # From diagram (Patient History)
    prescription = db.Column(db.String(500))        # From diagram
    
    patient = db.relationship('User', foreign_keys=[patient_id], back_populates='appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id])
