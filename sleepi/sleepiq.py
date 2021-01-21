""" Define the Sleepi API """
import asyncio
import logging
import aiohttp

from .const import (
    BED_LIGHTS,
)
from .exceptions import SleepiConnectionError, SleepiError, SleepiGenericError
from .models import Bed, FamilyStatus, Foundation, Foundation_Status, Light, Side, Sleeper

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from datetime import timedelta
from typing import Optional


BASE_URL = "https://prod-api.sleepiq.sleepnumber.com/rest"
DEFAULT_STATE_UPDATE_INTERVAL = timedelta(seconds=5)
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
_LOGGER = logging.getLogger(__name__)

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
            raise ValueError("Incorect username or password")
        
        json_response = await response.json()

        if json_response["key"] is not None:
            self._key = json_response["key"]
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
                raise SleepiGenericError("Help")
        else:
            params["_k"] = self._key

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
                    self.login()
            if response.status == 401: # 401 Unauthorized
                self.login()
            elif response.status == 502:  # 502 Session Invalid
                self.login()
            elif response.status == 503:  # 503 Server Error
                response.raise_for_status()
            elif response.status == 400:  # 400 bad request
                response.raise_for_status()
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

    async def get_sleepers(self):
        """ Sleepers """
        sleepers = []
        data = await self.__request("sleeper")
        for side in data["sleepers"]:
            sleepers.append(Sleeper.from_dict(side))
        return sleepers

    async def get_foundation(self, bed: Bed):
        """ Foundations """
        endpoint = "bed/" + bed.bedId + "/foundation/system"
        data = await self.__request(endpoint)
        return Foundation.from_dict(data)

    async def get_foundation_status(self, bed: Bed):
        """ Foundations """
        endpoint = "bed/" + bed.bedId + "/foundation/status"
        data = await self.__request(endpoint)
        return Foundation_Status.from_dict(data)

    async def get_family_status(self):
        """ Family status """
        family_status = []
        data: FamilyStatus = await self.__request("bed/familyStatus")
        family_status.append(Side.from_dict(data["beds"][0]["leftSide"], "left"))
        family_status.append(Side.from_dict(data["beds"][0]["rightSide"], "right"))
        return family_status

    async def turn_on_light(
        self,
        outletID: int,
        ):
        """ Turn on a light """
        if self._bedId == None:
            await self.get_bed_id()
        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        data = {"outletId": outletID, "setting": 1}
        response = await self.__request(endpoint, data=data)

    async def turn_off_light(
        self,
        outletID: int,
        ):
        """ Turn off a light """
        if self._bedId == None:
            await self.get_bed_id()
        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        data = {"outletId": outletID, "setting": 0}
        response = await self.__request(endpoint, data=data)

    async def get_light_status(
        self,
        outletID: int,
        ):
        """ Get the status of a light """
        if self._bedId == None:
            await self.get_bed_id()

        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        params = {"outletId": outletID}
        data = await self.__request(endpoint, params)

    async def get_bed_id(self):
        data = await self.__request("bed")
        self._bedId = str(data["beds"][0]["bedId"]) 

    async def get_bed(self) -> Bed:
        """ Get the latest bed information from SleepIQ """
        data = await self.__request("bed")
        return Bed.from_dict(data)

    async def toggle_light(
        self,
        outletID: int,
        ):
        """ Get the status of a light """
        status = await self.get_light_status(3)
        if self._bedId == None:
            await self.get_bed_id()
        
        endpoint = "bed/" + self._bedId + "/foundation/outlet"
        data = await self.__request(endpoint)
        if data["setting"] is True:
            self.turn_off_light(3)
        else:
            self.turn_on_light(3)

    async def get_lights(self, bed: Bed):
        """ A collection of lights """
        lights = []
        endpoint = "bed/" + bed.bedId + "/foundation/outlet"

        for light in BED_LIGHTS:
            params = {"outletId": light}
            data = await self.__request(endpoint, params)

            name: str
            if light == 1:
                name = "Sleep Number right nightstand"
            elif light == 2:
                name = "Sleep Number left nightstand"
            elif light == 3:
                name = "Sleep Number left nightlight"
            elif light == 4:
                name = "Sleep Number right nightlight"
            else:
                _LOGGER.debug("An unknown light was found. OutletID: %s", str(light))
                name = ""

            if data is not None:
                lights.append(Light.from_dict(data, name))

        return lights

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
        bed.lights = await self.get_lights(bed)
        foundation: Foundation = await self.get_foundation(bed)
        bed.foundation = foundation
        foundation_status: Foundation_Status = await self.get_foundation_status(bed)
        bed.foundation.foundation_status = foundation_status
        foundation_features = await self.get_foundation_features(bed)
        side: Side
        sleeper: Sleeper

        for foundation_feature in foundation_features:
            bed.foundation.features = foundation_feature

        for side in family_status:
            if side.side == "left":
                bed.left_side = side
                for sleeper in sleepers:
                    if bed.sleeperLeftId == sleeper.sleeperId:
                        side.sleeper = sleeper
            else:
                bed.right_side = side
                for sleeper in sleepers:
                    if bed.sleeperRightId == sleeper.sleeperId:
                        side.sleeper = sleeper

        return bed


