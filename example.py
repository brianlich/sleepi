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
        response = await api.fetch_homeassistant_data()
        # response = await api.turn_on_light(3)
        # response = await api.turn_off_light(3)
        # response = await api.get_light_status(3)
        # response = await api.get_favorite_sleepnumber()
        # response = await api.get_footwarming_status()
        # response = await api.turn_on_foot_warming("right", "med")
        # response = await api.turn_off_foot_warming("right")
        # response = await api.get_responsive_air()
        # response = await api.turn_on_responsive_air("left")
        # response = await api.turn_on_responsive_air("right")
        # response = await api.turn_off_responsive_air("left")
        # response = await api.turn_off_responsive_air("right")
        # response = await api.get_privacy_mode()
        # response = await api.turn_on_privacy_mode()
        # response = await api.turn_off_privacy_mode()
        # response = await api.get_privacy_mode()
        # response = await api.get_sleepnumber("left")
        print(response)
asyncio.get_event_loop().run_until_complete(main())

