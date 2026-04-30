from enum import Enum


class ServiceOrderStatus(str, Enum):
    in_progress = "in_progress"
    pending = "pending"
    suspended = "suspended"
    completed = "completed"
    cancelled = "cancelled"
