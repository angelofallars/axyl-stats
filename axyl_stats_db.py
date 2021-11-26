"""Fetch the download count of a repo,
   and store it in a PostgreSQL database"""
import os
from datetime import datetime

import psycopg2 as pgres
import requests
from dotenv import load_dotenv


# Connection to the PostgreSQL database
class Connection:

    def __init__(self,
                 db_name: str,
                 username: str = None,
                 password: str = None,
                 host: str = None,
                 port: str = None) -> None:

        # Initialize the connection to the PostgreSQL db
        self.connection: pgres.connection = pgres.connect(database=db_name,
                                                          user=username,
                                                          password=password,
                                                          host=host,
                                                          port=port)
        self.cursor: pgres.cursor = self.connection.cursor()

    def execute(self,
                statement: str,
                placeholders: tuple = None) -> list:
        self.cursor.execute(statement, placeholders)
        self.connection.commit()

        try:
            rows: list = self.cursor.fetchall()
        except pgres.ProgrammingError:
            rows: list = []

        return rows


def create_stats_table(connection: Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS repo_stats
                          (
                           repo text,
                           total_downloads integer,
                           latest_downloads integer,
                           stars integer,
                           watchers integer,
                           forks integer,
                           date timestamp
                          )""")


def insert_into_database(connection: Connection,
                         repo_name: str,
                         total_downloads: int,
                         latest_downloads: int,
                         stars_count: int,
                         watchers_count: int,
                         forks_count: int) -> None:
    connection.execute("""INSERT INTO repo_stats
                       (repo, total_downloads, latest_downloads,
                        stars, watchers, forks, date)
                       VALUES
                       (%s, %s, %s, %s, %s, %s,
                        CURRENT_TIMESTAMP(0))""",
                       (repo_name,
                        total_downloads,
                        latest_downloads,
                        stars_count,
                        watchers_count,
                        forks_count))


def fetch_download_count(repo_owner: str,
                         repo_name: str,
                         headers: dict = None) -> tuple[int, int]:

    request_link: str = 'https://api.github.com/repos/'\
                        + repo_owner + '/' + repo_name + '/releases'

    r: requests.Response = requests.get(request_link, headers=headers)
    releases: list = r.json()

    total_download_count = 0
    latest_release_count = releases[0]['assets'][0]['download_count']

    for release in releases:
        if "assets" in release:
            total_download_count += release["assets"][0]["download_count"]

    return total_download_count, latest_release_count


def fetch_regular_info(repo_owner: str,
                       repo_name: str,
                       headers: dict = None) -> dict:
    api_request = requests.get(
                  f"https://api.github.com/repos/{repo_owner}/{repo_name}",
                  headers=headers).json()
    return api_request


def main() -> int:
    load_dotenv()
    # Required .env vars
    DB_NAME = os.getenv("DB_NAME")
    REPO_OWNER = os.getenv("REPO_OWNER")
    REPO_NAME = os.getenv("REPO_NAME")

    # Optional .env vars
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "5432")

    GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

    if DB_NAME is None:
        print("Database name (DB_NAME) not set in the '.env' file.")
        return 1
    elif REPO_OWNER is None:
        print("No REPO_OWNER set in the .env file.")
        return 1
    elif REPO_NAME is None:
        print("No REPO_NAME set in the .env file.")
        return 1
    elif GITHUB_API_KEY is None:
        print("Warning: No GitHub API key. You will be limited to 60 requests \
per hour.")

    headers: dict = {}
    if GITHUB_API_KEY:
        headers["Authorization"] = f"token {GITHUB_API_KEY}"

    repo_name_combined = REPO_OWNER + '/' + REPO_NAME

    # Initialize the connection to the PostgreSQL db
    conn = Connection(db_name=DB_NAME,
                      username=DB_USER,
                      password=DB_PASS,
                      host=DB_HOST,
                      port=DB_PORT)

    # Create the table if it didn't exist
    create_stats_table(conn)

    current_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fetch data from the GitHub API (releases)
    total_downloads, latest_downloads = fetch_download_count(REPO_OWNER,
                                                             REPO_NAME,
                                                             headers)

    # Fetch from the regular API link
    repo_info = fetch_regular_info(REPO_OWNER, REPO_NAME, headers)

    stars_count = repo_info['stargazers_count']
    watchers_count = repo_info['watchers_count']
    forks_count = repo_info['forks_count']

    insert_into_database(connection=conn,
                         repo_name=repo_name_combined,
                         total_downloads=total_downloads,
                         latest_downloads=latest_downloads,
                         stars_count=stars_count,
                         watchers_count=watchers_count,
                         forks_count=forks_count)

    print(f"DB updated for `{repo_name_combined}` - {current_date}")
    print(f"total_downloads: {total_downloads}")
    print(f"latest_downloads: {latest_downloads}")
    print(f"stars: {stars_count}")
    print(f"watchers: {watchers_count}")
    print(f"forks: {forks_count}")

    return 0


if __name__ == "__main__":
    exit(main())
