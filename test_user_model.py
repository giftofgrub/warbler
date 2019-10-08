"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
  """Test views for messages."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    Likes.query.delete()
    db.session.commit()

    self.client = app.test_client()

  def tearDown(self):
    """Delete all instances of users from db"""
    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    db.session.commit()

    self.client = app.test_client()


  def test_user_model(self):
    """Does basic model work?"""

    u = User(
        email="testuser@testuser.com",
        username="testuser",
        password="testuser"
    )

    db.session.add(u)
    db.session.commit()

    # User should have no messages & no followers
    self.assertEqual(len(u.messages), 0)
    self.assertEqual(len(u.followers), 0)
    self.assertEqual(u.email, "testuser@testuser.com")
    self.assertEqual(u.username, "testuser")

  def test_signup(self):
    """Does signup for users work? """
    u = User.signup(
        email="testuser@testuser.com",
        username="testuser",
        password="testuser",
        image_url=None,
        header_image_url=None,
        bio=None,
        location=None
    )

    db.session.add(u)
    db.session.commit()

    # username and hashed password expected
    self.assertEqual(u.username, "testuser")
    self.assertIn('$2b$12$', u.password)
  
  def test_authenticate(self):
    """Does authentication process work?  Does passed in password match database password?"""
    u = User.signup(
      email="testuser@testuser.com",
      username="testuser",
      password="testuser",
      image_url=None,
      header_image_url=None,
      bio=None,
      location=None
    )

    db.session.add(u)
    db.session.commit()

    authenticated_user = User.authenticate(u.username, 'testuser')
    unauthenticated_user = User.authenticate(u.username, 'wrongPassword')

    # Correct password should return user
    # Incorrect password should return False
    self.assertEqual(authenticated_user.username, 'testuser')
    self.assertEqual(unauthenticated_user, False)