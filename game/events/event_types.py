from enum import Enum

class EventType(Enum):
    FACTION = "faction"
    REACTIVE = "reactive"
    CHAIN = "chain"
    CRISIS = "crisis"
    OPPORTUNITY = "opportunity"

class EventTrigger(Enum):
    PLAYER_ACTION = "player_action"
    FACTION_STATUS = "faction_status"
    ROUND_START = "round_start"
    ALLIANCE_FORMED = "alliance_formed"
