from fastapi import APIRouter


property_router = APIRouter()


@property_router.get("/")
async def get_properties():
    pass


@property_router.get("/{name}")
async def get_one_property(name: str):
    pass