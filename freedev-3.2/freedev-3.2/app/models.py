#this file creates tables for the database which is imported from _init__ file

#the database itself is stored in the file "freelancer_employer_information.db" in the instance folder
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


#there is a column profile_photo_url for storing the url for the pictures. Do not remove it!
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='freelancer')  # Default role is 'freelancer'
    profile_photo_url = db.Column(db.String(255))  # New column for storing profile picture URL

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    
# Define the JobPosting model
class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    project_type = db.Column(db.String(120), nullable=False)
    skills_required = db.Column(db.String(256), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    salary_min = db.Column(db.Float, nullable=False)
    salary_max = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table

    # Define the relationship with the User (Employer) model
    employer = db.relationship('User', backref=db.backref('job_postings', lazy=True))

    # Optional: You can define additional methods as needed
    def __repr__(self):
        return f"<JobPosting {self.title} (ID: {self.id})>"    
    
    
    


class TechnicalSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating out of 5
    skill_type = db.Column(db.String(20), nullable=False)  # 'language' or 'framework'


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_name = db.Column(db.String(50), nullable=False)
    exp_years = db.Column(db.Integer, nullable=False, default=0)    
    
    
    
    
    
    
    
  

    




    

#new
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Follow follower={self.follower_id} followed={self.followed_id}>'
    

#new
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(256))
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.message} from {self.sender_id} to {self.recipient_id}>'    
    


    
    



