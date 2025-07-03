from sqlalchemy.exc import IntegrityError
import pytest

from app import app
from models import db, User, Recipe


class TestUser:
    def test_has_attributes(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) was a British-American actress."
            )
            user.password_hash = "whosafraidofvirginiawoolf"
            db.session.add(user)
            db.session.commit()

            created = User.query.filter_by(username="Liz").first()
            assert created.username == "Liz"
            assert created.image_url.startswith("https://")
            assert created.bio.startswith("Dame Elizabeth")

            with pytest.raises(AttributeError):
                created.password_hash

    def test_requires_username(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User()
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user1 = User(username="Ben")
            user1.password_hash = "pass1"

            user2 = User(username="Ben")
            user2.password_hash = "pass2"

            with pytest.raises(IntegrityError):
                db.session.add_all([user1, user2])
                db.session.commit()

    def test_has_list_of_recipes(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username="Prabhdip")
            user.password_hash = "secure123"

            r1 = Recipe(
                title="Delicious Ham",
                instructions="Long instructions to satisfy the 50 char requirement for Recipe model validations.",
                minutes_to_complete=45,
            )
            r2 = Recipe(
                title="Quick Ham",
                instructions="Another very detailed explanation on how to prepare ham swiftly and safely in under 30 minutes.",
                minutes_to_complete=25,
            )

            user.recipes.extend([r1, r2])
            db.session.add(user)
            db.session.commit()

            assert r1 in user.recipes
            assert r2 in user.recipes
