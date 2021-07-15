from unittest import TestCase

from app import app
from models import db, User

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add test user."""

        User.query.delete()

        # Add test user
        user = User(first_name = 'TestUser', last_name="TestLast")

        # Add new object to session, so it persists
        db.session.add(user)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test that list of users show"""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        """Test that details about a specific user show"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> TestUser TestLast </h1>', html)

    def test_add_user(self):
        """Test that the process of adding a user and redirecting back to the list of users"""

        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "TestLast2", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2 TestLast2", html)

    def test_show_edit_form(self):
        """Test that the edit user form shows"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser", html)

    def test_edit_user(self):
        """Test that the process of editing a user and redirecting back to the list of users"""

        with app.test_client() as client:
            d = {"first_name": "TestUserA", "last_name": "TestLastA", "image_url": ""}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUserA TestLastA", html)

    def test_delete_user(self):
        """Test that the process of deleting a user and redirecting back to the list of users"""
        
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("TestUser", html)

    # passed: python3 -m unittest -v test_flask.py


