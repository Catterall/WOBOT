"""
Shooterspool - SPTypes.py
A namespace for types relating to Shooterspool, such as BGT values.

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 18:15 GMTs
"""

from enum import Enum


class BGT(Enum):
    """
    BGT Values

    For https://members.shooterspool.net/index.php?r=user/overview&id=<ID>,
    the totalStats variable is a JSON containing player data for various
    game modes. Each of these game modes appear to have a special "BGT" index.

    """
    US_POOL = '1' 
    SNOOKER = '2'
    BRITISH_POOL = '4'
    CHINESE_POOL = '8'
    CAROM_AND_BILLIARDS = '16'

    @classmethod
    def get_game_mode(cls, value):
        name_mapping = {
            cls.US_POOL: "US Pool",
            cls.SNOOKER: "Snooker",
            cls.BRITISH_POOL: "British Pool",
            cls.CHINESE_POOL: "Chinese Pool",
            cls.CAROM_AND_BILLIARDS: "Carom & Billiards",
        }
        for game_mode in cls:
            if game_mode.value == value:
                return name_mapping.get(game_mode, "Unknown")
        return "Unknown"


class Rules(Enum):
    """
    Rule Values

    Shooterspool categorises each individual game mode as a "rule". For example,
    8 ball is rule 1, 9 ball is rule 2, etc. etc.
    """
    EIGHT_BALL = '1'
    NINE_BALL = '2'
    FOURTEEN_ONE_STRAIGHT_POOL = '3'
    TEN_BALL = '4'
    ONE_POCKET = '5'
    SNOOKER = '6'
    BLACKBALL = '7'
    CHINESE_EIGHT_BALL = '8'
    STRAIGHT_RAIL_BILLIARDS = '9'
    ONE_CUSHION_BILLIARDS = '10'
    THREE_CUSHION_BILLIARDS = '11'
    SNOOKER_CUSTOM = '12'
    SNOOKER_SIX_REDS = '13'
    COWBOY_POOL = '14'
    COWBOY_SNOOKER = '15'
    COWBOY_POOL_ALTERNATE = '16'
    COWBOY_SNOOKER_ALTERNATE = '17'

    @classmethod
    def get_rule_name(cls, value):
        name_mapping = {
            cls.EIGHT_BALL: "8 Ball",
            cls.NINE_BALL: "9 Ball",
            cls.FOURTEEN_ONE_STRAIGHT_POOL: "14.1 Straight Pool",
            cls.TEN_BALL: "10 Ball",
            cls.ONE_POCKET: "One Pocket",
            cls.SNOOKER: "Snooker",
            cls.BLACKBALL: "Blackball",
            cls.CHINESE_EIGHT_BALL: "Chinese 8 Ball",
            cls.STRAIGHT_RAIL_BILLIARDS: "Straight Rail Billiards",
            cls.ONE_CUSHION_BILLIARDS: "1 Cushion Billiards",
            cls.THREE_CUSHION_BILLIARDS: "3 Cushion Billiards",
            cls.SNOOKER_CUSTOM: "Custom Snooker",
            cls.SNOOKER_SIX_REDS: "6 Reds Snooker",
            cls.COWBOY_POOL: "Cowboy Pool",
            cls.COWBOY_SNOOKER: "Cowboy Snooker",
            cls.COWBOY_POOL_ALTERNATE: "Cowboy Pool (Alternate)",
            cls.COWBOY_SNOOKER_ALTERNATE: "Cowboy Snooker (Alternate)",
        }
        for rule in cls:
            if rule.value == value:
                return name_mapping.get(rule, "Unknown")
