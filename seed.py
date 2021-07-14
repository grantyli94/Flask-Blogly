"""Seed file to make sample data for pets db."""
from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
albert = User(first_name = 'Albert', last_name="Anderson")
brittany = User(first_name = 'Brittany', last_name="Baylor")
carlos = User(first_name = 'Carlos', last_name="Crumbs")

# Add new objects to session, so they'll persist
db.session.add(albert)
db.session.add(brittany)
db.session.add(carlos)

# Commit--otherwise, this never gets saved!
db.session.commit()