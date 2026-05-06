from enum import Enum


class ServiceOrderStatus(str, Enum):
    in_progress = "in_progress"
    pending = "pending"
    not_started = "not_started"
    suspended = "suspended"
    completed = "completed"
    cancelled = "cancelled"
