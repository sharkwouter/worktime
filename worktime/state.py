import enum


class State(enum.Enum):
    READY = enum.auto()
    RUNNING = enum.auto()
    DONE = enum.auto()


class Track(enum.Enum):
    BREAK = enum.auto()
    WORK = enum.auto()
    PROCRASTINATE = enum.auto()
