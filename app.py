from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scraper import get_property_availability
from database import db
from cache import cache


app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins="*",
)


@app.get("/properties")
async def get_properties():
    # check cache
    key = "avail:all"
    if key in cache:
        res = cache.get(key)
        return res
    res = await get_property_availability(db)
    # cache value for 15 seconds
    cache.set(key, ttl=15)
    # Set a return header X-Cache-Hit
    return res


@app.get("/properties/{property_slug}")
async def get_one_property(property_slug: str):
    # check cache
    key = f"avail:{property_slug}"
    if key in cache:
        res = cache.get(key)
        return res
    res = await get_property_availability(db, property_slug)
    cache.set(res, ttl=15)
    return res


@app.get("/properties/{property_slug}/book")
async def get_property_booking_url(
    property_slug: str,
    date_begin: str,
    date_end: str,
    num_adults: int,
    num_children: int,
):
    res = get_booking_url(db, property_slug)
    cache.set(res, ttl=15)
    return res


@app.get('/reviews')
async def get_property_reviews():
    """
    Get reviews for all properties
    """
    pass


@app.get('/reviews/{property_slug}')
async def get_property_reviews(property_slug: str):
    """
    Get reviews for one property
    """

    pass


