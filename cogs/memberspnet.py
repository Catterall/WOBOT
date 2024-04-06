"""
Wobot - memberspnet.py
A cog for handling commands that involve content from  https://members.shooterspool.net/

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 22:50 GMT
"""

import discord
import discord.app_commands as app_commands
from discord.app_commands import Choice
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

                return
    
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
    
    @app_commands.command(
        name="player-stats",
        description="Get detailed statistics for a player."
    )
    @app_commands.describe(
        player_name='The name of the player to get statistics for.',
        game_mode='The game mode to get statistics for.'
    )
    @app_commands.choices(game_mode=[
        Choice(name="8 Ball", value="8 Ball"),
        Choice(name="9 Ball", value="9 Ball"),
        Choice(name="14.1 Straight Pool", value="14.1 Straight Pool"),
        Choice(name="10 Ball", value="10 Ball"),
        Choice(name="One Pocket", value="One Pocket"),
        Choice(name="Snooker", value="Snooker"),
        Choice(name="Blackball", value="Blackball"),
        Choice(name="Chinese 8 Ball", value="Chinese 8 Ball"),
        Choice(name="Straight Rail Billiards", value="Straight Rail Billiards"),
        Choice(name="1 Cushion Billiards", value="1 Cushion Billiards"),
        Choice(name="3 Cushion Billiards", value="3 Cushion Billiards"),
        Choice(name="Custom Snooker", value="Custom Snooker"),
        Choice(name="6 Reds Snooker", value="6 Reds Snooker"),
        Choice(name="Cowboy Pool", value="Cowboy Pool"),
        Choice(name="Cowboy Snooker", value="Cowboy Snooker"),
        Choice(name="Cowboy Pool (Alternate)", value="Cowboy Pool (Alternate)"),
        Choice(name="Cowboy Snooker (Alternate)", value="Cowboy Snooker (Alternate)")])
    async def player_stats(self, interaction: discord.Interaction, player_name: str, game_mode: Choice[str]):
        await interaction.response.defer(ephemeral=True)

        try:
            stats = await self.bot.cache.cachedValue(self.bot.scraper.pg_viewProfile_stats, player_name)
            user_data = spv.view_profileStats(player_name, stats)

            game_mode_stats: dict = user_data['stats'].get(game_mode.value)

            if not game_mode_stats:
                await interaction.followup.send(f'No {game_mode.name} stats found for player \"{player_name}\".')
                return

            stat_categories = {
                'Performance': ['matchesPlayed', 'matchesWin', 'matchesLost', 'gamesPlayed', 'gamesWin', 'gamesLost', 'totalPoints'],
                'Accuracy': ['ballsPocketed', 'shotsMade', 'totalFouls', 'totalSafeties'],
                'Specials': ['runouts', 'specialBallOnBreak', 'specialBallShots', 'specialBallMade'],
                'Breaks': ['breaks', 'maxBallsBreak', 'ballsOnBreak']
            }
            readable_names = {
                'matchesPlayed': 'Matches Played', 'matchesWin': 'Matches Won', 'matchesLost': 'Matches Lost',
                'gamesPlayed': 'Games Played', 'gamesWin': 'Games Won', 'gamesLost': 'Games Lost',
                'totalPoints': 'Total Points', 'ballsPocketed': 'Balls Pocketed', 'shotsMade': 'Shots Made',
                'totalFouls': 'Total Fouls', 'totalSafeties': 'Total Safeties', 'runouts': 'Runouts',
                'specialBallOnBreak': 'Special Ball on Break', 'specialBallShots': 'Special Ball Shots',
                'specialBallMade': 'Special Ball Made', 'breaks': 'Breaks', 'maxBallsBreak': 'Max Balls on Break',
                'ballsOnBreak': 'Balls on Break'
            }

            all_embeds = []
            
            for category, keys in stat_categories.items():
                embed = discord.Embed(title=f"\"{player_name}\"s {game_mode.name} Stats - {category}", color=discord.Color.blue())
                
                for key in keys:
                    if key in game_mode_stats:
                        readable_name = readable_names.get(key, key)
                        value = game_mode_stats[key]
                        if value is None:
                            value = "N/A"
                        embed.add_field(name=readable_name, value=value, inline=True)
                
                if embed.fields:
                    all_embeds.append(embed)
            
            await interaction.followup.send(embed=all_embeds[0], view=wobot.PaginationView(all_embeds))

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Player Stats',
                description='I do not have permission to post embeds to channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(
                f'Error when attempting to get player stats for player {player_name} for guild {interaction.guild.name}: {e}'
            )
            await interaction.followup.send(f'Error: {e}')


async def setup(bot: wobot.Wobot):
    await bot.add_cog(Memberspnet(bot))
