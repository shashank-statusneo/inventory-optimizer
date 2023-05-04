# Define fixture her to make a fixture available to multiple test files

from pytest import fixture
from modules import create_app, db
from routes import blueprint
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


@fixture(scope="class")
def app():
    # Create a Flask app configured for testing
    flask_app = create_app(env="test")
    flask_app.register_blueprint(blueprint=blueprint)
    flask_app.testing = True

    flask_app.app_context().push()

    db.create_all()

    yield flask_app

    db.session.close()
    db.drop_all()


@fixture(scope="class")
def client(app):
    return app.test_client()


@fixture(scope="class")
def import_users(client):
    """
    Create new users data from data/users.json
    """
    with open("tests/data/users.json", "r") as user_file:
        users = loads(user_file.read())

    for user in users:
        db.session.add(Users(**user, public_id=str(uuid.uuid4())))
    db.session.commit()
