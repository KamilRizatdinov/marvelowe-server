from src.bookmarks import (
    add_character_bookmark,
    get_all_character_bookmarks,
    is_bookmarked,
    add_comics_bookmark,
    is_comics_bookmarked,
    get_all_comics_bookmarks,
)


def test_is_bookmarked():
    assert not is_bookmarked("not_exist_user", 1)


def test_add_character_bookmark():
    add_character_bookmark("admin", 3)
    assert is_bookmarked("admin", 3)
    add_character_bookmark("admin", 3)  # to unbookmark for next tests


def test_get_all_character_bookmarks():
    add_character_bookmark("admin", 1)
    add_character_bookmark("admin", 2)
    assert get_all_character_bookmarks("admin") == [1, 2]


def test_is_comic_bookmarked():
    assert not is_comics_bookmarked("not_exist_user", 1)


def test_add_comic_bookmark():
    add_comics_bookmark("admin", 1)
    assert is_comics_bookmarked("admin", 1)
    add_comics_bookmark("admin", 1)


def test_get_all_comics_bookmarks():
    add_comics_bookmark("admin", 1)
    add_comics_bookmark("admin", 2)
    assert get_all_comics_bookmarks("admin") == [1, 2]

