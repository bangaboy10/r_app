from pydantic import BaseModel, validator
from datetime import datetime

class ReceiptData(BaseModel):
    vendor: str
    date: datetime
    amount: float
    category: str = "Uncategorized"

    @validator('vendor', 'amount', 'date')
    def check_fields(cls, v):
        if not v:
            raise ValueError("Field cannot be empty")
        return v
