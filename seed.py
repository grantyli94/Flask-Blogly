"""Seed file to make sample data for pets db."""
from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
albert = User(first_name = 'Albert', last_name="Anderson")
brittany = User(first_name = 'Brittany', last_name="Baylor")
carlos = User(first_name = 'Carlos', last_name="Crumbs")

# Add new objects to session, so they'll persist
db.session.add(albert)
db.session.add(brittany)
db.session.add(carlos)

db.session.commit()

# Add posts
post1 = Post(title='Title1', content="Content1", user_id=albert.id)
post2 = Post(title='Title2', content="Content2", user_id=brittany.id)
post3 = Post(title='Title3', content="Content3", user_id=carlos.id)

# Add new objects to session, so they'll persist
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# Commit--otherwise, this never gets saved!
db.session.commit()