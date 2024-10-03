from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuring SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Book model for the library
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)  # Roll number column
    book_name = db.Column(db.String(100), nullable=False)  # Book name column
    serial_number = db.Column(db.String(50), nullable=False)  # New column for serial number
    issue_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    deadline_date = db.Column(db.Date, nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Home page (listing all books)
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        student_name = request.form['student_name']
        roll_number = request.form['roll_number']
        book_name = request.form['book_name']
        serial_number = request.form['serial_number']  # Get serial number from the form
        issue_date = request.form['issue_date']
        deadline_date = request.form['deadline_date']

        # Convert issue and deadline date to datetime format
        issue_date = datetime.strptime(issue_date, '%Y-%m-%d')
        deadline_date = datetime.strptime(deadline_date, '%Y-%m-%d')

        new_book = Book(student_name=student_name, roll_number=roll_number, book_name=book_name, 
                        serial_number=serial_number, issue_date=issue_date, deadline_date=deadline_date)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_book.html')

# Route to delete a book
@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
