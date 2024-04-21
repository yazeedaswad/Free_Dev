#this file creates tables for the database which is imported from _init__ file
#there are two tables (classes) with four columns 
#the database itself is stored in the file "freelancer_employer_information.db" in the instance folder
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='freelancer')  # Default role is 'freelancer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

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
    
    
    

#new table
class TechnicalSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating out of 5
    skill_type = db.Column(db.String(20), nullable=False)  # 'language' or 'framework'

#new table
class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_name = db.Column(db.String(50), nullable=False)
    exp_years = db.Column(db.Integer, nullable=False, default=0)    
    
    
    
    
    
    
    
class Freelancer(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), index = True, unique = True, nullable = False)
    
    password_hash = db.Column(db.String(128))
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

    



class Employer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), index = True, unique = True, nullable = False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  
    
    



