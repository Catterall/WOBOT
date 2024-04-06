"""
Shooterspool - SPTypes.py
A namespace for types relating to Shooterspool, such as BGT values.

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 02:20 GMTs
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
