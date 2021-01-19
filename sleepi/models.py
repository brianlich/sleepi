""" Models for Sleepi """
from typing import Any, Dict, List
from attr import dataclass
from distutils.util import strtobool
import json


@dataclass
class Sleeper:
    """ Defines a sleeper """
    firstName: str
    active: bool
    emailValidated: bool
    gender: int
    isChild: bool
    bedId: str
    birthYear: str
    zipCode: str
    timezone: str
    privacyPolicyVersion: int
    duration: int
    weight: int
    sleeperId: str
    firstSessionRecorded: str
    height: int
    licenseVersion: int
    username: str
    birthMonth: int
    birthYear: int
    sleepGoal: int
    accountId: str
    isAccountOwner: bool
    email: str
    lastLogin: str
    side: int

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a bed object from the SleepIQ servers """
        return Sleeper(
            firstName = data["firstName"],
            active = data["active"],
            emailValidated = data["emailValidated"],
            gender = data["gender"],
            isChild = data["isChild"],
            bedId = data["bedId"],
            birthYear = data["birthYear"],
            zipCode = data["zipCode"],
            timezone = data["timezone"],
            privacyPolicyVersion = data["privacyPolicyVersion"],
            duration = data["duration"],
            weight = data["weight"],
            sleeperId = data["sleeperId"],
            firstSessionRecorded = data["firstSessionRecorded"],
            height = data["height"],
            licenseVersion = data["licenseVersion"],
            username = data["username"],
            birthMonth = data["birthMonth"],
            sleepGoal = data["sleepGoal"],
            accountId = data["accountId"],
            isAccountOwner = data["isAccountOwner"],
            email = data["email"],
            lastLogin = data["lastLogin"],
            side = data["side"]
        )

@dataclass
class Side:
    """ Return a side status """
    isInBed: bool
    alertDetailedMessage: str
    sleepNumber: int
    alertId: int
    lastLink: str
    pressure: int
    side: str
    bedId: str
    sleeper: Sleeper

    @staticmethod
    def from_dict(data: Dict[str, Any], left_or_right: str, bedId: str):
        """ Return a bed object from the SleepIQ servers """
        return Side(
            isInBed = data["isInBed"],
            alertDetailedMessage = data["alertDetailedMessage"],
            sleepNumber = data["sleepNumber"],
            alertId = data["alertId"],
            lastLink = data["lastLink"],
            pressure = data["pressure"],
            side = left_or_right,
            bedId = bedId,
            sleeper = None
        )

@dataclass
class Status:
    """ The status of the bed """
    status: bool
    bedId: str

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a bed object from the SleepIQ servers """
        return Status(
            status = data["status"],
            bedId = data["bedId"],
        )

@dataclass
class FamilyStatus:
    """ Familystatus """
    left_side: Side
    right_side: Side
    # bed: Status

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a FamilyStatus object from the SleepIQ servers """
        return FamilyStatus(
            left_side = data["left_side"],
            right_side = data["right_side"],
            # bed = data["bed"],
        )


@dataclass
class Light:
    """ Defines a light """
    bedId: str
    outlet: int
    setting: int
    timer: str


    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a light object from the SleepIQ servers """
        return Light(
            bedId = data["bedId"],
            outlet = data["outlet"],
            setting = data["setting"],
            timer = data["timer"],
        )

# @dataclass
# class Foundation_Features:
#     """ Defines a foundation status """


#     @staticmethod
#     def from_dict(data: Dict[str, Any]):
#         """ Return a foundation object from the SleepIQ servers """
#         return Foundation_Features(

#         )

