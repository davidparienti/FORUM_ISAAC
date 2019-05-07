from models import Message, Discussion, User, db
from faker import Faker
import random

fake = Faker()

def generate_discussions():
  for n in range(10):
    discussion  = Discussion(title=fake.text())
    db.session.add(discussion)

  db.session.commit()


def generate_messages(discussion_id, users):
  for n in range(5):
    user_index = random.randint(0, len(users) - 1)
    user = users[user_index]
    message = Message(text=fake.text(), discussion_id=discussion_id, user_id=user.id)
    db.session.add(message)

  db.session.commit()


def add_messages_to_discussions():
  users = User.query.all()
  for discussion in Discussion.query.all():
    generate_messages(discussion_id=discussion.id, users=users)


def generate_users():
  for n in range(10):
    user = User(username=fake.email(), password=fake.password())
    db.session.add(user)

  db.session.commit()

generate_users()
# generate_discussions()
add_messages_to_discussions()

