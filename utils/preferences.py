_user_genres: dict[int, set[int]] = {}

def get_genres(user_id: int) -> set[int]:
    return _user_genres.get(user_id, set())

def toggle_genre(user_id: int, genre_id: int):
    genres = _user_genres.setdefault(user_id, set())
    if genre_id in genres:
        genres.remove(genre_id)
    else:
        genres.add(genre_id)
    if not genres:
        _user_genres.pop(user_id, None)

def clear_genres(user_id: int):
    _user_genres.pop(user_id, None)
