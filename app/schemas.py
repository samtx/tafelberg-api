from typing import Dict, List, Optional
from decimal import Decimal
import datetime

from pydantic import BaseModel, Field, AnyHttpUrl


class Property(BaseModel):
    name: str
    booking_url: AnyHttpUrl = Field("Booking URL for property")
    availability_url: AnyHttpUrl = Field("Availability URL for property")
    product_id: str
    eid: int
    slug: str = Field("Slug for property")


class PropertyResponse(BaseModel):
    properties: List[Property]

class PropertyAvailabilityData(BaseModel):
    """
    """
    property_slug: str
    available: bool
    price: Optional[Decimal]


class PropertyAvailabilityResponse(BaseModel):
    """
    availability: {
        "2021-01-01" :
            {
                "muizenberg": {
                    "available": True,
                    "price": 250.00
                }, ...
            }, ...
    }
    """
    availability: Dict[datetime.date, Dict[str , PropertyAvailabilityData]]