from pydantic import BaseModel, Field, HttpUrl


class Property(BaseModel):
    name: str
    booking_url: HttpUrl = Field("Booking URL for property")
    availbility_url: HttpUrl = Field("Availability URL for property")
    product_id: str
    eid: int
    slug: str = Field("Slug for property")


class PropertyAvailability(BaseModel):
    """

    """
    pass



