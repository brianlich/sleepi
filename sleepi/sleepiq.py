""" Define the Sleepi API """
import asyncio
import logging
import aiohttp

from .const import (
    BED_LIGHTS,
)
from .exceptions import SleepiConnectionError, SleepiError, SleepiGenericError
from .models import Bed, FamilyStatus, FootWarming, Foundation, Foundation_Status, Light, PrivacyMode, Responsive_Air, Side, Sleeper

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from datetime import timedelta
from typing import Dict, Optional


BASE_URL = "https://prod-api.sleepiq.sleepnumber.com/rest"
DEFAULT_STATE_UPDATE_INTERVAL = timedelta(seconds=5)
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
_LOGGER = logging.getLogger(__name__)

LEFT = "left"
RIGHT = "right"
LEFT_SIDE = ["l", LEFT]
RIGHT_SIDE = ["r", RIGHT]
BOTH_SIDES = [LEFT_SIDE, RIGHT_SIDE]

HEAD = ['h', 'head']
FOOT = ['f', 'foot']

FAVORITE = 1
READ = 2
WATCH_TV = 3
FLAT = 4
ZERO_G = 5
SNORE = 6

BED_PRESETS = [
        FAVORITE,
        READ,
        WATCH_TV,
        FLAT,
        ZERO_G,
        SNORE
    ]

