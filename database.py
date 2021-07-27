from schemas import Property


muizenberg = Property(
    name='Muizenberg',
    availibilty_url="https://www.rockportescape.com/rockport-vacation-rentals/muizenberg-6031rpb",
    booking_url="https://www.rockportescape.com/rescms/item/6/buy",
    product_id="2529-168784",
    eid=6
    slug='muizenberg'
)

sea_point = Property(
    name="Sea Point",
    availibility_url="https://www.rockportescape.com/rockport-vacation-rentals/sea-point",
    booking_url="",
    slug="sea-point"
)

simons_town = Property(
    name="Simons Town",
    availibility_url="https://www.rockportescape.com/rockport-vacation-rentals/simons-town-6031rpc",
    booking_url="",
    product_id="2529-168785",
    eid=7,
    slug="simons-town"
)

pier_heaven = Property(
    name="Pier Heaven",
    availibility_url="https://www.rockportescape.com/rockport-vacation-rentals/pier-heaven-6031abc",
    booking_url="",
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