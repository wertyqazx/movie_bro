import random
import time
from typing import Any, Dict, List, Optional

import aiohttp

from config.settings import settings

_BASE_URL = "https://api.themoviedb.org/3"
_IMG_BASE = "https://image.tmdb.org/t/p/w500"
_TTL = 3600  # 1 час

_cache: Dict[str, tuple[float, Any]] = {}
_genres_cache: Optional[Dict[int, str]] = None

def _make_key(url: str, params: Dict[str, Any]) -> str:
    return f"{url}|{sorted(params.items())}"

async def _get_json(url: str, params: Dict[str, Any]) -> Any:
    key = _make_key(url, params)
    now = time.time()
    if key in _cache and _cache[key][0] > now:
        return _cache[key][1]

    headers = {"Authorization": f"Bearer {settings.tmdb_token}"}
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as sess:
        async with sess.get(url, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            _cache[key] = (now + _TTL, data)
            return data

async def search_movie(query: str, page: int = 1, lang: str = "ru-RU") -> List[Dict[str, Any]]:
    url = f"{_BASE_URL}/search/movie"
    params = {"query": query, "language": lang, "include_adult": "false", "page": page}
    data = await _get_json(url, params)
    return data.get("results", [])

async def get_movie_details(movie_id: int, lang: str = "ru-RU") -> Dict[str, Any]:
    url = f"{_BASE_URL}/movie/{movie_id}"
    return await _get_json(url, {"language": lang})

def poster_url(path: str | None) -> Optional[str]:
    return _IMG_BASE + path if path else None

async def random_popular_movie(lang: str = "ru-RU") -> Dict[str, Any]:
    page = random.randint(1, 50)
    url = f"{_BASE_URL}/movie/popular"
    data = await _get_json(url, {"language": lang, "page": page})
    return random.choice(data.get("results", []))

async def top_rated_movies(page: int = 1, lang: str = "ru-RU") -> List[Dict[str, Any]]:
    url = f"{_BASE_URL}/movie/top_rated"
    data = await _get_json(url, {"language": lang, "page": page})
    return data.get("results", [])

async def get_genres_map(lang: str = "ru-RU") -> Dict[int, str]:
    global _genres_cache
    if _genres_cache:
        return _genres_cache
    url = f"{_BASE_URL}/genre/movie/list"
    data = await _get_json(url, {"language": lang})
    _genres_cache = {g["id"]: g["name"] for g in data.get("genres", [])}
    return _genres_cache
