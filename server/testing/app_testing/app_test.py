from app import app
from models import db, User, Recipe
import pytest

class TestRecipeIndex:
    def test_creates_recipes_with_201(self):
        '''creates a recipe associated with the logged in user and returns 201.'''

        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(username='Misty')
            user.password_hash = 'starmie'
            db.session.add(user)
            db.session.commit()

            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = user.id

                response = client.post('/recipes', json={
                    'title': 'Cake',
                    'instructions': 'Mix ingredients thoroughly and bake for 45 minutes in a preheated oven at 350°F.',
                    'minutes_to_complete': 45
                })

                data = response.get_json()
                assert response.status_code == 201
                assert data['title'] == 'Cake'
                assert data['minutes_to_complete'] == 45

    def test_returns_422_for_invalid_recipes(self):
        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(username='Jessie')
            user.password_hash = 'ekans'
            db.session.add(user)
            db.session.commit()

            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = user.id

                # Missing instructions
                response = client.post('/recipes', json={
                    'title': 'Soup',
                    'minutes_to_complete': 10
                })

                assert response.status_code == 422
                assert 'errors' in response.get_json()
