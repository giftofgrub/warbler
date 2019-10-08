"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase
from flask import session
from models import db, connect_db, Message, User, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY, do_login

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserSignupViewTestCase(TestCase):
  """Test signup views for users."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    Likes.query.delete()

    self.client = app.test_client()

  def test_signup_form_rendered(self):
    """Test that signup form renders correctly"""

    resp = self.client.get('/signup')

    self.assertEqual(resp.status_code, 200)
    self.assertIn(
        b'<h2 class="join-message">Join Warbler today.</h2>', resp.data)

  def test_signup_submitted_invalid(self):
    """If submitted user signup form is invalid, form should be rendered again"""

    # set invalid password: too short
    resp = self.client.post("/signup", data={"username": "testuser",
                                              "email": "test@test.com",
                                              "password": "a",
                                              "image_url": None,
                                              "header_image_url":None,
                                              "bio":None,
                                              "location":None})

    self.assertEqual(resp.status_code, 200)
    self.assertIn(
        b'Field must be at least 6 characters long', resp.data)
    
    def test_signup_submitted_vali(self):
      """If submitted user signup form is invalid, used is added to database, redirects to homepage"""

      resp = self.client.post("/signup", data={"username": "testuser",
                                                "email": "test@test.com",
                                                "password": "testpassword",
                                                "image_url": None,
                                                "header_image_url":None,
                                                "bio":None,
                                                "location":None}, follow_redirects=True)

      signed_up_user = User.query.one()

      self.assertEqual(resp.status_code, 200)
      self.assertIn(b'<ul class="user-stats nav nav-pills">', resp.data)
      self.assertEqual(signed_up_user.username, 'testuser')

class UserLoginViewTestCase(TestCase):
  """Test login views for users."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    Likes.query.delete()

    self.client = app.test_client()

    self.testuser = User.signup(
                      username="testuser",
                      email="testuser@testuser.com",
                      password="testuser",
                      image_url=None,
                      header_image_url=None,
                      bio=None,
                      location=None
    )

    db.session.commit()
  
  def test_login_form_rendered(self):
    """Test login form shown"""

    resp = self.client.get('/login')

    self.assertEqual(resp.status_code, 200)
    self.assertIn(
      b'<h2 class="join-message">Welcome back.</h2>', resp.data)

  def test_login_submitted_invalid(self):
    """If user login form is not validated the form should be rendered again"""

    # set wrong username and password
    resp = self.client.post("/login", data={"username": "wronguser",
                                            "password": "wrongpassword"})

    self.assertEqual(resp.status_code, 200)
    self.assertIn(
      b'Invalid credentials', resp.data)

  def test_login_submitted_valid(self):
    """If user login form is validated, log in user and redirect to homepage"""

    with self.client:
      resp = self.client.post("/login", data={"username": "testuser",
                                              "password": "testuser"}, follow_redirects=True)
      self.assertEqual(session.get(CURR_USER_KEY), self.testuser.id)

    signed_up_user = User.query.one()

    self.assertEqual(resp.status_code, 200)
    self.assertIn(b'<ul class="user-stats nav nav-pills">', resp.data)
    self.assertEqual(signed_up_user.username, 'testuser')

  def test_logout(self):
    """Test that user can log out correctly"""

    with self.client:
      self.client.post("/login", data={"username": "testuser",
                                        "password": "testuser"}, follow_redirects=True)
      resp = self.client.get("/logout", follow_redirects=True)
      # .GET WHEN KEY DOESN'T EXIST IN DICTIONARY
      self.assertEqual(session.get(CURR_USER_KEY), None)

    self.assertEqual(resp.status_code, 200)
    self.assertIn(b'logged out', resp.data)