class SleepIQ:
    """ Define a class for interacting with the SleepIQ REST APIs """
    def __init__(
        self,
        username: str,
        password: str,
        websession: ClientSession
        ):
        """ Initialize """
        self._username = username
        self._password = password
        self._websession = websession
        self._bedId: str = None
        self._key = None

    async def login(self):
        """ Log into the API """
        if not self._username or not self._password:
            raise ValueError("username/password not set")
        
        data = {'login': self._username, 'password': self._password}
        response = await self._websession.put(
            BASE_URL+'/login',
            json=data,
            headers=DEFAULT_HEADERS
            )

        if response.status == 401:
            raise ValueError("HTTP Error 401: Incorect username or password")
        elif response.status == 502:  # 502 Session Invalid
            await self.login()
            _LOGGER.error("HTTP error 502: Session is invalid") 
        elif response.status == 503:  # 503 Server Error
            await response.raise_for_status()
            _LOGGER.error("HTTP error 503: Server error") 
        elif response.status == 400:  # 400 bad request
            await response.raise_for_status()
            _LOGGER.error("HTTP error 400: Bad request") 
        
        json_response = await response.json()

        if json_response["key"] is not None:
            self._key = json_response["key"]
            # await self.get_bed_id()
            return True
        else:
            return False

    async def __request(
        self,
        endpointName: str,
        params: Optional[dict] = {},
        method: Optional[str] = None,
        data: Optional[dict] = None,
        ):
        """ Send a REST call to the SleepIQ instance """
        method = "GET" if data is None else "PUT"
        url = BASE_URL + "/" + endpointName
        headers = DEFAULT_HEADERS

        if self._websession is None:
            raise(SleepiGenericError("Generic error"))

        if self._key is None:
            login = await self.login()
            if login:
                if '_k' not in params:
                    params["_k"] = self._key
            else:
                raise SleepiGenericError("There is no token attached to this request")
        else:
            params["_k"] = self._key

        print(f"Querying {url} with key: {self._key}")

        try:
            response = await self._websession.request(
                method,
                url,
                json=data,
                headers=headers,
                params=params
            )
            if response.status == 404: # 404 page not found
                if "foundation/outlet" in url:
                    return None
                else:
                    await self.login()
                    _LOGGER.error("Http error 404: Not found") 
            if response.status == 401: # 401 Unauthorized
                _LOGGER.error("HTTP error 401: Unauthorized") 
                await self.login()
            elif response.status == 502:  # 502 Session Invalid
                await self.login()
                _LOGGER.error("HTTP error 502: Session is invalid") 
            elif response.status == 503:  # 503 Server Error
                await response.raise_for_status()
                _LOGGER.error("HTTP error 503: Server error") 
            elif response.status == 400:  # 400 bad request
                _LOGGER.error("HTTP error 400: Bad request")
                await response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise SleepiConnectionError(
                "Timeout occurred while connecting to the SleepIQ servers"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
        ) as exception:
            raise SleepiConnectionError(
                "Error occurred while communicating with the SleepIQ servers"
            )

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise SleepiError(
                "Unexpected response from the SleepIQ servers",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def get_privacy_mode(self):
        """ Get the status of privacy mode """
        endpoint = "bed/" + self._bedId + "/pauseMode"
        data = await self.__request(endpoint)
        return PrivacyMode.from_dict(data)

    async def turn_on_privacy_mode(self):
        """ Get the status of privacy mode """
        endpoint = "bed/" + self._bedId + "/pauseMode"
        data = {}
        params = {"mode": "on"}
        return await self.__request(endpoint, data=data, params=params)

    async def turn_off_privacy_mode(self):
        """ Get the status of privacy mode """
        endpoint = "bed/" + self._bedId + "/pauseMode"
        data = {}
        params = {"mode": "off"}
        return await self.__request(endpoint, data=data, params=params)

    async def get_responsive_air(self):
        """ Responsive air status """
        endpoint = "bed/" + self._bedId + "/responsiveAir"
        data = await self.__request(endpoint)
        return Responsive_Air.from_dict(data)

    async def turn_on_responsive_air(self, side: str):
        """ Set responsive air """
        data = None
        if side.lower() in LEFT_SIDE:
            data = {"leftSideEnabled": True}
        elif side.lower() in RIGHT_SIDE:
            data = {"rightSideEnabled": True}

        endpoint = "bed/" + self._bedId + "/responsiveAir"
        return await self.__request(endpoint, data=data)

    async def turn_off_responsive_air(self, side: str):
        """ Set responsive air """
        data = None
        if side.lower() in LEFT_SIDE:
            data = {"leftSideEnabled": False}
        elif side.lower() in RIGHT_SIDE:
            data = {"rightSideEnabled": False}

        endpoint = "bed/" + self._bedId + "/responsiveAir"
        return await self.__request(endpoint, data=data)

    async def get_sleepers(self):
        """ Sleepers """
        sleepers = []
        data = await self.__request("sleeper")
        for side in data["sleepers"]:
            sleepers.append(Sleeper.from_dict(side))
        return sleepers

    async def get_footwarming(self):
        """ Foot warming """
        endpoint = "bed/" + self._bedId + "/foundation/footwarming"
        data = await self.__request(endpoint)
        return FootWarming.from_dict(data)

    async def turn_on_foot_warming(self, side, setting, timer=120):
        """ Foot warming """
        data = None
        if side.lower() in LEFT_SIDE:
            if setting == "low":
                data = {"footWarmingTempLeft": 31, "footWarmingTimerLeft": timer}
            elif setting == "medium" or setting == "med":
                data = {"footWarmingTempLeft": 57, "footWarmingTimerLeft": timer}
            elif setting == "low":
                data = {"footWarmingTempLeft": 72, "footWarmingTimerLeft": timer}

        if side.lower() in RIGHT_SIDE:
            if setting == "low":
                data = {"footWarmingTempRight": 31, "footWarmingTimerRight": timer}
            elif setting == "medium" or setting == "med":
                data = {"footWarmingTempRight": 57, "footWarmingTimerRight": timer}
            elif setting == "low":
                data = {"footWarmingTempRight": 72, "footWarmingTimerRight": timer}

        endpoint = "bed/" + self._bedId + "/foundation/footwarming"
        return await self.__request(endpoint, data=data)

    async def turn_off_foot_warming(self, side):
        """ Foot warming """
        data = None
        if side.lower() in RIGHT_SIDE:
            data = {"footWarmingTempRight": 0, "footWarmingTimerRight": 120}
        elif side.lower() in LEFT_SIDE:
            data = {"footWarmingTempLeft": 0, "footWarmingTimerLeft": 120}

        endpoint = "bed/" + self._bedId + "/foundation/footwarming"
        return await self.__request(endpoint, data=data)

    async def get_foundation_underbed_light(self):
        """ Foundations """
        endpoint = "bed/" + self._bedId + "/foundation/underbedLight"
        data = await self.__request(endpoint)
        return Foundation.from_dict(data)

    async def get_foundation(self):
        """ Foundations """
        endpoint = "bed/" + self._bedId + "/foundation/system"
        data = await self.__request(endpoint)
        return Foundation.from_dict(data)

    async def get_foundation_status(self):
        """ Foundations """
        endpoint = "bed/" + self._bedId + "/foundation/status"
        data = await self.__request(endpoint)
        return Foundation_Status.from_dict(data)

    async def get_family_status(self):
        """ Family status """
        family_status = []
        data: FamilyStatus = await self.__request("bed/familyStatus")
        family_status.append(Side.from_dict(data["beds"][0]["leftSide"], "left"))
        family_status.append(Side.from_dict(data["beds"][0]["rightSide"], "right"))
        return family_status

    async def set_light_brightness(self, lightLevel: str):
        """ """
        if lightLevel.lower() == "high":
            endpoint = "bed/" + self._bedId + "/foundation/system"
            data = {"fsLeftUnderbedLightPWM": 100, "fsRightUnderbedLightPWM": 100}
            await self.__request(endpoint, data=data)
            await self.turn_off_auto_light()
        elif lightLevel.lower() in ('medium', 'med'):
            endpoint = "bed/" + self._bedId + "/foundation/system"
            data = {"fsLeftUnderbedLightPWM": 30, "fsRightUnderbedLightPWM": 30}
            await self.__request(endpoint, data=data)
            await self.turn_off_auto_light()
        elif lightLevel.lower() == "low":
            endpoint = "bed/" + self._bedId + "/foundation/system"
            data = {"fsLeftUnderbedLightPWM": 1, "fsRightUnderbedLightPWM": 1}
            await self.__request(endpoint, data=data)
            await self.turn_off_auto_light()
        elif lightLevel.lower() == "off":
            self.turn_off_light()

    async def turn_on_auto_light(self):
        """ """
        endpoint = "bed/" + self._bedId + "/foundation/underbedLight"
        data = {"enableAuto": True}
        await self.__request(endpoint, data=data)

    async def turn_off_auto_light(self):
        """ """
        endpoint = "bed/" + self._bedId + "/foundation/underbedLight"
        data = {"enableAuto": False}
        await self.__request(endpoint, data=data)

    async def turn_on_light(
        self,
        outletID: int,
        lightLevel: str = ""
        ):
        """ Turn on a light """
        if lightLevel.lower() == "auto":
            await self.turn_on_auto_light()
        else:
            await self.set_light_brightness(lightLevel)

        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        data = {"outletId": outletID, "setting": 1}
        await self.__request(endpoint, data=data)

    async def turn_off_light(
        self,
        outletID: int,
        ):
        """ Turn off a light """
        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        data = {"outletId": outletID, "setting": 0}
        await self.__request(endpoint, data=data)

    async def get_light_status(
        self,
        outletID: int = 0,
        lightLevelData: int = 0,
        ):
        """ Get the status of a light """
        # endpoint = "bed/" + self._bedId + "/foundation/system"
        # lightLevelData = await self.__request(endpoint)
        lights = []

        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        if outletID == 0:
            for light in range(1, 5):
                params = {"outletId": light}
                data = await self.__request(endpoint, params)
                name = f"Sleep Number light {light}"
                lights.append(Light.from_dict(data, name, lightLevelData, True))
        else:
                params = {"outletId": outletID}
                data = await self.__request(endpoint, params)
                name = f"Sleep Number light {outletID}"
                lights.append(Light.from_dict(data, name, lightLevelData, True))

        return lights


        # endpoint = "bed/" + self._bedId + "/foundation/outlet"
        # params = {"outletId": outletID}
        # data = await self.__request(endpoint, params)


        # if outletID == 1:
        #     name = "Sleep Number right night stand"
        # elif outletID == 2:
        #     name = "Sleep Number left night stand"
        # elif outletID == 3:
        #     name = "Sleep Number left night light"
        # elif outletID == 4:
        #     name = "Sleep Number right night light"
        # else:
        #     name = ""
        #     _LOGGER.error("An unknown light was found. OutletID: %s", str(outletID))

        # return Light.from_dict(data, name, lightLevelData["fsLeftUnderbedLightPWM"], True)

    async def get_bed_id(self) -> str:
        data = await self.__request("bed")
        self._bedId = str(data["beds"][0]["bedId"])
        return str(data["beds"][0]["bedId"])

    async def get_bed(self) -> Bed:
        """ Get the latest bed information from SleepIQ """
        data = await self.__request("bed")
        self._bedId = str(data["beds"][0]["bedId"])
        return Bed.from_dict(data)

    async def set_preset_foundation_position(self, preset: int, side: str, slowSpeed = False):
        """ Set a specific side to a preset foundation position """
        # preset 1-6
        # side "R" or "L"
        # slowSpeed False=fast, True=slow
        #
        if side.lower() in RIGHT_SIDE:
            side = "R"
        elif side.lower() in LEFT_SIDE:
            side = "L"
        else:
            raise ValueError("Side mut be one of the following: left, right, L or R")

        if preset in BED_PRESETS:
            data = {'preset':preset,'side':side,'speed':1 if slowSpeed else 0}
            self.__request('/bed/' + self._bedId +'/foundation/preset', data)
            return True
        else:
            raise ValueError("Invalid preset")

    async def set_foundation_position(self, side, actuator, position, slowSpeed=False):
        #
        # side "R" or "L"
        # actuator "H" or "F" (head or foot)
        # position 0-100
        # slowSpeed False=fast, True=slow
        #
        if not 0 <= position <= 100:
            raise ValueError("Invalid position. It must be between 0 and 100")
        if side.lower() in RIGHT_SIDE:
            side = "R"
        elif side.lower() in LEFT_SIDE:
            side = "L"
        else:
            raise ValueError("Side mut be one of the following: left, right, L or R")
        
        if actuator.lower() in HEAD:
            actuator = 'H'
        elif actuator.lower() in FOOT:
            actuator = 'F'
        else:
            raise ValueError("Actuator must be one of the following: head, foot, H or F")

        endpoint = "bed/" + self._bedId + "/foundation/adjustment/micro"
        data = {'position': position, 'side': side, 'actuator': actuator, 'speed': 1 if slowSpeed else 0}
        await self.__request(endpoint, data=data)

    async def get_sleepnumber(self, side):
        """ Return the currently assigned sleep number to a specified side """
        endpoint = "bed/" + self._bedId + "/sleepNumber"
        
        if side.lower() in LEFT_SIDE:
            params = {'side': 'L'}
        elif side.lower() in RIGHT_SIDE:
            params = {'side': 'R'}
        data = await self.__request(endpoint, params=params)
        return data["sleepNumber"] 

    async def set_sleepnumber(self, side: str, setting: int):

        if not 0 <= setting <= 100:
            raise ValueError("Invalid SleepNumber. It must be between 1 and 100")
        if side.lower() in RIGHT_SIDE:
            side = "R"
        elif side.lower() in LEFT_SIDE:
            side = "L"
        else:
            raise ValueError("Side mut be one of the following: left, right, L or R")
        
        endpoint = "bed/" + self._bedId + "/sleepNumber"
        data = {'side': side, "sleepNumber": int(round(setting/5))*5}
        await self.__request(endpoint, data=data)     

    async def get_favorite_sleepnumber(self):
        endpoint = "bed/" + self._bedId + "/sleepNumberFavorite"
        return await self.__request(endpoint)

    async def set_favorite_sleepnumber(self, side: str, setting: int):

        if not 0 <= setting <= 100:
            raise ValueError("Invalid SleepNumber. It must be between 1 and 100")
        if side.lower() in LEFT_SIDE:
            side = "R"
        elif side.lower() in RIGHT_SIDE:
            side = "L"
        else:
            raise ValueError("Side mut be one of the following: left, right, L or R")
        
        endpoint = "bed/" + self._bedId + "/sleepNumberFavorite"
        data = {'side': side, "sleepNumberFavorite": int(round(setting/5))*5}
        await self.__request(endpoint, data=data)

    def __feature_check(self, value, digit):
        return ((1 << digit) & value) > 0

    async def get_foundation_features(self, bed: Bed):
        """ Foundation features """
        foundation_features = []
        board_features: int = bed.foundation.fsBoardFeatures
        bed_type: int = bed.foundation.fsBedType
        data = {}
        if bed_type == 0:
            data['single'] = True
        elif bed_type == 1:
            data['splitHead'] = True
        elif bed_type == 2:
            data['splitKing'] = True
        elif bed_type == 3:
            data['easternKing'] = True

        data['boardIsASingle'] = self.__feature_check(board_features, 0)
        data['hasMassageAndLight'] = self.__feature_check(board_features, 1)
        data['hasFootControl'] = self.__feature_check(board_features, 2)
        data['hasFootWarming'] = self.__feature_check(board_features, 3)
        data['hasUnderbedLight'] = self.__feature_check(board_features, 4)
        data['leftUnderbedLightPMW'] = bed.foundation.fsLeftUnderbedLightPWM
        data['rightUnderbedLightPMW'] = bed.foundation.fsRightUnderbedLightPWM


        if data['hasMassageAndLight']:
            data['hasUnderbedLight'] = True
        if data['splitKing'] or data['splitHead']:
            data['boardIsASingle'] = False

        foundation_features.append(data)
        return foundation_features
    
    async def fetch_homeassistant_data(self) -> Bed:
        """ Fetch the latest data from SleepIQ """
        bed: Bed = await self.get_bed()
        family_status: FamilyStatus = await self.get_family_status()
        sleepers = await self.get_sleepers()
        bed.foundation = await self.get_foundation()
        bed.lights = await self.get_light_status(lightLevelData=bed.foundation.fsLeftUnderbedLightPWM)
        bed.foundation.foundation_status = await self.get_foundation_status()
        bed.foundation.features = await self.get_foundation_features(bed)
        sleep_number_favorite = await self.get_favorite_sleepnumber()
        bed.responsive_air = await self.get_responsive_air()
        bed.privacy_mode = await self.get_privacy_mode()
        bed.foot_warming = await self.get_footwarming()
        side: Side
        sleeper: Sleeper

        for side in family_status:
            if side.side == "left":
                bed.left_side = side
                for sleeper in sleepers:
                    if bed.sleeperLeftId == sleeper.sleeperId:
                        side.sleeper = sleeper
                        side.sleeper.favorite = sleep_number_favorite['sleepNumberFavoriteLeft']
            else:
                bed.right_side = side
                for sleeper in sleepers:
                    if bed.sleeperRightId == sleeper.sleeperId:
                        side.sleeper = sleeper
                        side.sleeper.favorite = sleep_number_favorite['sleepNumberFavoriteRight']

        return bed


