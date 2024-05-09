from functools import wraps
from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, session, flash, jsonify,send_from_directory,make_response
from app.models import User, TechnicalSkill, UserRole, JobPosting, Notification
from werkzeug.utils import secure_filename
import os
from flask import flash, redirect, url_for, session
from .models import Follow, User, db

# Define the login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('You need to log in first')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function









#changed this function
@app.route('/profile-page', defaults={'user_id': None})
@app.route('/profile-page/<int:user_id>', methods=['GET'])
@login_required
def profile_page(user_id):
    # Convert user_id to int if it is not None
    user_id = int(user_id) if user_id is not None else None

    # Find user based on user_id or session user
    current_user_id = session.get('user_id')
    if user_id is None or user_id == current_user_id:
        user = User.query.filter_by(id=current_user_id).first()
        is_self_view = True  # Viewing own profile
    else:
        user = User.query.get(user_id)
        is_self_view = False  # Viewing another user's profile

    if not user:
        flash("User not found", 'error')
        return redirect(url_for('index'))

    # Determine follow status
    is_following = False
    if not is_self_view:
        is_following = Follow.query.filter_by(follower_id=current_user_id, followed_id=user.id).first() is not None
        print(f'Follow status between user {current_user_id} and {user_id}: {is_following}')

    # Fetch notifications if viewing own profile
    notifications = Notification.query.filter_by(recipient_id=user.id, read=False).all() if is_self_view else []

    # Fetch followed freelancers if user is an employer and viewing their own profile
    followed_freelancers = []
    if user.role == 'employer' and is_self_view:
        followed_freelancers = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user.id).all()

    template = "job_postings_emp.html" if user.role == 'employer' and is_self_view else "profile_page.html"
    return render_template(template, user=user, notifications=notifications, followed_freelancers=followed_freelancers, is_following=is_following)



@app.route('/update-profile-page', methods=['GET', 'POST'])
@login_required
def update_profile_page():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found", 'error')
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        # Assuming the form data contains fields named 'name', 'role', etc.
        user.name = request.form.get('name')
        user.role = request.form.get('role')
        # ... more fields to be updated ...

        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile_page'))

    # Make sure skills and roles are loaded for GET requests:
    user.skills = TechnicalSkill.query.filter_by(user_id=user.id).all()
    user.roles = UserRole.query.filter_by(user_id=user.id).all()

    return render_template("update_profilepage.html", user=user)
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

# This is where the role should be set in the session.
@app.route('/login-user', methods=['POST'])
def login_user():
    form = request.form
    user = User.query.filter_by(email=form['email-address']).first()
    if user and user.check_password(form['password']):
        session['user_id'] = user.id
        session['email'] = user.email
        session['role'] = user.role  # Ensure this line is setting the role correctly.
        return redirect(url_for('profile_page'))
    else:
        flash('Invalid login credentials')
        return redirect(url_for('login_page'))
    
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


@app.route('/jobpostings')
@login_required
def job_postings():
    user_id = session.get('user_id')
    
    # Retrieve the employer's job postings using the ID
    employer_job_postings = JobPosting.query.filter_by(employer_id=user_id).all()

    # Retrieve followed freelancers
    followed_freelancers = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    
    # Render the template with the employer's job postings and followed freelancers
    return render_template('job_postings_emp.html', job_postings=employer_job_postings, followed_freelancers=followed_freelancers)

from datetime import datetime

@app.route('/create-job-posting', methods=['POST'])
@login_required
def create_job_posting():
    # Get the logged-in user's ID from the session
    user_id = session.get('user_id')

    # Get the user's role from the database using the ID
    user = User.query.filter_by(id=user_id).first()

    # Check if the user exists and is an employer
    if not user or user.role != 'employer':
        flash('Only employers can create job postings')
        return redirect(url_for('user_main_content_page'))

    # Extract form data
    form = request.form
    title = form.get('jobTitle')
    project_type = form.get('projectType')
    skills_required = form.get('skillsRequired')
    
    # Convert deadline to a Python date object
    deadline_str = form.get('deadline')
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

    salary_min = float(form.get('salaryMin'))
    salary_max = float(form.get('salaryMax'))
    description = form.get('description')

    # Create a new JobPosting instance
    job_posting = JobPosting(
        title=title,
        project_type=project_type,
        skills_required=skills_required,
        deadline=deadline,
        salary_min=salary_min,
        salary_max=salary_max,
        description=description,
        employer_id=user.id  # Connect the job posting to the employer
    )

    # Add the job posting to the database
    db.session.add(job_posting)
    db.session.commit()

    # Flash a success message and redirect to the user main content page
    flash('Job posting created successfully')
    return redirect(url_for('job_postings'))

