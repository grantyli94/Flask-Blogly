"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/users')
def show_users():

    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new')
def show_add_form():

    return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def add_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # Maybe enforce 50 characters later

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


