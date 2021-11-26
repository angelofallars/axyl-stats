<h1 align=center>📈 axyl-stats</h1>

`axyl-stats` is a suite of programs for tracking and displaying stats and info about a GitHub repo.

One is a Discord bot made with **Python** (with the Hikari API wrapper) and uses **PostgreSQL**,
used as a stats visualizer for a repo. The other is a database program that
fetches info from the GitHub API and puts it in the SQL database.

The bot is used to check the download stats of a particular repo either with a
bot command (`.stats`) ~~or automatically in a set interval~~ (TODO).

Setting up the bot is done through the `.env` environment variables.

![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white) ![Postgres](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) [![Discord](https://img.shields.io/badge/hikari-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white)](https://www.hikari-py.dev/)

## Contents
- [Overview](#overview)
- [Setting Up](#setup)
  - [`axyl_stats_bot.py`](#axyl-bot)
  - [`stats-database.py`](#axyl-db)
- [Running The Bot](#run)
- [Database Schema](#database)
- [Testing](#testing)
- [License](#license)

<a id="overview"></a>
## Overview

Right now, the bot's functionality is like this:

![axyl-stats image](https://user-images.githubusercontent.com/39676098/142674295-40a3a649-551a-43b9-8f76-f60e4cfd2411.png)

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
## `axyl_stats_bot.py`

### Required
- `BOT_TOKEN`: The Discord bot's API token. Make a new Discord application in
the [Discord Dev Portal](https://discord.com/developers) and create a bot for
it. You will see the copyable token.
- `REPO_OWNER`: The owner of the repo.
- `REPO_NAME`: The name of the repo.
- `DB_NAME`: The database to fetch data from.
  - You must create a database in `PostgreSQL` first with the name you will put in `DB_NAME` before you can run this app.
- `COUNTER_CHANNEL`: The Discord channel(s) to send automated statistics to. Multiple
channels are separated with a comma (,).

### Optional
- `BOT_PREFIX` (default `.stats`): The prefix of the bot for commands.
- `INTERVAL` (default `60`): The interval in minutes in which the bot will fetch the download stats.
- `DB_USER`: The user logging into the DB.
- `DB_PASS`: The DB password.
- `DB_HOST` (default `127.0.0.1`): The host IP address.
- `DB_PORT` (default `5432`): The port of the DB.

<a id="axyl-db"></a>
## `axyl_stats_db.py`

To run the database module, you must also put in the `.env` file:

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
python3 axyl_stats_bot.py
```

To run the program that updates the database with info from the GitHub API, you
need to execute:
```bash
python3 axyl_stats_db.py
```

However, this will only create the database (if running for the first time) and
insert only one row of data for the current time. If you want more rows of data,
you need to run the bot again. If you want to periodically fetch data from the
GitHub API every set interval like 10 minutes, 30 minutes or an hour, it is
recommended to use [cron jobs](https://www.hostinger.com/tutorials/cron-job).

<a id="database"></a>
## Database Schema

In the configured database, `axyl_stats_db.py` will create a table called
`repo_stats` with the following columns:

- `repo`: The repository the program is set to fetch data from.
- `total_downloads`: The total number of downloads for every release in the
Releases section.
- `latest_downloads`: The number of downloads for the latest release in
Releases.
- `stars`
- `watchers`
- `forks`
- `date`: The time the data was fetched.

Example table:

```
       repo       | total_downloads | latest_downloads | stars | watchers | forks |        date
------------------+-----------------+------------------+-------+----------+-------+---------------------
 axyl-os/axyl-iso |            1325 |              349 |    56 |       56 |     2 | 2021-11-19 21:50:52
 axyl-os/axyl-iso |            1325 |              349 |    56 |       56 |     2 | 2021-11-19 21:55:53
 axyl-os/axyl-iso |            1325 |              349 |    56 |       56 |     2 | 2021-11-19 22:00:54
 axyl-os/axyl-iso |            1327 |              351 |    56 |       56 |     2 | 2021-11-19 22:05:56
 axyl-os/axyl-iso |            1327 |              351 |    56 |       56 |     2 | 2021-11-19 22:10:57
 axyl-os/axyl-iso |            1327 |              351 |    56 |       56 |     2 | 2021-11-19 22:15:58
```

You can run `axyl_stats_db.py` without having to run the bot program. In fact,
you can just run the database program by itself. You then can access the
PostgreSQL database from another program and perhaps run Matplotlib to visualize
the growth of your repository.

## License

This program is licensed under the GPLv3 License.
