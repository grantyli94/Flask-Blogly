"""Models for Blogly"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_URL = 'https://www.pngitem.com/pimgs/m/287-2876223_no-profile-picture-available-hd-png-download.png'

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model): 
    """A table for users of Blogly, a blogging application"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    image_url = db.Column(db.String, nullable=False, default=DEFAULT_URL)

    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        """Show information about the user"""

        return (f"<User {self.id} {self.first_name} {self.last_name}>")


class Post(db.Model):
    """A table for posts written by user of Blogly"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.String(1000),
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
                        
    
    def __repr__(self):
        """Show information about the post"""
        
        return (f"<Post {self.id} {self.title} {self.created_at}>")


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)
    
    posts = db.relationship('Post',
                            secondary='posts_tags',
                            backref='tags')

    def __repr__(self):
        """Shows information about the tag"""

        return (f"<Tag {self.id} {self.name}>")

class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True)

