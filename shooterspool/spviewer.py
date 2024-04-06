"""
Shooterspool - SPViewer.py
A namespace for viewing Shooterspool data gathered via SPScraper and SPReader

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 04/04/2024 00:02 GMTs
"""

import shooterspool.sptypes as spt


def view_profileOverview(viewProfile_data: dict, bio: str, matchInfo_data: tuple[str, str|None, list[str], list[str], list[dict]]) -> dict:
    """To be fed SPScraper.pg_viewProfile()[0], SPReader.read_viewProfile_bio, SPReader.read_viewProfile_matchInfo !!!

    Returns a presentable dictionary of various data. Present this to end users!
    """
    (globalRating, ratingProgress, lastMatchResults, lastTournamentResults, gameModes) = matchInfo_data

    lastMatchResultsStr = " ".join([result.upper()[0] for result in lastMatchResults])
    lastTournamentResultsStr = " ".join(lastTournamentResults)

    commonGameModes = {}
    for mode in gameModes:
        gameModeName = spt.BGT.get_game_mode(mode['bgt'])
        commonGameModes[gameModeName] = {key: value for key, value in mode.items() if key != 'bgt'}

    result_dict = {
        "userValue": viewProfile_data["value"],
        "flag": viewProfile_data["flag"],
        "username": viewProfile_data["label"],
        "bio": bio,
        "globalRating": globalRating,
        "ratingProgress": ratingProgress,
        "lastMatchResults": lastMatchResultsStr,
        "lastTournamentResults": lastTournamentResultsStr,
        "commonGameModes": commonGameModes,
    }

    return result_dict
