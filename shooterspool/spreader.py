"""
Shooterspool - SPReader.py
A namespace for handling the reading of https://members.shooterspool.net/ HTML scraped via SPScraper

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import html2text
import json
import re
from bs4 import BeautifulSoup
from functools import lru_cache


@lru_cache(maxsize=128)
def read_viewProfile_bio(html: str) -> str:
    """To be fed SPScraper.pg_viewProfile(username)[1][0] !!!

    Returns the users bio.
    """
    soup = BeautifulSoup(html, 'lxml')
    bio_div = soup.find('div', class_='bio').encode_contents().decode('utf-8')
    converter = html2text.HTML2Text()
    converter.wrap_links = False
    content = converter.handle(bio_div)
    return content


@lru_cache(maxsize=128)
def read_viewProfile_matchInfo(html: str) -> tuple[str, str|None, list[str], list[str], list[dict]]:
    """To be fed SPScraper.pg_viewProfile(username)[1][1] !!!

    Returns a tuple. 
    
    - The first value is the string global rating.
    - The second value WIP.
    - The third value is a list of ten previous match results, oldest to newest.
    - The fourth value is a list of five previous tournament results, oldest to newest.
    - The fifth value is a dictionary containing data for the user's most common game modes.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    global_rating = soup.find('div', class_='stat-value').text

    try:
        rating_progress = soup.find('div', class_='row').find('span', class_='stat-value').next_sibling.strip()
    except AttributeError:
        rating_progress = None
    
    match_results_div = soup.find('div', class_='lastResults match')
    match_results = ['win' if 'winner' in div.get('class') else 'loss' for div in match_results_div.find_all('div')]
    
    tournament_results_div = soup.find('div', class_='lastResults tournament')
    tournament_results = [div.text for div in tournament_results_div.find_all('div') if 'not-played' not in div.get('class')]


    script_text = ''
    for script in soup.find_all('script'):
        if 'totalStats' in script.text:
            script_text = script.text
            break
    
    total_stats_match = re.search(r'var totalStats = (\[.*?\]);', script_text, re.DOTALL)
    if total_stats_match:
        total_stats_json_str = total_stats_match.group(1)
        total_stats = json.loads(total_stats_json_str)
    else:
        total_stats = None

    return (global_rating, rating_progress, match_results, tournament_results, total_stats)
