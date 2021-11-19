import os

import hikari
import psycopg2 as pgres
from dotenv import load_dotenv

load_dotenv()
# Required .env vars
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
COUNTER_CHANNEL = os.getenv("COUNTER_CHANNEL", None)
REPO_OWNER = os.getenv("REPO_OWNER", None)
REPO_NAME = os.getenv("REPO_NAME", None)

DB_NAME = os.getenv("DB_NAME", None)

# Optional .env vars
INTERVAL = os.getenv("INTERVAL", 60)

DB_USER = os.getenv("DB_USER", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")

if BOT_TOKEN is None:
    raise Exception("No BOT_TOKEN set in the .env file.")
elif DB_NAME is None:
    raise Exception("Database name (DB_NAME) not set in the '.env' file.")
elif REPO_OWNER is None:
    raise Exception("No REPO_OWNER set in the .env file.")
elif REPO_NAME is None:
    raise Exception("No REPO_NAME set in the .env file.")
elif COUNTER_CHANNEL is None:
    raise Exception("No COUNTER_CHANNEL set in the .env file.")

repo_name_combined = REPO_OWNER + '/' + REPO_NAME

bot = hikari.GatewayBot(token=BOT_TOKEN)

# Initialize the connection to the PostgreSQL db
conn = pgres.connect(database=DB_NAME,
                     user=DB_USER,
                     password=DB_PASS,
                     host=DB_HOST,
                     port=DB_PORT)

# Initialize the cursor
cur = conn.cursor()


@bot.listen()
async def fetch_download_stats(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.startswith(".stats"):
        # Fetch the latest download info stats from the database
        cur.execute("""SELECT total_downloads FROM repo_stats
                       ORDER BY date DESC LIMIT 1;""")

        total_download_count = cur.fetchone()[0]

        await event.message.respond(f"`{repo_name_combined}` has received \
over {total_download_count} downloads!")


def main(debug=False) -> int:

    if not debug:
        bot.run()

    return 0


if __name__ == "__main__":
    exit(main())
