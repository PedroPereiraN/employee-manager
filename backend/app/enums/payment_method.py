from enum import Enum


class PaymentMethod(str, Enum):
    monthly = "monthly"
    weekly = "weekly"
    daily = "daily"
