from app import app
from unittest import TestCase
from models import User, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserViewsTestCase(TestCase):

    def setUp(self):
      '''Stuff to do before every test.'''
      print("INSIDE SET UP")
      self.client = app.test_client()

      # Make Flask errors be real errors, not HTML pages with error info
      app.config['TESTING'] = True

      # # Create all tables
      db.create_all()

      # # If table isn't empty, empty it
      User.query.delete()

      # Add pets
      user_1 = User(first_name='Bill', last_name="Mike")
      user_2 = User(first_name='Pete', last_name="Peter")
      user_3 = User(first_name='Sam', last_name="Tom")

      # Add new objects to session, so they'll persist
      db.session.add(user_1)
      db.session.add(user_2)
      db.session.add(user_3)

      # Commit--otherwise, this never gets saved!
      db.session.commit()

    def tearDown(self):
      '''do this after every test'''
      print("INSIDE TEAR DOWN")

      # drop database and recreate
      db.drop_all()
      db.create_all()


    def test_redirection(self):
      '''test to see if home redirects to users'''
      res = self.client.get('/')

      self.assertEqual(res.status_code, 302)
      self.assertEqual(res.location, 'http://localhost/users')

    def test_user_list(self):
      '''test to see if list is generated'''
      res = self.client.get('/users')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<a href="/users/1">Bill Mike</a>',html)

    def test_delete_user(self):
      '''test to see if user is deleted'''
      res = self.client.post('/users/1/delete', follow_redirects=True)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertNotIn('<a href="/users/1">Bill Mike</a>',html)
      self.assertIn('<a href="/users/2">Pete Peter</a>',html)

    def test_add_user(self):
      '''test to see if user is added'''
      res = self.client.post('/users/new', data={'first': 'Ben', 'last': 'Hun', 'image': 'NULL'}, follow_redirects=True)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<a href="/users/4">Ben Hun</a>', html)
