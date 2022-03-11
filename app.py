from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm

from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MyChihuahuaIsAngryToday'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)


@app.route('/')
def redirect_to_register():
    """Takes you to the registration page"""
    return redirect('/register')

 

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user and handle the form"""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Welcome { new_user.username }! You Successfully Created Your Account", 'success')
        return redirect('/secret')
    
    else:
        return render_template('register.html', form=form)
    

@app.route('/secret')
def show_secrets():
    return render_template('secrets.html')   
    