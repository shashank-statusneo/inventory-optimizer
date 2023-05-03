# Define fixture her to make a fixture available to multiple test files

from pytest import fixture
from modules import create_app, db
from routes import blueprint
from flask_cors import CORS
from modules.users.model import Users
from json import loads
import uuid

# --------
# Fixtures
# --------


@fixture(scope="class")
def test_user(
    email: str = "test_email@test.com",
    username: str = "test_username",
    password: str = "test_password",
    public_id: str = str(uuid.uuid4()),
):
    user = Users(
        email=email,
        username=username,
        password=password,
        public_id=public_id,
    )
    return user


@fixture(scope="session", autouse=True)
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
    db.create_all(bind_key="user")

    # TODO: add users from json file
    # Insert user data
    user1 = Users(
        email="test_user_1@gmail.com",
        username="test_user_1",
        password="test_password_1",
        public_id=str(uuid.uuid4()),
    )
    user2 = Users(
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
    Users.query.filter_by(email="test_user_1@gmail.com").delete()
    Users.query.filter_by(email="test_user_2@gmail.com").delete()
    db.session.commit()


@fixture(scope="class")
def import_users():
    """
    Create new users data from data/users.json
    """
    with open("tests/data/users.json", "r") as user_file:
        users = loads(user_file.read())

    # Create the database and the database table
    db.create_all(bind_key="user")

    # store users in Users table

    for user in users:
        db.session.add(Users(**user, public_id=str(uuid.uuid4())))
    db.session.commit()
