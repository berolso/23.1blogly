"""Seed file to make sample data for pets db."""

from models import User, Post, db, Tag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
user_1 = User(first_name='Paul', last_name="Kim")
user_2 = User(first_name='Dane', last_name="Mike")
user_3 = User(first_name='Gabe', last_name="Dom")


# Add new objects to session, so they'll persist
# db.session.add(user_1)
# db.session.add(user_2)
# db.session.add(user_3)

db.session.add_all([user_1,user_2,user_3])

# Commit--otherwise, this never gets saved!
db.session.commit()

p1 = Post(title='How to be Cool', content="It's really easy, just do this.", user_id=1)
p2 = Post(title='My Best Day', content="Ever just wake up and things are great?.. Well..", user_id=2)
p3 = Post(title='Top 5 Places to Visit', content='''1. Tulum
2. kauai
3. CapeTown
4. Rio De Janeiro
5. Yerevan''', user_id=3)

# db.session.add(p1)
# db.session.add(p2)
# db.session.add(p3)
db.session.add_all([p1,p2,p3])

db.session.commit()

tag_1 = Tag(name='funny')
tag_2 = Tag(name='interesting')
tag_3 = Tag(name='sad')
tag_4 = Tag(name='new')
tag_5 = Tag(name='science')

db.session.add_all([tag_1,tag_2,tag_3,tag_4,tag_5])
db.session.commit()