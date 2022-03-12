from src.bookmarks import is_bookmarked, add_character_bookmark, get_all_character_bookmarks

def test_is_bookmarked():
    assert not is_bookmarked('not_exist_user', 1)

def test_add_character_bookmark():
    add_character_bookmark('admin', 1)
    assert is_bookmarked('admin', 1)

def test_get_all_character_bookmarks():
    add_character_bookmark('admin', 1)
    add_character_bookmark('admin', 2)
    assert get_all_character_bookmarks('admin') == [1, 2]