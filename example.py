import logging
from typing import List
from sleepi.sleepiq import SleepIQ
from aiohttp.client import ClientSession
import asyncio

async def main() -> None:

    """ Create the session """
    async with ClientSession() as websession:
        api = SleepIQ('username', 'password', websession)
        await api.login()
        # response = await api.fetch_homeassistant_data()
        # response = await api.turn_on_light(3)
        # response = await api.turn_off_light(3)
        # response = await api.get_light_status(3)
        # response = await api.get_favorite_sleepnumber()
        # response = await api.get_footwarming_status()
        response = await api.get_responsive_air_status()
        # response = await api.set_responsive_air("left", True)
        print(response)
asyncio.get_event_loop().run_until_complete(main())

