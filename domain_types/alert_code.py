from enum import Enum

class AlertCode(Enum):
    LARGE_WITHDRAWAL = 1100
    CONSECUTIVE_WITHDRAWALS = 30
    INCREASING_DEPOSITS = 300
    ACCUMULATIVE_DEPOSIT = 123 