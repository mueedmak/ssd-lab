from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define database model
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'{self.sno} - {self.firstname}'

# Home route - Display all records
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        
        # Create new student instance
        student = Student(firstname=firstname, lastname=lastname, 
                         email=email, phone=phone)
        
        # Add to database
        db.session.add(student)
        db.session.commit()
    
    # Get all students from database
    allStudents = Student.query.all()
    return render_template('index.html', allStudents=allStudents)

# Home page route
@app.route('/home')
def home():
    return "Welcome to Home Page!"

# Delete route
@app.route('/delete/<int:sno>')
def delete(sno):
    student = Student.query.filter_by(sno=sno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

# Update route
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        
        # Fetch and update student
        student = Student.query.filter_by(sno=sno).first()
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.phone = phone
        
        db.session.commit()
        return redirect('/')
    
    # Get student details for the form
    student = Student.query.filter_by(sno=sno).first()
    return render_template('update.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)