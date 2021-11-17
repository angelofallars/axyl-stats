import os

import hikari
from dotenv import load_dotenv

load_dotenv()
# Required .env vars
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
COUNTER_CHANNEL = os.getenv("COUNTER_CHANNEL", None)
REPO_OWNER = os.getenv("REPO_OWNER", None)
REPO_NAME = os.getenv("REPO_NAME", None)

# Optional .env vars
INTERVAL = os.getenv("INTERVAL", 60)

if BOT_TOKEN is None:
    raise Exception("No BOT_TOKEN set in the .env file.")
elif REPO_OWNER is None:
    raise Exception("No REPO_OWNER set in the .env file.")
elif REPO_NAME is None:
    raise Exception("No REPO_NAME set in the .env file.")
elif COUNTER_CHANNEL is None:
    raise Exception("No COUNTER_CHANNEL set in the .env file.")

bot = hikari.GatewayBot(token=BOT_TOKEN)


@bot.listen()
async def fetch_download_stats(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.startswith(".stats"):
        # TODO: Fetch the latest download info stats from the database
        total_download_count = 0

        await event.message.respond(f"{REPO_NAME} has received over \
{total_download_count} downloads!")


def main(debug=False) -> int:

    if not debug:
        bot.run()

    return 0


if __name__ == "__main__":
    exit(main())
