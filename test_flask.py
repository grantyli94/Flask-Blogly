from unittest import TestCase

from app import app
from models import db, User, Post

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

        Post.query.delete()
        User.query.delete()

        # Add test user
        user = User(first_name = 'TestUser', last_name="TestLast")

        # Add new user object to session, so it persists
        db.session.add(user)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.user_id = user.id

        # Add test post
        post = Post(title = 'TestTitle', content = 'TestContent')

        # Add new post object to session, so it persists
        db.session.add(post)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.post_id = post.id


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

    def test_show_add_form(self):
        """Test that the form to add a post shows for the user"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add Post For", html)

    def test_add_post(self):
        """Test the process of adding a post and redirecting back to the user detail page"""

        with app.test_client() as client:
            d = {"title": "TestTitle2", "content": "TestContent2", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTitle2", html)

    def test_show_post(self):
        """Test that details about a specific post show"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestTitle</h1>', html)

    def test_show_post_edit(self):
        """Test that the edit post form shows"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTitle", html)

    def test_edit_post(self):
        """Test the process of editing a post and redirecting back to the post view"""

        print('user ID is ', self.user_id)
        print('post ID is ', self.post_id)

        with app.test_client() as client:
            d = {"title": "TestTitleEdit", "content": "TestContentEdit", "user_id": self.user_id}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTitleEdit", html)

    # def test_delete_post(self):
    #     """Test the process of deleting a post and redirecting back to the post view"""
        
    #     with app.test_client() as client:
    #         resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True, "user_id": self.user_id)
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("TestTitle", html)


    # passed: python3 -m unittest -v test_flask.py


