from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt 
from models import db, connect_db

app = Flask(__name__)
bcrypt=Bcrypt()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MyChihuahuaIsAngryToday'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug=DebugToolbarExtension(app)
connect_db(app)