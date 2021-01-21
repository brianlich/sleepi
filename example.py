import logging
from typing import List
from sleepi.sleepiq import SleepIQ
from aiohttp.client import ClientSession
import asyncio

async def main() -> None:

    """ Create the session """
    async with ClientSession() as websession:
        api = SleepIQ('username', 'password', websession)
        # response = await api.fetch_homeassistant_data()
        # response = await api.turn_on_light(3)
        response = await api.turn_off_light(3)
        # response = await api.get_light_status(3)
        print(response)
asyncio.get_event_loop().run_until_complete(main())
    




