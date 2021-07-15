"""Models for Blogly."""
# from typing import Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# add default image as a global variable and then reference the variable below

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    image_url = db.Column(db.String, nullable=False, default='https://www.pngitem.com/pimgs/m/287-2876223_no-profile-picture-available-hd-png-download.png')

