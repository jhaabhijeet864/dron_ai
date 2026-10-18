"""
LeetCode GraphQL API Fetcher

Fetches public profile data from LeetCode's GraphQL endpoint:
    - Total problems solved (by difficulty: Easy/Medium/Hard)
    - Contest rating
    - Submission statistics
    - Public profile info

GraphQL Endpoint: https://leetcode.com/graphql

Note: LeetCode does not provide official API documentation.
These queries are based on reverse-engineered community implementations
(alfa-leetcode-api, leetcode-query).
"""

import copy
import time
import threading
import requests
import logging

from app.utils.sanitizer import sanitize_username

logger = logging.getLogger(__name__)

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

_CACHE_TTL_SECONDS = 600
_CACHE_MAXSIZE = 128
_cache: dict = {}
_cache_lock = threading.Lock()


def _cache_get(key: str):
    now = time.monotonic()
    with _cache_lock:
        entry = _cache.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < now:
            _cache.pop(key, None)
            return None
        return copy.deepcopy(value)


def _cache_set(key: str, value: dict) -> None:
    with _cache_lock:
        if key in _cache:
            _cache.pop(key)
        elif len(_cache) >= _CACHE_MAXSIZE:
            _cache.pop(next(iter(_cache)))
        _cache[key] = (time.monotonic() + _CACHE_TTL_SECONDS, copy.deepcopy(value))


def _cache_clear() -> None:
    with _cache_lock:
        _cache.clear()


# GraphQL query to fetch user profile and problem stats
USER_PROFILE_QUERY = """
query getUserProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            realName
            ranking
            reputation
        }
        submitStats {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}
"""

# GraphQL query to fetch contest rating
CONTEST_RATING_QUERY = """
query userContestRankingInfo($username: String!) {
    userContestRanking(username: $username) {
        rating
        globalRanking
        totalParticipants
        attendedContestsCount
    }
}
"""


def fetch_leetcode_stats(username: str) -> dict:
    """
    Fetch public LeetCode statistics for a given username.

    Results are cached in memory for 10 minutes. Failures (unknown
    user, network error) return baseline zeros and are NOT cached,
    so a later retry hits the API again.

    Args:
        username: LeetCode username

    Returns:
        Dict with:
            - problems_solved: int (total)
            - easy_solved: int
            - medium_solved: int
            - hard_solved: int
            - contest_rating: float
            - ranking: int
    """
    logger.info(f"Fetching LeetCode stats for: {username}")

    result = {
        "problems_solved": 0,
        "easy_solved": 0,
        "medium_solved": 0,
        "hard_solved": 0,
        "contest_rating": 0.0,
        "ranking": 0,
    }

    if not username or not isinstance(username, str):
        return result

    try:
        clean_user = sanitize_username(username)
    except (ValueError, TypeError, AttributeError):
        logger.warning(f"Rejected invalid LeetCode username: {username}")
        return result
    if not clean_user:
        return result

    cache_key = clean_user.lower()
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    result, cacheable = _fetch_leetcode_stats_uncached(clean_user)
    if cacheable:
        _cache_set(cache_key, result)
    return result


def _fetch_leetcode_stats_uncached(username: str) -> tuple:
    """Fetch from API. Returns (result, cacheable); failures are not cacheable."""
    result = {
        "problems_solved": 0,
        "easy_solved": 0,
        "medium_solved": 0,
        "hard_solved": 0,
        "contest_rating": 0.0,
        "ranking": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    try:
        # 1. Fetch user profile and submission stats
        payload1 = {
            "query": USER_PROFILE_QUERY,
            "variables": {"username": username}
        }
        r1 = requests.post(LEETCODE_GRAPHQL_URL, json=payload1, headers=headers, timeout=10)

        # GUARD: Non-200 responses (429 rate limits, 500/503 server errors) must NOT be cached
        if r1.status_code != 200:
            logger.warning(f"LeetCode API returned status {r1.status_code} for user: {username}")
            return result, False

        data = r1.json().get("data", {})
        matched_user = data.get("matchedUser")

        if matched_user is None:
            logger.warning(f"LeetCode user not found: {username}")
            return result, False

        stats = matched_user.get("submitStats", {}).get("acSubmissionNum", [])
        for stat in stats:
            diff = stat.get("difficulty")
            count = stat.get("count", 0)
            if diff == "All":
                result["problems_solved"] = count
            elif diff == "Easy":
                result["easy_solved"] = count
            elif diff == "Medium":
                result["medium_solved"] = count
            elif diff == "Hard":
                result["hard_solved"] = count

        # 2. Fetch contest ranking
        payload2 = {
            "query": CONTEST_RATING_QUERY,
            "variables": {"username": username}
        }
        r2 = requests.post(LEETCODE_GRAPHQL_URL, json=payload2, headers=headers, timeout=10)

        if r2.status_code == 200:
            contest_data = r2.json().get("data", {})
            contest_info = contest_data.get("userContestRanking")

            if contest_info:
                result["contest_rating"] = contest_info.get("rating", 0.0)
                result["ranking"] = contest_info.get("globalRanking", 0)

        return result, True

    except requests.RequestException as e:
        logger.error(f"Error fetching LeetCode stats for {username}: {e}")
        return result, False
    except Exception as e:
        logger.error(f"Unexpected error fetching LeetCode stats for {username}: {e}")
        return result, False


def _leetcode_cache_clear() -> None:
    _cache_clear()


fetch_leetcode_stats.cache_clear = _leetcode_cache_clear
