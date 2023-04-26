# Define fixture her to make a fixture available to multiple test files

from pytest import fixture
from modules import create_app, db
from routes import blueprint
from flask_cors import CORS
from modules.user.model import User
import uuid

# --------
# Fixtures
# --------


@fixture(scope="module")
def new_user():
    user = User(
        email="test_user_4@gmail.com",
        username="test_user_4",
        password="test_password_4",
        public_id=str(uuid.uuid4()),
    )
    return user


@fixture(scope="module")
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app(env="test")
    flask_app.register_blueprint(blueprint=blueprint)
    CORS(flask_app)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@fixture(scope="module")
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(
        email="test_user_1@gmail.com",
        username="test_user_1",
        password="test_password_1",
        public_id=str(uuid.uuid4()),
    )
    user2 = User(
        email="test_user_2@gmail.com",
        username="test_user_2",
        password="test_password_2",
        public_id=str(uuid.uuid4()),
    )
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    # delete users
    User.query.filter_by(email="test_user_1@gmail.com").delete()
    User.query.filter_by(email="test_user_2@gmail.com").delete()
    db.session.commit()
