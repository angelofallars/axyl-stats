<h1 align=center>📈 axyl-stats</h1>

`axyl-stats` is a Discord bot made with **Python** (with the Hikari API wrapper) and **PostgreSQL**,
used as a download counter for a GitHub repo.

This bot is used to check the download stats of a particular repo either with a
bot command (`.stats`) ~~or automatically in a set interval~~ (TODO).

Setting up this bot is done through the `.env` environment variables.

## Contents
- [Overview](#overview)
- [Setting Up](#setup)
  - [`axyl-stats.py`](#axyl-bot)
  - [`stats-database.py`](#axyl-db)
- [Running The Bot](#run)
- [Testing](#testing)
- [License](#license)

<a id="overview"></a>
## Overview

Right now, the bot's functionality is like this:

![axyl-stats image](https://i.imgur.com/LNjFNpE.png)

<a id="setup"></a>
## Setting Up

`Python 3.8` and above is required. PostgreSQL must also be installed, set
up with a database and running. axyl-stats will take care of creating and
managing the database table.

First, clone this repo:

```bash
git clone https://github.com/angelofallars/axyl-stats
```

Then, change directories into the repo and install the required dependencies:

```bash
cd axyl-stats
python3 -m pip install -r requirements.txt
```

In the same directory, make a `.env` file and put the bot token and repo info
in there.

The environment variables that axyl-stats will use are:

<a id="axyl-bot"></a>
## `axyl-stats.py`

### Required
- `BOT_TOKEN`: The Discord bot's API token. Make a new Discord application in
the [Discord Dev Portal](https://discord.com/developers) and create a bot for
it. You will see the copyable token.
- `REPO_OWNER`: The owner of the repo.
- `REPO_NAME`: The name of the repo.
- `DB_NAME`: The database to fetch data from.
  - You must create a database in `PostgreSQL` first with the name `DB_NAME` before you can run this app.
- `COUNTER_CHANNEL`: The Discord channel(s) to send automated statistics to. Multiple
channels are separated with a comma (,).

### Optional
- `INTERVAL` (default `60`): The interval in minutes in which the bot will fetch the download stats.
- `DB_USER`: The user logging into the DB.
- `DB_PASS`: The DB password.
- `DB_HOST` (default `127.0.0.1`): The host IP address.
- `DB_PORT` (default `5432`): The port of the DB.

<a id="axyl-db"></a>
## `stats-database.py`

To run the database testing, you must also put in the `.env` file:

### Required

- `DB_NAME`: Ditto.
- `REPO_OWNER`: Ditto.
- `REPO_NAME`: Ditto.

### Optional

- `GITHUB_API_KEY`: The GitHub API key for requesting data. If you don't
have an API key, you'll be limited to 60 requests per hour.
- `DB_USER`: Ditto.
- `DB_PASS`: Ditto.
- `DB_HOST`: Ditto.
- `DB_PORT`: Ditto.
- `DB_UPDATE_INTERVAL` (default `5`): The interval (in minutes) to update the
database.

## `.env` example

### `.env` file

```env
BOT_TOKEN=<your token>
GITHUB_API_KEY=<api key>
REPO_OWNER=axyl-os
REPO_NAME=axyl-iso
INTERVAL=60
COUNTER_CHANNEL=axyl-statistics
DB_NAME=axyl-stats
DB_USER=archie
DB_PASS=hunter2
```

<a id="run"></a>
## Running The Bot

To run the bot:
```bash
python3 axyl_stats.py
```

To run the backend that updates the database with info from the GitHub API:
```bash
python3 stats_database.py
```

## Testing

~~To be able to unit test the bot, you must also specify a `TEST_BOT_TOKEN` in the .env
file.~~ (Tests not yet implemented)

## License

This program is licensed under the GPLv3 License.