@app.route('/delete-job-posting/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job_posting(job_id):
    # Get the job posting by ID
    job_posting = JobPosting.query.get(job_id)
    
    if job_posting:
        # Check if the logged-in user is the employer of the job posting
        user_id = session.get('user_id')
        if job_posting.employer_id == user_id:
            # Remove the job posting from the database
            db.session.delete(job_posting)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    else:
        return jsonify({'error': 'Job posting not found'}), 404


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


@app.route('/profile-data', methods=['GET'])
def profile_data():
    email = request.args.get('email')
    if not email:
        return jsonify({'status': 'error', 'message': 'No email provided'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    skills = TechnicalSkill.query.filter_by(user_id=user.id).all()
    roles = UserRole.query.filter_by(user_id=user.id).all()

    skills_data = [{'name': skill.name, 'rating': skill.rating, 'type': skill.skill_type} for skill in skills]
    roles_data = [{'role_name': role.role_name, 'exp_years': role.exp_years} for role in roles]

    return jsonify({'skills': skills_data, 'roles': roles_data}), 200


app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # for example, 16 megabytes

UPLOAD_FOLDER = r'H:\Sophomore\4th_Sem\COMP202\free_dev-merged\app\uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if the filename has one of the allowed extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#new
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


#new/changed this
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
            user.profile_photo_url = url_for('uploaded_file', filename=filename)  # Use the new route
            db.session.commit()
            flash('Profile photo updated successfully!')
            return redirect(url_for('profile_page'))
        except Exception as e:
            flash(f'Failed to save file, error: {e}')
            return redirect(request.referrer)
    else:
        flash('Invalid file type')
        return redirect(request.referrer)
    


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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    users_by_name_email = User.query.filter(
        (User.name.ilike(f'%{query}%')) |
        (User.email.ilike(f'%{query}%'))
    ).all()

    # Search by technical skills
    users_by_skills = User.query.join(TechnicalSkill).filter(
        TechnicalSkill.name.ilike(f'%{query}%')
    ).all()

    # Search by roles
    users_by_roles = User.query.join(UserRole).filter(
        UserRole.role_name.ilike(f'%{query}%')
    ).all()

    # Combine unique users from all queries
    # Utilizing a dictionary to map user IDs to user objects, which inherently removes duplicates
    found_users = {user.id: user for user in users_by_name_email + users_by_skills + users_by_roles}.values()

    job_postings = JobPosting.query.filter(
        db.or_(
            JobPosting.title.ilike(f'%{query}%'),
            JobPosting.project_type.ilike(f'%{query}%'),
            JobPosting.skills_required.ilike(f'%{query}%'),
            JobPosting.description.ilike(f'%{query}%')
        )
    ).all()

    return render_template('search_results.html', query=query, users=found_users, job_postings=job_postings)


'''
@app.route('/public-profile/<email>')
def public_profile(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('index'))
    return render_template("public_profile_page.html", user=user)
    '''


#changed this function
@app.route('/public-profile/<email>')
@login_required  # Ensuring the user is logged in to follow/unfollow and view detailed public profiles
def public_profile(email):
    current_user_id = session.get('user_id')  # Get the current logged-in user's ID from the session
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found", 'error')
        return redirect(url_for('index'))

    # Determine if the current logged-in user is following this user
    is_following = Follow.query.filter_by(follower_id=current_user_id, followed_id=user.id).first() is not None

    # Load notifications if the current user is viewing their own profile
    notifications = []
    if user.id == current_user_id:
        notifications = Notification.query.filter_by(recipient_id=user.id, read=False).all()

    # Only show follow/unfollow options if viewing someone else's profile
    show_follow_options = user.id != current_user_id

    return render_template("public_profile_page.html", user=user, is_following=is_following, notifications=notifications, show_follow_options=show_follow_options)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('term', '')
    if not search:
        return jsonify([])

    # Querying users, skills, roles, and job postings
    user_query = User.query.filter(
        db.or_(
            User.name.ilike(f'%{search}%'),
            User.email.ilike(f'%{search}%')
        )
    ).limit(5).all()

    skill_query = TechnicalSkill.query.filter(
        TechnicalSkill.name.ilike(f'%{search}%')
    ).limit(5).all()

    role_query = UserRole.query.filter(
        UserRole.role_name.ilike(f'%{search}%')
    ).limit(5).all()

    job_query = JobPosting.query.filter(
        db.or_(
            JobPosting.title.ilike(f'%{search}%'),
            JobPosting.project_type.ilike(f'%{search}%'),
            JobPosting.skills_required.ilike(f'%{search}%'),
            JobPosting.description.ilike(f'%{search}%')
        )
    ).limit(5).all()

    # Combining all queries
    results = set()
    for user in user_query:
        results.add(user.name)
        results.add(user.email)

    for skill in skill_query:
        results.add(skill.name)

    for role in role_query:
        results.add(role.role_name)

    for job in job_query:
        results.add(job.title)  # Include job titles in the autocomplete suggestions

    return jsonify(list(results))






#new
@app.route('/follow/<int:freelancer_id>', methods=['POST'])
@login_required
def follow_freelancer(freelancer_id):
    if 'user_id' not in session or session.get('role') != 'employer':
        flash('You need to be logged in as an employer to follow.')
        return redirect(url_for('login'))

    freelancer = User.query.get(freelancer_id)
    employer = User.query.get(session['user_id'])  # Get the employer who is following
    if not freelancer:
        flash('Freelancer not found.')
        return redirect(url_for('some_fallback_route'))

    if Follow.query.filter_by(follower_id=employer.id, followed_id=freelancer_id).first():
        flash('You are already following this freelancer.')
        return redirect(url_for('public_profile', email=freelancer.email))

    new_follow = Follow(follower_id=employer.id, followed_id=freelancer_id)
    db.session.add(new_follow)
    db.session.commit()

    # Include employer's name in the notification message
    notification = Notification(
        recipient_id=freelancer_id,
        sender_id=employer.id,
        message=f'{employer.name} is now following you!',
        read=False
    )
    db.session.add(notification)
    db.session.commit()

    flash('You are now following the freelancer.')
    return redirect(url_for('public_profile', email=freelancer.email))


#new
@app.route('/unfollow/<int:freelancer_id>', methods=['POST'])
@login_required
def unfollow_freelancer(freelancer_id):
    if 'user_id' not in session or session.get('role') != 'employer':
        flash('You need to be logged in as an employer to unfollow.')
        return redirect(url_for('login'))

    employer = User.query.get(session['user_id'])
    follow_relation = Follow.query.filter_by(follower_id=employer.id, followed_id=freelancer_id).first()

    if not follow_relation:
        flash('You are not following this freelancer.')
        return redirect(url_for('public_profile', email=User.query.get(freelancer_id).email))

    db.session.delete(follow_relation)
    db.session.commit()
    flash('You have unfollowed the freelancer.')
    return redirect(url_for('public_profile', email=User.query.get(freelancer_id).email))

#new
@app.route('/notifications')
@login_required
def notifications():
    user_id = session.get('user_id')
    user_role = session.get('role')

    if user_role != 'freelancer':
        flash('You need to be logged in as a freelancer to view notifications.')
        return redirect(url_for('login'))

    notifications = Notification.query.filter_by(recipient_id=user_id, read=False).all()

    return render_template('notifications.html', notifications=notifications)

#new
@app.route('/notifications/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification and notification.recipient_id == session['user_id']:
        notification.read = True
        db.session.commit()
        flash('Notification marked as read.')
    else:
        flash('Notification not found or access denied.')
    return redirect(url_for('profile_page'))  # Redirect back to the profile page or notifications page

#new
@app.route('/my-followers')
@login_required
def my_followers():
    user_id = session.get('user_id')
    followers = User.query.join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user_id).all()
    return render_template('followers.html', followers=followers)


#new
@app.route('/view-followings')
@login_required
def view_followings():
    user_id = session.get('user_id')
    # Assuming you have a relationship set up to directly access whom the user is following
    user = User.query.get(user_id)
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('login'))

    followed_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()

    return render_template("followings.html", followed_users=followed_users)