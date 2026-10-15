"""Counts the releases I've shipped and renders them as a light and a dark SVG card.

A release counts when it is published (not a draft), lives in a non-fork repository
I own, and was created by me or by GitHub Actions (my CI). A repository named
"X-releases" is skipped when I also own "X", since it only mirrors X's releases.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com/graphql"
OUT_DIR = "profile-stats"
CI_LOGINS = {"github-actions", "github-actions[bot]"}

REPOS_QUERY = """
query($cursor: String) {
  viewer {
    login
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes { name nameWithOwner isPrivate }
    }
  }
}
"""

RELEASES_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    releases(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { isDraft publishedAt author { login } }
    }
  }
}
"""

THEMES = {
    "light": {"bg": "#ffffff", "border": "#e4e2e2", "title": "#0366d6", "text": "#586069", "accent": "#24292e"},
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#58a6ff", "text": "#8b949e", "accent": "#c9d1d9"},
}


def graphql(token, query, variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
    if body.get("errors"):
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


def owned_repos(token):
    repos, cursor, login = [], None, None
    while True:
        viewer = graphql(token, REPOS_QUERY, {"cursor": cursor})["viewer"]
        login = viewer["login"]
        page = viewer["repositories"]
        repos += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return login, repos
        cursor = page["pageInfo"]["endCursor"]


def releases(token, name_with_owner):
    owner, name = name_with_owner.split("/")
    result, cursor = [], None
    while True:
        page = graphql(token, RELEASES_QUERY, {"owner": owner, "name": name, "cursor": cursor})
        page = page["repository"]["releases"]
        result += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return result
        cursor = page["pageInfo"]["endCursor"]


def collect(token):
    login, repos = owned_repos(token)
    names = {r["name"] for r in repos}
    authors = CI_LOGINS | {login}
    since = datetime.now(timezone.utc) - timedelta(days=365)

    total = last_year = 0
    shipped_repos = private_repos = 0
    latest = None
    for repo in repos:
        if repo["name"].endswith("-releases") and repo["name"].removesuffix("-releases") in names:
            continue
        mine = [
            r for r in releases(token, repo["nameWithOwner"])
            if not r["isDraft"] and r["publishedAt"] and (r["author"] or {}).get("login") in authors
        ]
        if not mine:
            continue
        shipped_repos += 1
        private_repos += repo["isPrivate"]
        total += len(mine)
        for r in mine:
            published = datetime.fromisoformat(r["publishedAt"].replace("Z", "+00:00"))
            last_year += published >= since
            latest = max(latest or published, published)
    return {
        "total": total,
        "last_year": last_year,
        "repos": shipped_repos,
        "private": private_repos,
        "latest": latest,
    }


def render(stats, theme):
    c = THEMES[theme]
    latest = stats["latest"].strftime("%b %d, %Y") if stats["latest"] else "—"
    repos_line = f"across {stats['repos']} repositories"
    if stats["private"]:
        repos_line += f" ({stats['private']} private)"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="340" height="200" viewBox="0 0 340 200">
  <rect x="0.5" y="0.5" width="339" height="199" rx="5" fill="{c['bg']}" stroke="{c['border']}"/>
  <text x="20" y="35" font-family="Segoe UI, Ubuntu, sans-serif" font-size="18" font-weight="600" fill="{c['title']}">Releases shipped</text>
  <text x="20" y="98" font-family="Segoe UI, Ubuntu, sans-serif" font-size="48" font-weight="700" fill="{c['accent']}">{stats['total']}</text>
  <text x="20" y="124" font-family="Segoe UI, Ubuntu, sans-serif" font-size="14" fill="{c['text']}">{repos_line}</text>
  <text x="20" y="160" font-family="Segoe UI, Ubuntu, sans-serif" font-size="13" fill="{c['text']}">Last 12 months: <tspan font-weight="600" fill="{c['accent']}">{stats['last_year']}</tspan></text>
  <text x="20" y="180" font-family="Segoe UI, Ubuntu, sans-serif" font-size="13" fill="{c['text']}">Latest: <tspan font-weight="600" fill="{c['accent']}">{latest}</tspan></text>
</svg>
"""


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    stats = collect(token)
    os.makedirs(OUT_DIR, exist_ok=True)
    for theme in THEMES:
        with open(os.path.join(OUT_DIR, f"releases-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(render(stats, theme))
    print(f"{stats['total']} releases across {stats['repos']} repositories")


if __name__ == "__main__":
    main()
