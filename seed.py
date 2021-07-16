"""Seed file to make sample data for pets db."""
from models import User, Post, Tag, PostTag, db
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

db.session.commit()

# Add tags
tag1 = Tag(name='tag1')
tag2 = Tag(name='tag2')
tag3 = Tag(name='tag3')

# Add new objects to session, so they'll persist
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()

# Add PostTags
post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
post_tag2 = PostTag(post_id=post2.id, tag_id=tag2.id)
post_tag3 = PostTag(post_id=post3.id, tag_id=tag3.id)

db.session.add(post_tag1)
db.session.add(post_tag2)
db.session.add(post_tag3)

# Commit--otherwise, this never gets saved!
db.session.commit()