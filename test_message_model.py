"""Message models tests"""

import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
  """Test model for User."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()

    self.client = app.test_client()

  def tearDown(self):
    """Delete all instances of users from test database"""

    User.query.delete()
    Message.query.delete()
    db.session.commit()

    self.client = app.test_client()

  def test_message_model(self):
    """Does basic model work?"""

    u = User(
      id=1,
      email="test@test.com",
      username="testuser",
      password="testuser"
    )

    m = Message(
      id=1,
      text="Test Message",
      timestamp=None,
      user_id=1
    )

    db.session.add_all([u, m])
    db.session.commit()

    # Message instance attributes should equal the ones were set, timestamp defaults to datetime now()
    self.assertEqual(m.text, 'Test Message')
    self.assertEqual(m.id, 1)
    self.assertEqual(m.user.username, 'testuser')
    self.assertEqual(m.user.email, 'test@test.com')
    self.assertNotEqual(m.timestamp, None)

class MessageLikesRelationshipTestCase(TestCase):
  """Test relationship between messages and likes models"""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Likes.query.delete()

    self.client = app.test_client()

  def tearDown(self):
    """Delete all instances of users from test database"""

    User.query.delete()
    Message.query.delete()
    Likes.query.delete()
    db.session.commit()

    self.client = app.test_client()

  def test_message_like_relationship(self):

    u = User(
      id=1,
      email="test@test.com",
      username="testuser",
      password="testuser"
    )

    m = Message(
      id=1,
      text="Test Message",
      timestamp=None,
      user_id=1
    )


    db.session.add_all([u, m])
    db.session.commit()

    u.liked_messages.append(m)
    db.session.commit()

    #message shows users liking it, users liked messages should include the liked message
    self.assertEqual(m.user_likes[0], u)
    self.assertEqual(u.liked_messages[0], m)