import os
import hikari
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", None)
REPO_OWNER = os.getenv("REPO_OWNER", None)
REPO_NAME = os.getenv("REPO_NAME", None)
INTERVAL = os.getenv("INTERVAL", 60)
COUNTER_CHANNEL = os.getenv("COUNTER_CHANNEL", None)
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

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


@bot.listen()
async def fetch_download_stats(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.startswith(".stats"):
        # TODO: Fetch the latest download info stats from a PostgreSQL db
        await event.message.respond("AXYL STATS")


def main(debug=False) -> int:

    if not debug:
        bot.run()

    return 0


if __name__ == "__main__":
    exit(main())
