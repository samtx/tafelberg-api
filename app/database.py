from fastapi import HTTPException

from .schemas import Property


muizenberg = Property(
    name='Muizenberg',
    availability_url="https://www.rockportescape.com/rockport-vacation-rentals/muizenberg-6031rpb",
    booking_url="https://www.rockportescape.com/rescms/item/6/buy",
    product_id="2529-168784",
    eid=6,
    slug='muizenberg'
)

sea_point = Property(
    name="Sea Point",
    availability_url="https://www.rockportescape.com/rockport-vacation-rentals/sea-point",
    booking_url="https://www.rockportescape.com/rescms/item/5/buy",
    slug="sea-point",
    product_id="2529-168777",
    eid="5"
)

simons_town = Property(
    name="Simons Town",
    availability_url="https://www.rockportescape.com/rockport-vacation-rentals/simons-town-6031rpc",
    booking_url="https://www.rockportescape.com/rescms/item/7/buy",
    product_id="2529-168785",
    eid=7,
    slug="simons-town"
)

pier_heaven = Property(
    name="Pier Heaven",
    availability_url="https://www.rockportescape.com/rockport-vacation-rentals/pier-heaven-6031abc",
    booking_url="https://www.rockportescape.com/rescms/item/4/buy",
    product_id="2529-168776",
    eid=4,
    slug="pier-heaven"
)


db = {
    'properties': {
        'muizenberg': muizenberg,
        'sea-point': sea_point,
        'simons-town': simons_town,
        'pier-heaven': pier_heaven,
    }
}

def get_property_or_404(property_slug):
    if property_slug in db['properties']:
        return db["properties"][property_slug]
    raise HTTPException(status_code=404, detail="Property not found")