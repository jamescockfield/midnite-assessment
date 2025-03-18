from pydantic import BaseModel, Field, field_validator
from domain_types import ActivityType

class EventRequest(BaseModel):
    type: str = Field(..., description="Activity type (deposit or withdraw)")
    amount: str = Field(..., description="Amount as string")
    user_id: int = Field(..., description="User ID")
    t: int = Field(..., description="Timestamp in seconds")

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if v not in [ActivityType.DEPOSIT.value, ActivityType.WITHDRAW.value]:
            raise ValueError(f'type must be either {ActivityType.DEPOSIT.value} or {ActivityType.WITHDRAW.value}')
        return v

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        try:
            float(v)
        except ValueError:
            raise ValueError('amount must be a valid number string')
        return v