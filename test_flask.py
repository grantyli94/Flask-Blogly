from unittest import TestCase

from app import app
from models import db, User

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
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
        """Add sample user."""
        User.query.delete()

        # Add users
        albert = User(first_name = 'Albert', last_name="Anderson")
        brittany = User(first_name = 'Brittany', last_name="Baylor")
        carlos = User(first_name = 'Carlos', last_name="Crumbs")

        # Add new objects to session, so they'll persist
        db.session.add(albert)
        db.session.add(brittany)
        db.session.add(carlos)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.user_id = user.id


    # def tearDown(self):
    #     """Clean up any fouled transaction."""
    #     db.session.rollback()
    # def test_list_pets(self):
    #     with app.test_client() as client:
    #         resp = client.get("/")
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('TestPet', html)
    # def test_show_pet(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/{self.pet_id}")
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h1>TestPet</h1>', html)
    # def test_add_pet(self):
    #     with app.test_client() as client:
    #         d = {"name": "TestPet2", "species": "cat", "hunger": 20}
    #         resp = client.post("/", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>TestPet2</h1>", html)


