""" Define the Sleepi API """
import asyncio
import logging

import aiohttp
from sleepi.models import Bed, FamilyStatus, Foundation, Foundation_Status, Light, Side, Sleeper
from typing import List, Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from datetime import datetime, timedelta
from .exceptions import SleepiConnectionError, SleepiError, SleepiGenericError

BASE_URL = "https://prod-api.sleepiq.sleepnumber.com/rest"

_LOGGER = logging.getLogger(__name__)
DEFAULT_STATE_UPDATE_INTERVAL = timedelta(seconds=5)

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}

RIGHT_NIGHT_STAND = 1
LEFT_NIGHT_STAND = 2
RIGHT_NIGHT_LIGHT = 3
LEFT_NIGHT_LIGHT = 4

BED_LIGHTS = [
        RIGHT_NIGHT_STAND,
        LEFT_NIGHT_STAND,
        RIGHT_NIGHT_LIGHT,
        LEFT_NIGHT_LIGHT
    ]

class API:
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
        self._key = None
        self._first_bed_id: int = None
        
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
        self._key = json_response["key"]
        return True

    async def _request(
        self,
        endpointName: str,
        params: dict,
        method: Optional[str] = None,
        data: Optional[dict] = None,
        ):
        """ Send a REST call to the SleepIQ instance """
        method = "GET" if method is None else "PUT"
        url = BASE_URL + "/" + endpointName
        headers = DEFAULT_HEADERS

        if self._websession is None:
            raise(SleepiGenericError("Generic error"))

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
                # Login
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

    async def bed(self, data) -> Bed:
        """ Get the latest bed information from SleepIQ """
        return Bed.from_dict(data)

    async def beds(self) -> list:
        """ Get the latest bed information from SleepIQ """
        beds = []
        params = {"_k": self._key}
        data = await self._request("bed", params)
        for item in data["beds"]:
            self._first_bed_id = item["bedId"]
            beds.append(Bed.from_dict(item))
        return beds

    async def sleeper(self, data) -> Sleeper:
        """ Get the latest bed information from SleepIQ """
        return Bed.from_dict(data)

    async def sleepers(self):
        """ Sleepers """
        sleepers = []
        params = {"_k": self._key}
        data = await self._request("sleeper", params)
        for side in data["sleepers"]:
            sleepers.append(Sleeper.from_dict(side))
        return sleepers

    async def foundations(self, beds: List):
        """ Foundations """
        foundations = []
        bed: Bed
        for bed in beds:
            endpoint = "bed/" + bed.bedId + "/foundation/system"
            params = {"_k": self._key}
            data = await self._request(endpoint, params)
            foundations.append(Foundation.from_dict(data, bed.bedId))

        return foundations

    async def foundation_status(self, beds: List):
        """ Foundations """
        foundation_status = []

        bed: Bed
        for bed in beds:
            endpoint = "bed/" + bed.bedId + "/foundation/status"
            params = {"_k": self._key}
            data = await self._request(endpoint, params)
            foundation_status.append(Foundation_Status.from_dict(data, bed.bedId))

        return foundation_status

    async def family_status(self):
        """ Family status """
        family_status = []
        params = {"_k": self._key}
        data: FamilyStatus = await self._request("bed/familyStatus", params)
        family_status.append(Side.from_dict(data["beds"][0]["leftSide"], "left", data["beds"][0]["bedId"]))
        family_status.append(Side.from_dict(data["beds"][0]["rightSide"], "right", data["beds"][0]["bedId"]))
        return family_status

    async def lights(self, beds: List):
        """ A collection of lights """
        lights = []

        bed: Bed
        for bed in beds:
            endpoint = "bed/" + bed.bedId + "/foundation/outlet"

            for light in BED_LIGHTS:
                params = {"_k": self._key, "outletId": light}
                data = await self._request(endpoint, params)

                if data is not None:
                    lights.append(Light.from_dict(data))

        return lights

    async def light(self, data):
        """ A light """
        return Light.from_dict(data)

    def __feature_check(self, value, digit):
        return ((1 << digit) & value) > 0

    async def foundation_features(self, beds: List):
        """ Foundation features """
        foundation_features = []

        bed: Bed
        for bed in beds:
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

            data["bedId"] = bed.bedId
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

    async def fetch_data(self):
        """ Fetch the latest data from SleepIQ """
        try:
            await self.login()
            family_status = await self.family_status()
            beds = await self.beds()
            sleepers = await self.sleepers()
            lights = await self.lights(beds)
            foundations = await self.foundations(beds)
            foundation_status = await self.foundation_status(beds)

            bed: Bed
            family_status: FamilyStatus
            sleeper: Sleeper
            side: Side
            light: Light
            foundation: Foundation
            foundation_status: Foundation_Status
            for bed in beds:
                for light in lights:
                    if bed.bedId == light.bedId:
                        bed.lights.append(light)
                for foundation in foundations:
                    if bed.bedId == foundation.bedId:
                        bed.foundation = foundation
                for status in foundation_status:
                    if bed.bedId == status.bedId:
                        bed.foundation.status = status
                for side in family_status:
                    if bed.bedId == side.bedId:
                        if side.side.lower() == "left":
                            bed.left_side = side
                            for sleeper in sleepers:
                                if bed.sleeperLeftId == sleeper.sleeperId:
                                    side.sleeper = sleeper
                        if side.side.lower() == "right":
                            bed.right_side = side
                            for sleeper in sleepers:
                                if bed.sleeperRightId == sleeper.sleeperId:
                                    side.sleeper = sleeper
            foundation_features = await self.foundation_features(beds)
            for bed in beds:
                for foundation_feature in foundation_features:
                    if bed.bedId == foundation_feature["bedId"]:
                        bed.foundation.features = foundation_feature
            
            return beds
        except:
            raise
            # raise SleepiGenericError(logging.exception)


