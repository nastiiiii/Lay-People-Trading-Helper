from enum import Enum

class ExperienceLevelEnum(str, Enum):
    novice = "Novice"
    intermediate = "Intermediate"
    advanced = "Advanced"

class TradeTypeEnum(str, Enum):
    buy = "Buy"
    sell = "Sell"

class BiasTypeEnum(str, Enum):
    overconfidence = "Overconfidence"
    anchoring = "Anchoring"
    loss_aversion = "Loss Aversion"
    regret_aversion = "Regret Aversion"

class DeliveryTypeEnum(str, Enum):
    tooltip = "Tooltip"
    modal = "Modal"
    notification = "Notification"

class UserResponseEnum(str, Enum):
    ignored = "Ignored"
    dismissed = "Dismissed"
    acted = "Acted"
    delayed = "Delayed"