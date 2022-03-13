from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    

#  MODELS
class User(db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(20),
                         primary_key = True,
                         unique = True)
    
    password = db.Column(db.Text,
                         nullable = False)
    
    email = db.Column(db.String(50),
                      nullable = False)
    
    first_name = db.Column(db.String(30),
                           nullable = False)
    
    last_name = db.Column(db.String(30),
                          nullable = False)
    
    # feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")
    
    @classmethod
    # cls is refering to User, but this is a class method so
    # using cls which is the standard way of doing things on
    # a class method 
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user"""
        
        hashed = bcrypt.generate_password_hash(pwd)
        
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        #  return instance of user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct
           Return user if valid; else return false
        """
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            #  return user instance
            return u
        else:
            return False
        
        
class Feedback(db.Model):
    __tablename__ = 'feedbacks' 
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True) 
    
    title = db.Column(db.String(75),
                      nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable = False)   
    
    user =  db.relationship('User', backref="feedbacks")  