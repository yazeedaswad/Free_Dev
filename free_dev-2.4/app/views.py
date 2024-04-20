from functools import wraps
from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, session, flash, jsonify, request, send_from_directory
from app.models import User, TechnicalSkill, UserRole
from werkzeug.utils import secure_filename
import os

# Define the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('You need to log in first')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile-page')
@login_required
def profile_page():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('login_page'))
    return render_template("profile_page.html", user=user)


@app.route('/update-profile-page')
@login_required
def update_profile_page():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('login_page'))
    # Make sure skills and roles are loaded:
    user.skills = TechnicalSkill.query.filter_by(user_id=user.id).all()
    user.roles = UserRole.query.filter_by(user_id=user.id).all()
    return render_template("update_profilepage.html", user=user)

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
        return redirect(url_for('profile_page'))
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








#new
@app.route('/add-technical-skill', methods=['POST'])
@login_required
def add_technical_skill():
    user = User.query.filter_by(email=session['email']).first()
    skill_name = request.form['name']
    skill_type = request.form['skill_type']

    # Check for existing skill
    existing_skill = TechnicalSkill.query.filter_by(user_id=user.id, name=skill_name, skill_type=skill_type).first()
    if existing_skill:
        return jsonify({'status': 'error', 'message': 'Skill already added'}), 409

    technical_skill = TechnicalSkill(
        user_id=user.id,
        name=skill_name,
        rating=int(request.form['rating']),
        skill_type=skill_type  # 'language' or 'framework'
    )
    db.session.add(technical_skill)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Technical skill added successfully'}), 200








#new
@app.route('/add-role', methods=['POST'])
@login_required
def add_role():
    user = User.query.filter_by(email=session['email']).first()
    role_name = request.form['role_name']

    # Check for existing role
    existing_role = UserRole.query.filter_by(user_id=user.id, role_name=role_name).first()
    if existing_role:
        return jsonify({'status': 'error', 'message': 'Role already added'}), 409

    new_role = UserRole(
        user_id=user.id,
        role_name=role_name,
        exp_years=int(request.form['exp_years'])
    )
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Role {role_name} added successfully'}), 200


#new
@app.route('/profile-data', methods=['GET'])
@login_required
def profile_data():
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    skills = TechnicalSkill.query.filter_by(user_id=user.id).all()
    roles = UserRole.query.filter_by(user_id=user.id).all()

    skills_data = [{'name': skill.name, 'rating': skill.rating, 'type': skill.skill_type} for skill in skills]
    roles_data = [{'role_name': role.role_name, 'exp_years': role.exp_years} for role in roles]

    return jsonify({'skills': skills_data, 'roles': roles_data}), 200

#new
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # for example, 16 megabytes
#new
UPLOAD_FOLDER = r'H:\Sophomore\4th_Sem\COMP202\free_dev-2.3\app\static\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#new
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#new
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#new
# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
#new
@app.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        flash('No file part')
        return redirect(request.referrer)
    file = request.files['photo']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.referrer)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            user = User.query.filter_by(email=session['email']).first()
            # Update the profile_photo_url to be relative to the static directory
            user.profile_photo_url = url_for('static', filename='uploads/' + filename)
            db.session.commit()
            return redirect(url_for('profile_page'))
        except Exception as e:
            flash('Failed to save file, error: {}'.format(e))
            return redirect(request.referrer)
    else:
        flash('Invalid file type')
        return redirect(request.referrer)
    

#new
@app.route('/delete-skill', methods=['POST'])
@login_required
def delete_skill():
    skill_id = request.json.get('id')
    skill = TechnicalSkill.query.get(skill_id)
    if skill:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Skill deleted successfully'}), 200
    return jsonify({'status': 'error', 'message': 'Skill not found'}), 404


#new
@app.route('/delete-role', methods=['POST'])
@login_required
def delete_role():
    role_id = request.json.get('id')
    role = UserRole.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Role deleted successfully'}), 200
    return jsonify({'status': 'error', 'message': 'Role not found'}), 404    


    