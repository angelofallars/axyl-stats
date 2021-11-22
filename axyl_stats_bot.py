import os

import hikari
import psycopg2 as pgres
from dotenv import load_dotenv

load_dotenv()
# Required .env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
COUNTER_CHANNEL = os.getenv("COUNTER_CHANNEL")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")

DB_NAME = os.getenv("DB_NAME")

# Optional .env vars
INTERVAL = os.getenv("INTERVAL", 60)
PREFIX = os.getenv("BOT_PREFIX", ".stats")

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

repo_full_name = REPO_OWNER + '/' + REPO_NAME

bot = hikari.GatewayBot(token=BOT_TOKEN)

# Initialize the connection to the PostgreSQL db
connection = pgres.connect(database=DB_NAME,
                           user=DB_USER,
                           password=DB_PASS,
                           host=DB_HOST,
                           port=DB_PORT)

# Initialize the cursor
cursor = connection.cursor()


info_commands = {
                 "stats":
                 """`{repo_name}` stats:
**⬇️ Downloads (Total)**
`{total_downloads}`
**🔥 Downloads (Latest Release)**
`{latest_downloads}`
**⭐ Stars**
`{stars}`
**🌱 Forks**
`{forks}`
**🔭 Watchers**
`{watchers}`""",

                 "downloads":
                 """**⬇️ Downloads (Total)** - `{repo_name}`
`{total_downloads}`
**🔥 Downloads (Latest Release)**
`{latest_downloads}`""",

                 "stars":
                 """**⭐ Stars** - `{repo_name}`
`{stars}`""",

                 "forks":
                 """**🌱 Forks** - `{repo_name}`
`{forks}`""",

                 "watchers":
                 """**🔭 Watchers** - `{repo_name}`
`{watchers}`""",
                 }


def list_help_commands(commands: dict, prefix: str) -> str:
    help_str = "🔎 List of commands:\n"

    for command_name in commands:
        help_str += f"`{prefix} {command_name}`\n"

    # Strip the last new line
    help_str = help_str.rstrip("\n")

    return help_str


def unknown_command() -> str:
    return f"❓ Unknown command. Try `{PREFIX} help` for the list of commands."


def fetch_latest_db_stats(cursor: pgres.extensions.cursor) \
     -> tuple[int, int, int, int, int]:

    cursor.execute("""SELECT total_downloads, latest_downloads,
                          stars, watchers, forks
                      FROM repo_stats
                      ORDER BY date DESC LIMIT 1;""")

    (total_downloads,
     latest_downloads,
     stars,
     watchers,
     forks) = cursor.fetchone()

    return total_downloads, latest_downloads, stars, watchers, forks


@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    if (event.is_bot or not
       event.content or not
       event.content.startswith(PREFIX)):
        return

    args = event.content[1:].split()

    if len(args) > 1:
        (total_downloads,
         latest_downloads,
         stars,
         watchers,
         forks) = fetch_latest_db_stats(cursor)

        if args[1] in info_commands:
            await event.message.respond(info_commands[args[1]]
                                        .format(
                repo_name=repo_full_name,
                total_downloads=total_downloads,
                latest_downloads=latest_downloads,
                stars=stars,
                watchers=watchers,
                forks=forks,
                ))

        elif args[1] == "help":
            await event.message.respond(list_help_commands(info_commands,
                                                           PREFIX))

        else:
            await event.message.respond(unknown_command())

    else:
        await event.message.respond(unknown_command())


def main(debug=False) -> int:

    if not debug:
        bot.run()

    return 0


if __name__ == "__main__":
    exit(main())
