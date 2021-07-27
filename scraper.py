import asyncio

import httpx
from bs4 import BeautifulSoup


async def get_property_availability(db, property_slugs=None):
    """
    Scrape the Rockport Escapes website to get current availability
    db: dictionary database of properties
    property_slugs: list of properties to get availability data from
        None = all properties
    """
    if property_slugs is None or not property_slugs:
        property_slugs = db.properties.keys()
    properties = tuple(db.properties.values())
    tasks = [
        fetch_property_html(p.availibility_url) for p in properties
        if p in property_slugs
    ]
    html_results = await asyncio.gather(*tasks)
    data = {}
    for html, property_ in zip(html_results, properties):
        data = parse_html(html, property_, data)
    return data


async def get_one_property_availability(db):
    pass


async def fetch_property_html(property_availability_url: str):
    headers = {
        "User-Agent": "Tafelberg API/Rockport Escapes Scraper (Sam Friedman, samtx@outlook.com)"
    }
    async with httpx.AsyncClient as client:
        res = await client.get(property_availability_url, headers=headers)
    html = res.text
    return html


def parse_html(html, property_, data=None):
    soup = BeautifulSoup(html, 'lxml')
    months = soup.find_all('table', class_='rc-calendar')
    if data is None:
        data = {}
    for month in months:
        caption = month.find('caption').get_text().replace(u'\xa0', u' ')
        month_str, year_str = caption.split()
        month_int = month_to_int(month_str)
        year = str(year_str)
        days = month.find_all('td', class_='day')
        for day in days:
            day_of_month = int(day.find('span', class_='mday').get_text())
            price = day.find(class_='rc-price')
            price = price.get_text(strip=True) if price else None
            avail_classes = day['class']
            available = is_available(avail_classes)
            date_str = f'{year}-{month_int:02d}-{day_of_month:02d}'
            data_item = {
                'property': property_,
                'price': price,
                'available': available
            }
            if date_str in data:
                data[date_str].append(data_item)
            else:
                data[date_str] = [data_item]
    return data


def month_to_int(month_str):
    months = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }
    month_int = months[month_str]
    return month_int


def is_available(class_list):
    if 'av-O' in class_list:
        return 1
    elif 'av-X' in class_list:
        return 0
    else:
        raise Exception('is_available error')