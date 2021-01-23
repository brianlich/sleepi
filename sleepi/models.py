""" Models for Sleepi """
from typing import Any, Dict, List
from attr import dataclass


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
    favorite: int

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
            side = data["side"],
            favorite = None
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
    sleeper: Sleeper

    @staticmethod
    def from_dict(data: Dict[str, Any], left_or_right: str):
        """ Return a bed object from the SleepIQ servers """
        return Side(
            isInBed = data["isInBed"],
            alertDetailedMessage = data["alertDetailedMessage"],
            sleepNumber = data["sleepNumber"],
            alertId = data["alertId"],
            lastLink = data["lastLink"],
            pressure = data["pressure"],
            side = left_or_right,
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
class SleepNumberFavorite:
    """ Familystatus """
    bedId: str
    sleepNumberFavoriteRight: int
    sleepNumberFavoriteLeft: int

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a SleepNumberFavorite object from the SleepIQ servers """
        return SleepNumberFavorite(
            bedId = data["bedId"],
            SleepNumberFavoriteRight = data["SleepNumberFavoriteRight"],
            SleepNumberFavoriteLeft = data["SleepNumberFavoriteLeft"],
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
        )


@dataclass
class Light:
    """ Defines a light """
    bedId: str
    outlet: int
    setting: int
    timer: str
    name: str


    @staticmethod
    def from_dict(data: Dict[str, Any], name):
        """ Return a light object from the SleepIQ servers """
        if data is not None:
            return Light(
                bedId = data["bedId"],
                outlet = data["outlet"],
                setting = data["setting"],
                timer = data["timer"],
                name = name,
            )

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

    @staticmethod
    def from_dict(data: Dict[str, Any]):
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
    foundation_status: Foundation_Status
    features: Dict

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a foundation object from the SleepIQ servers """
        return Foundation(
            fsBedType = data["fsBedType"],
            fsBoardFaults = data["fsBoardFaults"],
            fsBoardFeatures = data["fsBoardFeatures"],
            fsBoardHWRevisionCode = data["fsBoardHWRevisionCode"],
            fsBoardStatus = data["fsBoardStatus"],
            fsLeftUnderbedLightPWM = data["fsLeftUnderbedLightPWM"],
            fsRightUnderbedLightPWM =  data["fsRightUnderbedLightPWM"],
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
    light1: Dict 
    light2: Dict
    light3: Dict
    light4: Dict
    foundation: Foundation

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a bed object from the SleepIQ servers """
        return Bed(
            registrationDate = data["beds"][0]["registrationDate"],
            sleeperRightId = data["beds"][0]["sleeperRightId"],
            base = data["beds"][0]["base"],
            returnRequestStatus = data["beds"][0]["returnRequestStatus"],
            size = data["beds"][0]["size"],
            name = data["beds"][0]["name"],
            serial = data["beds"][0]["serial"],
            isKidsBed = data["beds"][0]["isKidsBed"],
            dualSleep = data["beds"][0]["dualSleep"],
            bedId = data["beds"][0]["bedId"],
            status = data["beds"][0]["status"],
            sleeperLeftId = data["beds"][0]["sleeperLeftId"],
            version = data["beds"][0]["version"],
            accountId = data["beds"][0]["accountId"],
            timezone = data["beds"][0]["timezone"],
            generation = data["beds"][0]["generation"],
            model = data["beds"][0]["model"],
            purchaseDate = data["beds"][0]["purchaseDate"],
            macAddress = data["beds"][0]["macAddress"],
            sku = data["beds"][0]["sku"],
            zipcode = data["beds"][0]["zipcode"],
            reference = data["beds"][0]["reference"],
            left_side = None,
            right_side = None,
            light1 = {},
            light2 = {},
            light3 = {},
            light4 = {},
            foundation = None,
        )
