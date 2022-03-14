from src.auth import UserDB, get_user_from_db, hash_password, save_user


def test_hash_password():
    """result should not be equal to the password"""

    example_string = "example_string"

    assert example_string != hash_password(example_string)


def test_save_and_get_user(db_setup):
    user_data = {"username": "birdi7", "hashed_password": "123"}

    save_user(UserDB(**user_data))

    assert get_user_from_db("birdi7") == UserDB(**user_data)


def test_get_user_empty_db(db_setup):
    assert get_user_from_db("birdi7") is None
