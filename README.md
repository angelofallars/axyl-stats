# Axyl Stats

Axyl Stats is a Discord bot made with Hikari, used as a download counter for a
GitHub repo.

This bot is used to check the download stats of a particular repo either with a
bot command (`.stats`) or automatically in a set interval.

The interval, repo owner and repo name to fetch is set in the environment variables.

## Setting Up

`Python 3.8` and above is required. PostgreSQL must also be installed and set
up.

First, clone this repo:

`git clone https://github.com/angelofallars/axyl-stats`

Then, change directories into the repo and install the required dependencies:

```bash
cd axyl-stats
python3 -m pip install -r requirements.txt
```

In the same directory, make a `.env` file and put the bot token and repo info
in there.

The environment variables that Axyl Stats will use are:

- `BOT_TOKEN`: The Discord bot's API token. Make a new Discord application in
the [Discord Dev Portal](https://discord.com/developers) and create a bot for
it. You will see the copyable token.
- `GITHUB_API_KEY` (optional): The GitHub API key for requesting data. If you don't
have an API key, you'll be limited to 60 requests per hour.
- `REPO_OWNER`: The owner of the repo.
- `REPO_NAME`: The name of the repo.
- `INTERVAL` (optional, default `60`): The interval in minutes in which the bot will fetch the download stats.
- `COUNTER_CHANNEL`: The Discord channel(s) to send statistics to. Multiple
channels are separated with a comma (,).

Example:

### `.env` file

```env
BOT_TOKEN=<your token>
GITHUB_API_KEY=<api key>
REPO_OWNER=axyl-os
REPO_NAME=axyl-iso
INTERVAL=60
COUNTER_CHANNEL=axyl-statistics
```

After you're done setting up, run the Discord bot with `python3 axyl_stats.py`.

## Testing

To be able to unit test the bot, you must also specify a `TEST_BOT_TOKEN` in the .env
file.

## Database

To run the database testing, you must also put in the `.env` file:

### Required

- `DB_NAME`: The database to log to
have an API key, you'll be limited to 60 requests per hour.
- `REPO_OWNER`: Ditto.
- `REPO_NAME`: Ditto.

### Optional

- `GITHUB_API_KEY` (optional): Ditto.
- `DB_USER`: The user that will log in
- `DB_PASS`: The database password
- `DB_HOST` (default `127.0.0.1`): The host IP address
- `DB_PORT` (default `5432`): The port of the PostgreSQL database
- `DB_UPDATE_INTERVAL` (default `5`): The interval (in minutes) to update the
database
