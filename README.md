# WOBOT

WOBOT is the Discord bot currently in development for the [World Online Billiards discord server](https://discord.com/invite/2xtEBjEPKf).

## Cogs

| Cog          | Description                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------------------- |
| memberspnet  | A cog for handling commands that involve content from  [members.shooterspool.net](https://members.shooterspool.net/) |


## Commands

| Command         | Cog         | Type  | Args              | Description                                                                                                      |
| --------------- | ----------- | ----- | ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| player-overview | memberspnet | slash | player_name (str) | displays an embed overview of a player, including match results for BGT groups.                                  |
| player-stats    | memberspnet | slash | player_name (str), game_mode (str) | displays performance, accuracy, special, and break stats for a specific game mode for a player. |
