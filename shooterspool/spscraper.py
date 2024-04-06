"""
Shooterspool - SPScraper.py
A namespace for handling the webscraping of https://members.shooterspool.net/

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import asyncio
import httpx
import consts.request_consts as ru
from json.decoder import JSONDecodeError


class SPScraper:
    """A class to handle the scraping of Shooterspool HTML, using async httpx for requests."""

    def __init__(self):
        self.client = httpx.AsyncClient(follow_redirects=True)

    async def login(self, email: str, password: str):
        """Initializes self.client by logging into https://members.shooterspool.net"""
        url = 'https://members.shooterspool.net/index.php?r=site/login'
        login_data = {
            'LoginForm[username]': email,
            'LoginForm[password]': password,
            'LoginForm[device]': 'web',
            'yt0': 'Log in',
            'LoginForm[rememberMe]': '0'
        }
        await self.client.post(url, data=login_data, headers=ru.FORM_URLE_HEADERS)
    
    async def logout(self, close_session: bool = True):
        """Logs out of https://members.shooterspool.net"""
        url = 'https://members.shooterspool.net/index.php?r=site/logout'
        await self.client.post(url, headers=ru.TEXT_HTML_HEADERS)
        if close_session:
            await self.client.aclose()

    async def pg_viewProfile(self, username: str) -> tuple[dict, tuple[str]] | None:
        """Returns a tuple with profile data and HTML page responses for viewing a profile."""
        url = f'https://members.shooterspool.net/getUsers.php?term={username}'
        try:
            r = await self.client.get(url, headers=ru.JSON_HEADERS)
            rjson = r.json()[0]
            url_viewProfile = f'https://members.shooterspool.net/index.php?r=user/viewProfile&id={rjson["value"]}'
            url_overview = f'https://members.shooterspool.net/index.php?r=user/overview&id={rjson["value"]}'

            r1, r2 = await asyncio.gather(
                self.client.get(url_viewProfile, headers=ru.TEXT_HTML_HEADERS),
                self.client.get(url_overview, headers=ru.TEXT_HTML_HEADERS)
            )

            if (r1.status_code == 200 or r1.status_code == 302) and (r2.status_code == 200 or r2.status_code == 302):
                return (rjson, (r1.text, r2.text))
            return None

        except JSONDecodeError:
            return None
