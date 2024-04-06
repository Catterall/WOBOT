"""
Wobot - memberspnet.py
A cog for handling commands that involve content from  https://members.shooterspool.net/

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import shooterspool.spreader as spr
import shooterspool.spviewer as spv

import bot.wobot as wobot
import utils.log_utils as lu


class Memberspnet(commands.Cog):

    def __init__(self, bot: wobot.Wobot):
        self.bot: wobot.Wobot = bot

    @app_commands.command(
        name='player-overview',
        description='Get a simple overview of a player - only includes their common game modes!')
    @app_commands.describe(
        player_name='The name of the player to get an overview of.')
    async def player_overview(self, interaction: discord.Interaction,  player_name: str):
            await interaction.response.defer(ephemeral=True)
    
            try:
                viewProfile = await self.bot.cache.cachedValue(self.bot.scraper.pg_viewProfile, player_name)
                bio = spr.read_viewProfile_bio(viewProfile[1][0])
                matchInfo = spr.read_viewProfile_matchInfo(viewProfile[1][1])
                user_data = spv.view_profileOverview(viewProfile[0], bio, matchInfo)

                general_info_embed = discord.Embed(
                    title=f"{user_data['username']} :flag_{user_data['flag'].lower()}:",
                    description=f"A brief overview of \"{user_data['username']}\"s profile.",
                    color=discord.Color.blue()
                )
                general_info_embed.add_field(name="Bio", value=user_data['bio'], inline=False)
                general_info_embed.add_field(name="Global Rating", value=user_data['globalRating'], inline=True)
                rating_progress = "MAXED" if user_data['ratingProgress'] is None else user_data['ratingProgress']
                general_info_embed.add_field(name="Rating Progress", value=rating_progress, inline=True)
                general_info_embed.add_field(name="Last Match Results", value=user_data['lastMatchResults'], inline=False)
                general_info_embed.add_field(name="Last Tournament Results", value=user_data['lastTournamentResults'], inline=False)

                game_mode_embeds = []
                for mode, stats in user_data['commonGameModes'].items():
                    embed = discord.Embed(
                        title=f"{mode} Stats",
                        description=f"Statistics for {mode}.",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Games Played", value=stats['gamesPlayed'], inline=True)
                    embed.add_field(name="Games Won", value=stats['gamesWin'], inline=True)
                    embed.add_field(name="Matches Played", value=stats['matchesPlayed'], inline=True)
                    embed.add_field(name="Matches Won", value=stats['matchesWin'], inline=True)
                    game_mode_embeds.append(embed)

                all_embeds = [general_info_embed] + game_mode_embeds

                await interaction.followup.send(embed=all_embeds[0], view=wobot.PaginationView(all_embeds))

                return True
    
            except discord.errors.Forbidden:
                embed = discord.Embed(
                    title='Player Overview',
                    description=
                    'I do not have permission to post embeds to channels.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)
    
            except Exception as e:
                lu.swarning(
                    f'Error when attempting to get player overview for player {player_name} for guild {interaction.guild.name}: {e}'
                )
                await interaction.followup.send(f'Error: {e}')


async def setup(bot: wobot.Wobot):
    await bot.add_cog(Memberspnet(bot))
