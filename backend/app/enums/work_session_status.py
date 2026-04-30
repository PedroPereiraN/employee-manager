from enum import Enum


class WorkSessionStatus(str, Enum):
    started = "started"
    paused = "paused"
    resumed = "resumed"
    completed = "completed"
    stopped = "stopped"
