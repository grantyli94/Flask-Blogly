"""Models for Blogly"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_URL = 'https://www.pngitem.com/pimgs/m/287-2876223_no-profile-picture-available-hd-png-download.png'

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

# Nate: No need to describe table schema (the what). It's mostly best to just document how the models work. Joel?
class User(db.Model): 
    """A table for users of Blogly, a blogging application

        - id: an auto-incrementing integer number that is the primary key
        - first_name: a text value limited to 50 characters
        - last_name: a text value limited to 50 characters
        - image_url: a text link that defaults to a 'Photo Not Available' image"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    image_url = db.Column(db.String, nullable=False, default=DEFAULT_URL)

    def __repr__(self):
        """Show information about the user"""

        return (f"<User {self.id} {self.first_name} {self.last_name}>")

