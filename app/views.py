from functools import wraps
from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, session, flash
from app.models import User

# Define the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('You need to log in first')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Define the route for the user main content page
@app.route('/user-main-content-page')
@login_required
def user_main_content_page():
    return render_template("user_main_content.html")

# Define the route for registering a user
@app.route('/register-user', methods=['POST'])
def register_user():
    form = request.form
    user = User(    
        name=form['name'],
        email=form['email-address'],
        role=form['role']
    )   
    user.set_password(form['password'])
    db.session.add(user)
    db.session.commit()
    return "Successfully registered"

# Define the route for validating user registration
@app.route('/validate-registration', methods=['POST'])
def validate_registration():
    email = request.json.get('email')  # Assuming the email is sent in JSON format
    user = User.query.filter_by(email=email).first()
    if user:
        # User with provided email already exists
        return jsonify({'user_exists': True})
    else:
        # User with provided email does not exist
        return jsonify({'user_exists': False})

# Define the route for user login
@app.route('/login-user', methods=['POST'])
def login_user():
    form = request.form
    user = User.query.filter_by(email=form['email-address']).first()
    if not user:
        flash("User does not exist")
        return redirect(url_for("index"))
    if user.check_password(form['password']):
        session['email'] = user.email  # Storing email in session
        return redirect(url_for('user_main_content_page'))
    else:
        flash('Password was incorrect')
        return redirect(url_for('index'))

# Define the route for user logout
@app.route('/logout-user', methods=['POST', 'GET'])
def logout_user():
    session.pop('email', None)  # Removing email from session
    return redirect(url_for('index'))

# Define the route for the main login page
@app.route('/main-login-page')
def login_page():
    return render_template("main_login_page.html") 
@app.route('/')
def index():
    return render_template('main.html')