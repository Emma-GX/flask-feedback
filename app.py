from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, connect_db, User, Feedback
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'MyChihuahuaIsAngryToday')
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
        return redirect(f"/users/{username}")
    
    else:
        return render_template('register.html', form=form)
    

@app.route('/users/<username>')
def show_user(username):
    """Display a template the shows information about that user 
    (everything except for their password) and their posts
    
    You should ensure that only logged in users can access this page
    """    
  
    user = User.query.get_or_404(username)
    
    current_users_posts = Feedback.query.filter_by(username = username)
    
    if session.get('username') is not None:
        return render_template("user.html", user=user, posts = current_users_posts)        
    else:
        flash('Please Log In Before Trying To Access This Page!', 'danger')
        return redirect('/')

@app.route ('/users/all') 
def show_all_users():
    """Shows a list of all users"""
    
    if session.get('username') is not None:
        users = User.query.order_by(User.username.desc()).all()
        return render_template("all_users.html", users=users)         
    else:
        flash('Please Log In Before Trying To Access This Page!', 'danger')
        return redirect('/')
      

@app.route('/posts/all')
def show_all_posts():
    """Show list of all posts"""
    
    if session.get('username') is not None:
        posts = Feedback.query.all()
        return render_template('all_feedback.html', posts=posts)        
    else:
        flash('Please Log In Before Trying To Access This Page!', 'danger')
        return redirect('/')
    
        
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
            flash(f"Welcome Back, { username }! You Successfully Logged In To Your Account", 'success')
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
       
        
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_user_form(username):
    """Display a form to a new feedback    
    You should ensure that only logged in users can access this page
    """
    
    if session.get('username') is not None:
        form = FeedbackForm()
        all_posts = Feedback.query.all()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_post = Feedback(title=title, content=content, username=session["username"])
            db.session.add(new_post)
            db.session.commit()
            flash('Post Created!', 'success')
            return redirect(f"/users/{username}")
        return render_template(f"feedback.html", form=form, posts=all_posts)        
    else:
        flash('Please Log In Before Trying To Access This Page!', 'danger')
        return redirect('/')
    
    
@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    """Delete a Post by the Feedback id"""
    
    # If someone tries to send a request from insomnia
    if 'username' not in session:
        flash("Please Log In First", 'danger')
        return redirect('/')
    
     # This makes sure the person who is deleting the post is the one who created it
    if post.username != session['username']:
        flash('Not Allowed')
        return redirect('/posts/all')
    
    post = Feedback.query.get_or_404(id)
    if post.username == session['username']:
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted", 'success')
    
        return redirect(f"/users/{post.username}")
    flash("You Don't Have Permission To Delete This Post")
    return redirect("/posts/all")


@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    """Show the edit page for a user.
       Have a cancel button that returns to the detail 
       page for a user, and a save button that updates 
       the user.
       
        Process the edit form, returning the user to the /users page."""
    form = FeedbackForm()
    post = Feedback.query.get_or_404(id)
    # This makes sure the person who is updating the post is the one who created it
    if post.username != session['username']:
        flash('Not Allowed')
        return redirect('/posts/all')
    # This takes the values from post and fills the form    
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
    if form.validate_on_submit():
        post.title = request.form['title']
        post.content = request.form['content']
        
        current_user = post.username
        
       
        db.session.add(post)
        db.session.commit()
        flash("Post Updated", 'success')
        return redirect(f"/users/{current_user}")
        
    
    return render_template('feedback.html', post=post, form=form)
    
    