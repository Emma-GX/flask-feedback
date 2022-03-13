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
    Then redirect to /secret
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
        flash(f"Welcome { new_user.username }! You Successfully Created Your Account", 'success')
        return redirect('/secret')
    
    else:
        return render_template('register.html', form=form)
    

@app.route('/secret')
def show_secrets():
    return render_template('secrets.html')   
    
    
@app.route('/login', methods=['GET', 'POST']) 
def login():
    """GET: Show a form that when submitted will login a user. 
    This form should accept a username and a password.
    
    POST: Process the login form, ensuring the user is authenticated 
    and going to /secret if so 
    """       
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome { username }! You Successfully Logged In To Your Account", 'success')
            return redirect('/secret')
    
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)
    
    
    @app.route('/secret')
    def go_to_secret():
        """Display a template the shows information about that user 
        (everything except for their password)
        You should ensure that only logged in users can access this page
        """
        
        return redirect('secrets.html')