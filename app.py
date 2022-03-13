from crypt import methods
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm

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
    """Redirect to /register"""
    return redirect('/register')

 

@app.route('/register', methods=['GET', 'POST'])
def register():
    """GET: Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, 
    and last_name.
    
    POST: Process the registration form by adding a new user. 
    Then redirect to /user
    """
    
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
        session['username'] = new_user.username
        flash(f"Welcome { new_user.username }! You Successfully Created Your Account", 'success')
        return redirect('/user')
    
    else:
        return render_template('register.html', form=form)
    

@app.route('/users/<username>')
def show_user(username):
    """Display a template the shows information about that user 
    (everything except for their password)
    
    You should ensure that only logged in users can access this page
    """
    
    user = User.query.get_or_404(username)
    if user:
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
    
    else:
        flash('Please Log In Before Trying To Access This Page!', 'danger')
    return render_template('login.html')
    
    
    
@app.route('/login', methods=['GET', 'POST']) 
def login():
    """GET: Show a form that when submitted will login a user. 
    This form should accept a username and a password.
    
    POST: Process the login form, ensuring the user is authenticated 
    and going to /user if so 
    """       
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome { username }! You Successfully Logged In To Your Account", 'success')
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
    
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)
    
    
@app.route('/logout', methods=['POST'])
def log_out_user():
    """Clear any information from the session and redirect to /"""
    
    session.pop('username')
    flash("Goodbye! You have been logged out!", 'success')
    return redirect('/')
       