"""
Wobot - Wobot.py
The "World Online Billiards" Discord Server Bot

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import abc
import asyncio
import itertools
import os
import typing

import aiohttp
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

import shooterspool.spscraper as sps
import shooterspool.spcache as spc

import utils.log_utils as lu


class PaginationView(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0
        
        if self.current_page == 0:
            self.previous.disabled = True
        
        if len(embeds) == 1:
            self.next.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == interaction.message.interaction.user

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            button.disabled = self.current_page == 0
            self.next.disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            button.disabled = self.current_page == len(self.embeds) - 1
            self.previous.disabled = False
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)


class BotType(abc.ABC):

    @abc.abstractmethod
    def extensions(self) -> typing.List[str]:
        """Return a list of extensions to load"""


class Wob(BotType):

    def extensions(self) -> typing.List[str]:
        return ['cogs.memberspnet']


class Wobot(commands.Bot):

    def __init__(self, bot_type: BotType, prefix: str, app_id: str):
        super().__init__(command_prefix=prefix,
                         intents=discord.Intents.all(),
                         application_id=app_id)
        self.bot_type = bot_type
        self.statuses = itertools.cycle(
            ['The World Online Billiards Bot', 'developed by xorbit64'])
        self.session = aiohttp.ClientSession()
        self.remove_command('help')

        self.scraper = sps.SPScraper() 
        self.cache = spc.SPCache(1800)

        self.loggedInMSP = False

    async def setup_hook(self):
        tasks = [
            self.load_extension(ext) for ext in self.bot_type.extensions()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                lu.serror(f'Failed to load extension: {result}')
                raise result

    async def on_ready(self):
        try:
            pass
            # await self.tree.sync()
        except discord.errors.NotFound:
            lu.scritical(
                'Failed to sync tree. Please check the application ID.')
            raise discord.errors.NotFound
        print("Wobot Ready!")
        self.change_status.start()
        self.scraperLogin.start()

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.statuses)))
    
    @tasks.loop(minutes=30)
    async def scraperLogin(self):
        if self.loggedInMSP:
            await self.scraper.logout(close_session=False)

        await self.scraper.login(os.getenv('SHOOTERSPOOL_EMAIL'), os.getenv('SHOOTERSPOOL_PASSWORD'))
        self.loggedInMSP = True
    
    async def on_disconnect(self):
        if self.loggedInMSP:
            await self.scraper.logout()
        await self.session.close()
