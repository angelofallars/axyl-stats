"""Periodically fetch the download count of a repo every (INTERVAL) minutes,
   and store it in a PostgreSQL database"""
import os
import time
from datetime import datetime

import psycopg2 as pgres
import requests
from dotenv import load_dotenv

load_dotenv()
# Required .env vars
DB_NAME = os.getenv("DB_NAME", None)
REPO_OWNER = os.getenv("REPO_OWNER", None)
REPO_NAME = os.getenv("REPO_NAME", None)

# Optional .env vars
DB_USER = os.getenv("DB_USER", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_UPDATE_INTERVAL = int(os.getenv("DB_UPDATE_INTERVAL", 5))

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

if DB_NAME is None:
    raise Exception("Database name (DB_NAME) not set in the '.env' file.")
elif REPO_OWNER is None:
    raise Exception("No REPO_OWNER set in the .env file.")
elif REPO_NAME is None:
    raise Exception("No REPO_NAME set in the .env file.")
elif GITHUB_API_KEY is None:
    print("Warning: No GitHub API key. You will be limited to 60 requests per \
hour.")


def fetch_download_count(repo_owner: str,
                         repo_name: str,
                         headers: dict) -> tuple[int, int]:

    request_link = 'https://api.github.com/repos/'\
                   + repo_owner + '/' + repo_name + '/releases'

    r = requests.get(request_link, headers=headers)
    releases = r.json()

    total_download_count = 0
    latest_release_count = releases[0]['assets'][0]['download_count']

    for release in releases:
        if "assets" in release:
            total_download_count += release["assets"][0]["download_count"]

    return total_download_count, latest_release_count


def main() -> int:
    headers = {}
    if GITHUB_API_KEY:
        headers["Authorization"] = f"token {GITHUB_API_KEY}"

    repo_name_combined = REPO_OWNER + '/' + REPO_NAME

    # Initialize the connection to the PostgreSQL db
    conn = pgres.connect(database=DB_NAME,
                         user=DB_USER,
                         password=DB_PASS,
                         host=DB_HOST,
                         port=DB_PORT)

    # Initialize the cursor
    cur = conn.cursor()

    # Create the table if it didn't exist
    cur.execute("""CREATE TABLE IF NOT EXISTS repo_stats
                   (
                    repo text,
                    total_downloads integer,
                    latest_downloads integer,
                    stars integer,
                    forks integer,
                    watchers integer,
                    date timestamp
                   )""")
    conn.commit()

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fetch data from the GitHub API (releases)
        total_downloads, latest_downloads = fetch_download_count(REPO_OWNER,
                                                                 REPO_NAME,
                                                                 headers)

        # Fetch from the regular API link (api.github.com/repos/owner/repo)

        # Get stargazer count
        # Get watcher count
        # Get fork count

        cur.execute("""INSERT INTO download_stats
                       (repo, total_downloads, latest_downloads,
                        stars, forks, watchers, date)
                       VALUES
                       (%s, %s, %s, CURRENT_TIMESTAMP(0))""",
                    (repo_name_combined,
                     total_downloads,
                     latest_downloads))
        conn.commit()

        print(f"DB updated for `{repo_name_combined}` - {current_date}")
        print(f"total_downloads: {total_downloads}")
        print(f"latest_downloads: {latest_downloads}")

        # Wait every (interval) minutes
        time.sleep(DB_UPDATE_INTERVAL * 60)

    return 0


if __name__ == "__main__":
    exit(main())
