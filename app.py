from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, DoctorDetail, Appointment
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hms-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- AUTHENTICATION ROUTES ---

@app.route('/')
def home():
    # CHANGE: Instead of redirecting to login, show the new Landing Page
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            
            if user.role == 'admin': return redirect(url_for('admin_dashboard'))
            if user.role == 'doctor': return redirect(url_for('doctor_dashboard'))
            if user.role == 'patient': return redirect(url_for('patient_dashboard'))
        else:
            flash("Invalid Credentials")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = 'patient' # Default registration is always patient
        
        if User.query.filter_by(username=username).first():
            flash("User already exists")
        else:
            new_user = User(username=username, password=password, email=email, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful! Please Login.")
            return redirect(url_for('login'))
            
    return render_template('register.html')

# --- ADMIN DASHBOARD LOGIC ---

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    doctors = User.query.filter_by(role='doctor').all()
    patients = User.query.filter_by(role='patient').all()
    return render_template('admin/dashboard.html', doctors=doctors, patients=patients)

@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    
    # 1. Create User Account
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    new_user = User(username=username, email=email, password=password, role='doctor')
    db.session.add(new_user)
    db.session.commit() # Commit to get the ID
    
    # 2. Add Doctor Specific Details
    dept = request.form['department']
    spec = request.form['specialization']
    exp = request.form['experience']
    
    new_profile = DoctorDetail(user_id=new_user.id, department=dept, specialization=spec, experience=exp)
    db.session.add(new_profile)
    db.session.commit()
    
    flash("New Doctor Added Successfully")
    return redirect(url_for('admin_dashboard'))

# --- DOCTOR DASHBOARD LOGIC ---

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if session.get('role') != 'doctor': return redirect(url_for('login'))
    
    doctor_id = session['user_id']
    # Get appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return render_template('doctor/dashboard.html', appointments=appointments)

@app.route('/doctor/complete_appointment/<int:id>', methods=['POST'])
def complete_appointment(id):
    # Logic for "Update Patient History" from Diagram
    appt = Appointment.query.get(id)
    appt.diagnosis = request.form['diagnosis']
    appt.prescription = request.form['prescription']
    appt.status = 'Completed'
    db.session.commit()
    flash("Patient History Updated")
    return redirect(url_for('doctor_dashboard'))

# --- PATIENT DASHBOARD LOGIC ---

@app.route('/patient/dashboard')
def patient_dashboard():
    if session.get('role') != 'patient': return redirect(url_for('login'))
    
    # Get available doctors for booking
    doctors = User.query.filter_by(role='doctor').all()
    
    # Get my past history
    my_history = Appointment.query.filter_by(patient_id=session['user_id']).all()
    
    return render_template('patient/dashboard.html', doctors=doctors, history=my_history)

@app.route('/patient/book', methods=['POST'])
def book_appointment():
    doctor_id = request.form['doctor_id']
    date_str = request.form['date'] # Input type="date"
    
    # Create Appointment
    new_appt = Appointment(
        patient_id=session['user_id'],
        doctor_id=doctor_id,
        date=datetime.strptime(date_str, '%Y-%m-%d'),
        status='Scheduled'
    )
    db.session.add(new_appt)
    db.session.commit()
    flash("Appointment Booked Successfully")
    return redirect(url_for('patient_dashboard'))
# Add these to your existing app.py

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/doctors')
def doctors():
    # We need to fetch doctors from DB to show them on the page
    all_doctors = User.query.filter_by(role='doctor').all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- INIT ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create Default Admin
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@hms.com', password='admin', role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Default Admin Created (User: admin, Pass: admin)")
    app.run(debug=True)
  