@dataclass
class Foundation_Status:
    """ Defines a foundation status """
    fsCurrentPositionPresetRight: str
    fsNeedsHoming: bool
    fsRightFootPosition: str
    fsLeftPositionTimerLSB: str
    fsTimerPositionPresetLeft: str
    fsCurrentPositionPresetLeft: str
    fsLeftPositionTimerMSB: str
    fsRightFootActuatorMotorStatus: str
    fsCurrentPositionPreset: str
    fsTimerPositionPresetRight: str
    fsType: str
    fsOutletsOn: bool
    fsLeftHeadPosition: str
    fsIsMoving: bool
    fsRightHeadActuatorMotorStatus: str
    fsStatusSummary: str
    fsTimerPositionPreset: str
    fsLeftFootPosition: str
    fsRightPositionTimerLSB: str
    fsTimedOutletsOn: bool
    fsRightHeadPosition: str
    fsConfigured: bool
    fsRightPositionTimerMSB: str
    fsLeftHeadActuatorMotorStatus: str
    fsLeftFootActuatorMotorStatus: str
    bedId: str

    @staticmethod
    def from_dict(data: Dict[str, Any], bedId: str):
        """ Return a foundation object from the SleepIQ servers """
        return Foundation_Status(
        fsCurrentPositionPresetRight = data["fsCurrentPositionPresetRight"],
        fsNeedsHoming = data["fsNeedsHoming"],
        fsRightFootPosition = data["fsRightFootPosition"],
        fsLeftPositionTimerLSB = data["fsLeftPositionTimerLSB"],
        fsTimerPositionPresetLeft = data["fsTimerPositionPresetLeft"],
        fsCurrentPositionPresetLeft = data["fsCurrentPositionPresetLeft"],
        fsLeftPositionTimerMSB = data["fsLeftPositionTimerMSB"],
        fsRightFootActuatorMotorStatus = data["fsRightFootActuatorMotorStatus"],
        fsCurrentPositionPreset = data["fsCurrentPositionPreset"],
        fsTimerPositionPresetRight = data["fsTimerPositionPresetRight"],
        fsType = data["fsType"],
        fsOutletsOn = data["fsOutletsOn"],
        fsLeftHeadPosition = data["fsLeftHeadPosition"],
        fsIsMoving = data["fsIsMoving"],
        fsRightHeadActuatorMotorStatus = data["fsRightHeadActuatorMotorStatus"],
        fsStatusSummary = data["fsStatusSummary"],
        fsTimerPositionPreset = data["fsTimerPositionPreset"],
        fsLeftFootPosition = data["fsLeftFootPosition"],
        fsRightPositionTimerLSB = data["fsRightPositionTimerLSB"],
        fsTimedOutletsOn = data["fsTimedOutletsOn"],
        fsRightHeadPosition = data["fsRightHeadPosition"],
        fsConfigured = data["fsConfigured"],
        fsRightPositionTimerMSB = data["fsRightPositionTimerMSB"],
        fsLeftHeadActuatorMotorStatus = data["fsLeftHeadActuatorMotorStatus"],
        fsLeftFootActuatorMotorStatus = data["fsLeftFootActuatorMotorStatus"],
        bedId = bedId,
        )

@dataclass
class Foundation:
    """ Defines a foundation """
    fsBedType: int
    fsBoardFaults: int
    fsBoardFeatures: int
    fsBoardHWRevisionCode: int
    fsBoardStatus: int
    fsLeftUnderbedLightPWM: int
    fsRightUnderbedLightPWM: int
    bedId: str
    foundation_status: Foundation_Status
    features: Dict

    @staticmethod
    def from_dict(data: Dict[str, Any], bedId: str):
        """ Return a foundation object from the SleepIQ servers """
        return Foundation(
            fsBedType = data["fsBedType"],
            fsBoardFaults = data["fsBoardFaults"],
            fsBoardFeatures = data["fsBoardFeatures"],
            fsBoardHWRevisionCode = data["fsBoardHWRevisionCode"],
            fsBoardStatus = data["fsBoardStatus"],
            fsLeftUnderbedLightPWM = data["fsLeftUnderbedLightPWM"],
            fsRightUnderbedLightPWM =  data["fsRightUnderbedLightPWM"],
            bedId = bedId,
            foundation_status = None,
            features = {},
        )

@dataclass
class Bed:
    """ Defines a bed """
    registrationDate: str
    sleeperRightId: int
    base: str
    returnRequestStatus: int
    size: str
    name: str
    serial: str
    isKidsBed: bool
    dualSleep: bool
    bedId: int
    status: int
    sleeperLeftId: int
    version: str
    accountId: int
    timezone: str
    generation: str
    model: str
    purchaseDate: str
    macAddress: str
    sku: str
    zipcode: str
    reference: str
    left_side: Side
    right_side: Side
    lights: List
    foundation: Foundation

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a bed object from the SleepIQ servers """
        return Bed(
            registrationDate = data["registrationDate"],
            sleeperRightId = data["sleeperRightId"],
            base = data["base"],
            returnRequestStatus = data["returnRequestStatus"],
            size = data["size"],
            name = data["name"],
            serial = data["serial"],
            isKidsBed = data["isKidsBed"],
            dualSleep = data["dualSleep"],
            bedId = data["bedId"],
            status = data["status"],
            sleeperLeftId = data["sleeperLeftId"],
            version = data["version"],
            accountId = data["accountId"],
            timezone = data["timezone"],
            generation = data["generation"],
            model = data["model"],
            purchaseDate = data["purchaseDate"],
            macAddress = data["macAddress"],
            sku = data["sku"],
            zipcode = data["zipcode"],
            reference = data["reference"],
            left_side = None,
            right_side = None,
            lights = [],
            foundation = None,
        )
