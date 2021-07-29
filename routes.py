import datetime

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from scraper import get_property_availability, generate_booking_url
from database import db, get_property_or_404
from cache import cache
from schemas import PropertyResponse, PropertyAvailabilityResponse


router = APIRouter()


@router.get("/", include_in_schema=False)
def home():
    with open("index.html", "r") as f:
        html = f.read()
    return HTMLResponse(html)


@router.get("/properties", response_model=PropertyResponse)
def get_all_property_information():
    """
    Return property information in database
    """
    properties = list(db['properties'].values())
    res = PropertyResponse(properties=properties)
    return res


@router.get("/availability", response_model=PropertyAvailabilityResponse)
async def get_availability():
    # check cache
    key = "avail:all"
    if res := cache.get(key):
        print('cache HIT')
        # Set a return header X-Cache-Hit
        return res
    availability = await get_property_availability()
    res = PropertyAvailabilityResponse(availability=availability)
    # cache value for 15 seconds
    cache.set(key, res, ttl=15)
    return res


def today_factory():
    return datetime.date.today()


@router.get("/book/{property_slug}")
def book_property(
    property_slug: str,
    date_begin: datetime.date,
    date_end: datetime.date,
    num_adults: int,
    num_children: int,
):
    property_ = get_property_or_404(property_slug)
    params = {
        'date_begin': date_begin,
        'date_end': date_end,
        'num_adults': num_adults,
        'num_children': num_children
    }
    res = generate_booking_url(property_, params)
    return res


# @router.get('/reviews')
# async def get_all_reviews():
#     """
#     Get reviews for all properties
#     """
#     pass


# @router.get('/reviews/{property_slug}')
# async def get_one_reviews(property_slug: str):
#     """
#     Get reviews for one property
#     """
#     pass