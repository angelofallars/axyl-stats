import os

import hikari
import requests
from dotenv import load_dotenv

load_dotenv()
# Required .env vars
TOKEN = os.getenv("BOT_TOKEN", None)
REPO_OWNER = os.getenv("REPO_OWNER", None)
REPO_NAME = os.getenv("REPO_NAME", None)
COUNTER_CHANNEL = os.getenv("COUNTER_CHANNEL", None)

# Optional .env vars
INTERVAL = os.getenv("INTERVAL", 60)
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", None)

if TOKEN is None:
    raise Exception("No BOT_TOKEN set in the .env file.")
elif REPO_OWNER is None:
    raise Exception("No REPO_OWNER set in the .env file.")
elif REPO_NAME is None:
    raise Exception("No REPO_NAME set in the .env file.")
elif COUNTER_CHANNEL is None:
    raise Exception("No COUNTER_CHANNEL set in the .env file.")
elif GITHUB_API_KEY is None:
    print("Warning: No GitHub API key. You will be limited to 60 requests per \
hour.")

bot = hikari.GatewayBot(token=TOKEN)
request_link = 'https://api.github.com/repos/'\
               + REPO_OWNER + '/' + REPO_NAME + '/releases'


@bot.listen()
async def fetch_download_stats(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.startswith(".stats"):
        # TODO: Fetch the latest download info stats from the GitHub API
        total_download_count = 0

        r = requests.get(request_link)
        releases = r.json()

        for release in releases:
            if "assets" in release:
                total_download_count += release["assets"][0]["download_count"]

        await event.message.respond(f"{REPO_NAME} has received over \
{total_download_count} downloads!")


def main(debug=False) -> int:

    if not debug:
        bot.run()

    return 0


if __name__ == "__main__":
    exit(main())
