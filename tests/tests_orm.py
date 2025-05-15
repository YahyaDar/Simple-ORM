import pytest
from orm.engine import Model
from orm.migrations import run_migrations


class User(Model):
    table_name = "users"
    primary_key = "id"


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    run_migrations()


def test_create_user():
    user = User.create(name="Test User", email="test@example.com")
    assert user is not None
    assert user.name == "Test User"
    assert user.email == "test@example.com"


def test_get_user():
    user = User.create(name="Test Get", email="get@example.com")
    fetched_user = User.get(id=user.id)
    assert fetched_user is not None
    assert fetched_user.name == "Test Get"
    assert fetched_user.email == "get@example.com"


def test_update_user():
    user = User.create(name="Update User", email="update@example.com")
    user.update(name="Updated Name")
    updated_user = User.get(id=user.id)
    assert updated_user.name == "Updated Name"


def test_delete_user():
    user = User.create(name="Delete User", email="delete@example.com")
    user_id = user.id
    user.delete()
    deleted_user = User.get(id=user_id)
    assert deleted_user is None


def test_all_users():
    User.create(name="User 1", email="user1@example.com")
    User.create(name="User 2", email="user2@example.com")
    users = User.all()
    assert len(users) >= 2