class UserShowViewTestCase(TestCase):
  """Test show user views for users."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    Likes.query.delete()

    self.client = app.test_client()

    self.testuser = User.signup(username="testuser",
                                email="testuser@testuser.com",
                                password="testuser",
                                image_url=None,
                                header_image_url=None,
                                bio=None,
                                location=None)

    db.session.commit()

  def test_list_users(self):
    """Test list of users show up in html, filtered list"""

    u1 = User.signup(username="gabriel",
                      email="gabriel@gabriel.com",
                      password="gabriel",
                      image_url=None,
                      header_image_url=None,
                      bio=None,
                      location=None)

    u2 = User.signup(username="jessica",
                      email="jessica@jessica.com",
                      password="jessica",
                      image_url=None,
                      header_image_url=None,
                      bio=None,
                      location=None)

    db.session.commit()

    resp_all = self.client.get("/users")
    resp_search = self.client.get("/users?q=jess")

    self.assertIn(b'gab', resp_all.data)
    self.assertIn(b'jessica', resp_search.data)

def test_users_show(self):
  """Test user profile is shown"""

  resp = self.client.get(f"/users/{self.testuser.id}")

  self.assertIn(b'testuser', resp.data)
  self.assertIn(b'<ul class="list-group" id="messages">', resp.data)

class UserFollowViewTestCase(TestCase):
  """Test user follow views."""

  def setUp(self):
    """Create test client, add sample data."""

    User.query.delete()
    Message.query.delete()
    Follows.query.delete()
    Likes.query.delete()

    self.client = app.test_client()

    self.testuser1 = User.signup(username="testuser1",
                                  email="test1@test.com",
                                  password="testpassword",
                                  image_url=None,
                                  header_image_url=None,
                                  bio=None,
                                  location=None)

    self.testuser2 = User.signup(username="testuser2",
                                  email="test2@test.com",
                                  password="testpassword",
                                  image_url=None,
                                  header_image_url=None,
                                  bio=None,
                                  location=None)

    self.testuser3 = User.signup(username="testuser3",
                                  email="test3@test.com",
                                  password="testpassword",
                                  image_url=None,
                                  header_image_url=None,
                                  bio=None,
                                  location=None)

    db.session.commit()

    # testuser id not available/created until id session is committed
    # f1 = Follows(
    #   user_being_followed_id=self.testuser1.id,
    #   user_following_id=self.testuser2.id
    # )

    # f2 = Follows(
    #   user_being_followed_id=self.testuser2.id,
    #   user_following_id=self.testuser3.id
    # )

    self.testuser1.following.append(self.testuser2)
    self.testuser2.following.append(self.testuser3)
    self.testuser3.following.append(self.testuser1)
    
    db.session.commit()

  def test_show_following(self):
    """Test list of user followers are shown"""

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.testuser1.id

      resp = c.get(f"/users/{self.testuser1.id}/followers")

      self.assertIn(b'testuser3', resp.data)
      self.assertIn(b'<div class="card user-card">', resp.data)

  def test_show_following(self):
    """Test list of user following are shown"""

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.testuser1.id

      resp = c.get(f"/users/{self.testuser1.id}/following")

      self.assertIn(b'testuser2', resp.data)
      self.assertIn(b'<div class="card user-card">', resp.data)

  def test_add_follow(self):
    """Test adding follow returns followed user in html"""
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.testuser1.id

    testFollowee = User.signup(username="testfollowee",
                                email="testfollowee@test.com",
                                password="testpassword",
                                image_url=None,
                                header_image_url=None,
                                bio=None,
                                location=None)
    db.session.commit()

    respForLoggedInUser = c.post(
        f"/users/follow/{testFollowee.id}", follow_redirects='True')

    self.assertIn(b'testfollowee', respForLoggedInUser.data)
    self.assertIn(b'<div class="card user-card">', respForLoggedInUser.data)
    self.assertEqual(respForLoggedInUser.status_code, 200)

  def test_add_follow_unauthorized(self):
    """Test adding follow returns followed user in html"""

    with self.client as c:
      testfollowee = User.signup(username="testfollowee",
                                  email="testfollowee@test.com",
                                  password="testpassword",
                                  image_url=None,
                                  header_image_url=None,
                                  bio=None,
                                  location=None)
      db.session.commit()

      respForUnauthorizedUser = c.post(
          f"/users/follow/{testfollowee.id}", follow_redirects='True')

    self.assertIn(b'Access unauthorized.', respForUnauthorizedUser.data)
    self.assertEqual(respForUnauthorizedUser.status_code, 200)