
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# models
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

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if admin already exists to avoid duplicates
        existing_admin = User.query.filter_by(username="admin").first()
        
        if not existing_admin:
            admin_user = User(
                username="admin",
                password="admin",  # Note: For production, use hashed passwords!
                email="admin@gmail.com",  # Fixed typo from 'lid@gmail.com'
                role="admin"
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
            
    app.run(debug=True)

