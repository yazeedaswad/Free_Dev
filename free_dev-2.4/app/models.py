#this file creates tables for the database which is imported from _init__ file
#there are two tables (classes) with four columns 
#the database itself is stored in the file "freelancer_employer_information.db" in the instance folder

from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


#added profile_photo_url column
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='freelancer')  # Default role is 'freelancer'
    profile_photo_url = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    



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
    

    

    




