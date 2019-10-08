# Warbler App

Warbler is a concept app created to showcase similar functionality as Twitter. Users can create accounts to use the features of the app. Once registered, users can create messages, follow/unfollow other user, like/unlike messages

The app is served with a [Flask](http://http://flask.pocoo.org/) backend, [Postgres](https://www.postgresql.org/) managed by [SQL Alchemy](https://www.sqlalchemy.org/) as data storage, and [Jinja](http://http://jinja.pocoo.org/) templates for the frontend.
___
#### Features
 - User account creation: required to be able to use the app. User authentication and password hashing is done using [bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
 - User follows: users can follow other users so that their posts will show up on their feed.
 - Message posts: users can post new messages to show up on their feed.
 - Message likes: users can like any message to show in their "liked messages"
 - User feed: view of own feed can be filtered based on the followed users, liked messages, or own messages.
 - User profile: users can edit or delete their profile only by authenticating with their valid password.

___
#### Using the app
Coming from the project folder, create a virtual environment

```sh
$ python -m venv venv
$ source venv/bin/activate
```
Or, use your existing virtual environment (yourflaskenv)
```sh
$ python -m venv venv
$ source activate (yourflaskenv)
```
Install the dependencies
```sh
$ pip install -r requirements.txt
```
Create database and seed with data
```sh
$ createdb warbler
$ python seed.py
```
Start server
```sh
$ flask run
```
