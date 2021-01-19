from aiohttp.client import ClientSession
import asyncio
from sleepi.api import API

async def main() -> None:
    async with ClientSession() as websession:
        api = API('username', 'password', websession)
        test = await api.fetch_data()
        print (test)

asyncio.get_event_loop().run_until_complete(main())



