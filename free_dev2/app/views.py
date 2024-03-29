#this is the crux of the application
#allmost all the functions are stored and accessed here

from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, session, flash
from app.models import Freelancer, Employer


@app.route('/')
def index():
    return  render_template('main.html')

@app.route('/register-freelancer', methods = ['POST'])
def register_freelancer():
    form = request.form
    freelancer = Freelancer(    
        
        name = form['name'],
        email= form['email-address']
    )   
    freelancer.set_password(form['password'])
    db.session.add(freelancer)
    db.session.commit()
    return "Successfully registered"

@app.route('/validate-freelancer-registration', methods = ['POST'])
def validate_freelancer_registration():

    if request.method == "POST":
        email_address = request.get_json()['email']
        freelancer = Freelancer.query.filter_by(email = email_address).first()
        if freelancer:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})
    

    

@app.route('/login-freelancer', methods = ['POST'])
def login_freelancer():
    form = request.form
    freelancer = Freelancer.query.filter_by(email = form['email-address']).first()
    if not freelancer:
        flash("freelancer does not exist")
        return redirect(url_for("index"))
    if freelancer.check_password(form['password']):
        session['freelancer'] = freelancer.id
        return  redirect(url_for('freelancer_main_page'))
    else:
        flash('Password was incorrect')
        return redirect(url_for('index'))

    
@app.route('/logout-freelancer', methods = ['POST', 'GET'])
def logout_freelancer():
    session.pop('freelancer', None)
    return redirect(url_for('index'))


@app.route('/register-employer', methods = ['POST'])
def register_employer():
    form = request.form
    employer = Employer(    
        
        name = form['name'],
        email= form['email-address']
    )   
    employer.set_password(form['password'])
    db.session.add(employer)
    db.session.commit()
    return "Successfully registered"

@app.route('/validate-employer-registration', methods = ['POST'])
def validate_employer_registration():

    if request.method == "POST":
        email_address = request.get_json()['email']
        employer = Employer.query.filter_by(email = email_address).first()
        if employer:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})
    

    

@app.route('/login-employer', methods = ['POST'])
def login_employer():
    form = request.form
    employer = Employer.query.filter_by(email = form['email-address']).first()
    if not employer:
        flash("employer does not exist")
        return redirect(url_for("index"))
    if employer.check_password(form['password']):
        session['employer'] = employer.id
        return  redirect(url_for('employer_main_page'))
    else:
        flash('Password was incorrect')
        return redirect(url_for('index'))

    
@app.route('/logout-employer', methods = ['POST', 'GET'])
def logout_employer():
    session.pop('employer', None)
    return redirect(url_for('index'))

    



@app.route('/employer-reg-log-page')
def employer_page():
    return render_template("employer_reg_log.html")

@app.route('/freelancer-reg-log-page')
def freelancer_page():
    return render_template("freelancer_reg_log.html") 


@app.route('/employer-main-content-page')
def employer_main_page():
    return render_template("employer_main_content.html")


@app.route('/freelancer-main-content-page')
def freelancer_main_page():
    return render_template("freelancer_main_content.html")


