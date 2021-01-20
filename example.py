import logging
from typing import List
from sleepi import API
from aiohttp.client import ClientSession
import asyncio

async def main() -> None:

    """ Create the session """
    async with ClientSession() as websession:
        api = API('username', 'passsword', websession)
        results = await api.fetch_data()
    i: int = 1

asyncio.get_event_loop().run_until_complete(main())
    




