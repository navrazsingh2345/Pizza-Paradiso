# all the libraries that i have imported
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message  
from werkzeug.security import generate_password_hash, check_password_hash  

app = Flask(__name__, static_url_path='/static')


# Configure Flask app, database, and mail
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logininfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mehar'
db = SQLAlchemy(app)



# Define the User model for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)


# Define routes for home page
@app.route('/')  
def homelog():  
    return render_template("index1.html")


# this is for the login page of the website
@app.route('/redirected_page', methods=['POST'])
def redirected_page():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        session['username'] = username
        if user and check_password_hash(user.password, password):
            return render_template('index.html', username=username)
        else:
            return "<script>alert('Invalid username or password. Please try again.');</script>"
    else:
        return render_template('index.html')


# this code is for sign up page it stores the data of person in .db file
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username'] 
        new_password = request.form['password']
        if User.query.filter_by(username=new_username).first():
            return "<script>alert('Username already taken. Choose a different one.');</script>"
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=new_username, password=hashed_password) 
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_username 


        return render_template('index.html')
    return render_template('signup.html')  


# for redirecting to the cart page 
@app.route('/cart_summary')
def cart():
    return render_template("cart_summary.html", username=session.get('username', 'new_username'))


# for redirecting to the login page 
@app.route('/login')
def login():
    return render_template("login.html", username=session.get('username', 'new_username'))


# for redirecting back to the home page 
@app.route('/back')
def back():
    return render_template("index.html")


# for redirecting  to the review page 
@app.route('/Review')
def review():
    return render_template("Review.html")


# for redirecting  to the review page 
@app.route('/home')
def home():
    return render_template("index1.html")

# for redirecting  to the review page 
@app.route('/home1')
def home1():
    return render_template("index.html")


# Route to handle review submission
@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        username = request.form['username']
        rating = int(request.form['rating'])
        review_text = request.form['review_text']

        # Create a new Review object
        new_review = Review(username=username, rating=rating, review_text=review_text)

        # Add the new review to the database
        db.session.add(new_review)
        db.session.commit()

        # Optionally, you can return a JSON response indicating success
        return jsonify({'message': 'Review submitted successfully'})


# used to run the flask python file 
if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)



