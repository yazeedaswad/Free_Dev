#this file creates tables for the database which is imported from _init__ file
#there are two tables (classes) with four columns 
#the database itself is stored in the file "freelancer_employer_information.db" in the instance folder

from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


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
    
    




