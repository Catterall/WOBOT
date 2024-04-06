"""
WOBOT - main.py
WOBOT, the "World Online Billiards" Discord Server Bot

Created & Maintained by XORBit
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import asyncio.proactor_events as ape
import logging
import os

import discord
from dotenv import load_dotenv

import bot.wobot as wobot
import utils.async_utils as au
import utils.log_utils as lu


def main():
    logger = logging.getLogger('discord')
    logger.handlers = []

    load_dotenv()

    try:
        TOKEN = os.getenv("DISCORD_BOT_SECRET")
        APP_ID = os.getenv("DISCORD_APP_ID")
        PREFIX = os.getenv("DISCORD_BOT_PREFIX")

        wb = wobot.Wobot(wobot.Wob(), prefix=PREFIX, app_id=APP_ID)
        wb.run(TOKEN)

    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        lu.serror('Failed to login. Please check the token.')
        raise SystemExit
    except discord.errors.PrivilegedIntentsRequired:
        lu.serror(
            'Privileged intents are required. Please enable them in the development portal.'
        )
        raise SystemExit


if __name__ == '__main__':
    au.silence_event_loop_closed_exception(
        ape._ProactorBasePipeTransport.__del__)
    lu.init('wobot')
    main()
