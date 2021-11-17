import os
import hikari
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN", None)

if bot_token is None:
    raise Exception("No BOT_TOKEN set in the .env file.")

bot = hikari.GatewayBot(token=bot_token)


@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return

    if event.content.startswith("hk.ping"):
        await event.message.respond("Pong!")


def main() -> int:
    bot.run()
    return 0


if __name__ == "__main__":
    exit(main())
