from enum import Enum


class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_vacation = "on_vacation"
    sick_leave = "sick_leave"
