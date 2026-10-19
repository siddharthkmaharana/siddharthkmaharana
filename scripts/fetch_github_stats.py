#!/usr/bin/env python3
"""
fetch_github_stats.py

Dynamically fetches live GitHub statistics for a user:
- Daily contribution streak (consecutive days with contributions)
- Annual contributions / total commits
- Public repositories count
- Repositories contributed to
- Followers count
- Lines of code (LOC) additions, deletions, and total count

Caches values to scripts/stats_cache.json so the build scripts remain robust
even if GitHub APIs are rate-limited, offline, or run without tokens.
"""

import os
import re
import json
import datetime
import urllib.request
import urllib.error

CACHE_FILE = os.path.join(os.path.dirname(__file__), "stats_cache.json")

DEFAULT_STATS = {
    "username": "siddharthkmaharana",
    "repos": 20,
    "contributed": "10+",
    "streak": 25,
    "commits": 551,
    "followers": 0,
    "loc_total": 3283733,
    "loc_add": 1407982,
    "loc_del": 1875751,
    "last_updated": "2026-10-19T11:54:29Z"
}


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                res = DEFAULT_STATS.copy()
                res.update(cached)
                return res
        except Exception as e:
            print(f"[fetch_github_stats] Warning: failed to read cache: {e}")
    return DEFAULT_STATS.copy()


def save_cache(stats):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        print(f"[fetch_github_stats] Cached stats saved to {CACHE_FILE}")
    except Exception as e:
        print(f"[fetch_github_stats] Warning: failed to write cache: {e}")


def fetch_contributions_data(username):
    """
    Fetches the SVG/HTML contributions fragment from github.com/users/{username}/contributions
    Returns (current_streak, total_annual_contributions, cells)
    """
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"[fetch_github_stats] Failed to fetch contributions page: {e}")
        return None, None, []

    # Parse total contributions in the last year
    annual_count = None
    h2_match = re.search(r'([\d,]+)\s+contributions\s+in the last year', html)
    if h2_match:
        annual_count = int(h2_match.group(1).replace(",", ""))

    # Parse individual cells
    # Pattern for cells: data-date and data-level
    cell_re = re.compile(r'data-date="(?P<date>\d{4}-\d{2}-\d{2})"[^>]*data-level="(?P<level>\d)"')
    cell_re_alt = re.compile(r'data-level="(?P<level>\d)"[^>]*data-date="(?P<date>\d{4}-\d{2}-\d{2})"')

    cells_map = {}
    for m in cell_re.finditer(html):
        cells_map[m.group("date")] = int(m.group("level"))
    if not cells_map:
        for m in cell_re_alt.finditer(html):
            cells_map[m.group("date")] = int(m.group("level"))

    # Also parse tooltip counts for accurate per-day count if present
    # <tool-tip ... for="...-X-Y">N contributions on Month Day.</tool-tip>
    # Note: data-level > 0 is always at least 1 contribution
    sorted_dates = sorted(cells_map.keys())
    if not sorted_dates:
        return None, annual_count, []

    # Calculate current daily streak
    # If today has level > 0, streak ends today.
    # If today has level == 0, check yesterday. If yesterday has level > 0, streak is still active.
    # Otherwise streak is 0.
    today_idx = len(sorted_dates) - 1
    if cells_map[sorted_dates[today_idx]] == 0:
        # Today has no contributions yet (could be early morning)
        if today_idx > 0 and cells_map[sorted_dates[today_idx - 1]] > 0:
            start_idx = today_idx - 1
        else:
            start_idx = -1
    else:
        start_idx = today_idx

    current_streak = 0
    if start_idx >= 0:
        for i in range(start_idx, -1, -1):
            date_str = sorted_dates[i]
            if cells_map[date_str] > 0:
                current_streak += 1
            else:
                break

    cells_list = [(d, cells_map[d]) for d in sorted_dates]
    return current_streak, annual_count, cells_list


def fetch_api_user_data(username, token=None):
    """
    Fetches public repos, followers, and basic profile info via GitHub API.
    """
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[fetch_github_stats] Warning: GitHub user API failed: {e}")
        return None


def fetch_graphql_stats(username, token):
    """
    Queries GitHub GraphQL API for repositories contributed to, total commits, and LOC.
    """
    if not token:
        return {}

    url = "https://api.github.com/graphql"
    query = """
    query($login: String!) {
      user(login: $login) {
        repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        repositories(first: 100, ownerAffiliations: [OWNER]) {
          totalCount
          nodes {
            name
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 100) {
                    nodes {
                      author {
                        user {
                          login
                        }
                      }
                      additions
                      deletions
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    data = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read().decode("utf-8"))
            if "errors" in res:
                print(f"[fetch_github_stats] GraphQL error: {res['errors']}")
                return {}
            return res.get("data", {}).get("user", {})
    except Exception as e:
        print(f"[fetch_github_stats] Warning: GraphQL query failed: {e}")
        return {}


def get_live_stats(username="siddharthkmaharana"):
    """
    Gathers live GitHub stats with multi-layered fallbacks:
    1. Contributions calendar (streak + annual contributions)
    2. GitHub REST API (repos, followers)
    3. GitHub GraphQL (if GITHUB_TOKEN present)
    4. Local cache (stats_cache.json) for LOC or offline fallbacks
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("ACCESS_TOKEN")
    stats = load_cache()

    # 1. Contributions calendar
    streak, annual_contribs, _ = fetch_contributions_data(username)
    if streak is not None:
        stats["streak"] = streak
    if annual_contribs is not None and annual_contribs > 0:
        stats["commits"] = annual_contribs

    # 2. REST API user details
    user_api = fetch_api_user_data(username, token=token)
    if user_api:
        if "public_repos" in user_api:
            stats["repos"] = user_api["public_repos"]
        if "followers" in user_api:
            stats["followers"] = user_api["followers"]

    # 3. GraphQL if token is available
    if token:
        gql = fetch_graphql_stats(username, token)
        if gql:
            contrib_count = gql.get("repositoriesContributedTo", {}).get("totalCount")
            if contrib_count is not None and contrib_count > 0:
                stats["contributed"] = f"{contrib_count}+"

            # Compute additions & deletions from recent commit history if nodes present
            repo_nodes = gql.get("repositories", {}).get("nodes", [])
            total_adds = 0
            total_dels = 0
            for repo in repo_nodes:
                branch = repo.get("defaultBranchRef")
                if not branch:
                    continue
                commits = branch.get("target", {}).get("history", {}).get("nodes", [])
                for c in commits:
                    author_login = c.get("author", {}).get("user", {}).get("login")
                    if author_login and author_login.lower() == username.lower():
                        total_adds += c.get("additions", 0)
                        total_dels += c.get("deletions", 0)

            # If additions found from token query, update LOC
            if total_adds > 0:
                # Add on top of baseline if incremental, or update
                stats["loc_add"] = max(stats["loc_add"], total_adds)
                stats["loc_del"] = max(stats["loc_del"], total_dels)
                stats["loc_total"] = stats["loc_add"] + stats["loc_del"]

    stats["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_cache(stats)
    return stats


if __name__ == "__main__":
    import sys
    uname = sys.argv[1] if len(sys.argv) > 1 else "siddharthkmaharana"
    s = get_live_stats(uname)
    print("\n--- Live GitHub Stats ---")
    for k, v in s.items():
        print(f"  {k}: {v}")
