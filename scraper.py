import asyncio
from collections import namedtuple
from schemas import PropertyAvailabilityData
from typing import List, Union
from decimal import Decimal
import urllib.parse

import httpx
from bs4 import BeautifulSoup
from starlette.concurrency import run_in_threadpool

from database import db


HtmlProperty = namedtuple('HtmlProperty', ['html', 'property'])

async def get_property_availability(property_slugs: Union[str, List[str]] = None):
    """
    Scrape the Rockport Escapes website to get current availability
    property_slugs: list of properties to get availability data from
        None = all properties
    """
    if property_slugs is None or not property_slugs:
        property_slugs = tuple(db['properties'].keys())
    if isinstance(property_slugs, str):
        property_slugs = (property_slugs,)
    properties = tuple(db['properties'].values())
    tasks = [
        fetch_property_html(p.availability_url) for p in properties
        if p.slug in property_slugs
    ]
    html_results = await asyncio.gather(*tasks)
    html_property_list = [
        HtmlProperty(html, property_) for html, property_ in zip(html_results, properties)
    ]
    data = await run_in_threadpool(collect_data_from_html, html_property_list)
    return data


async def fetch_property_html(property_availability_url: str):
    headers = {
        "User-Agent": "Tafelberg API/Rockport Escapes Scraper (Sam Friedman, samtx@outlook.com)"
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(property_availability_url, headers=headers)
    html = res.text
    return html


def collect_data_from_html(html_property_list: List[HtmlProperty]):
    data = {}
    for item in html_property_list:
        data = parse_html(item.html, item.property, data)
    return data


def parse_html(html, property_, data):
    soup = BeautifulSoup(html, 'lxml')
    months = soup.find_all('table', class_='rc-calendar')
    for month in months:
        caption = month.find('caption').get_text().replace(u'\xa0', u' ')
        month_str, year_str = caption.split()
        month_int = month_to_int(month_str)
        year = str(year_str)
        days = month.find_all('td', class_='day')
        for day in days:
            day_of_month = int(day.find('span', class_='mday').get_text())
            price = day.find(class_='rc-price')
            price = price_string_to_decimal(price.get_text(strip=True)) if price else None
            avail_classes = day['class']
            available = is_available(avail_classes)
            date_str = f'{year}-{month_int:02d}-{day_of_month:02d}'
            availability = PropertyAvailabilityData(
                property_slug=property_.slug,
                price=price,
                available=available
            )
            if date_str in data:
                data[date_str][property_.slug] = availability
            else:
                data[date_str] = {property_.slug: availability}
    return data


def price_string_to_decimal(price_string):
    """
    price_string = "  $350  " --> Decimal('350.00')
    """
    price = price_string.strip('$').replace(',','')
    price = float(price)
    out_str = f"{price:.2f}"
    dec = Decimal(out_str)
    return dec


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


def generate_booking_url(property_, input_params):
    """
    Generate booking url based on query parameters
    """
    query_params = {
        'rcav[begin]': input_params['date_begin'],
        'rcav[end]': input_params['date_end'],
        'rcav[adult]': input_params['num_adults'],
        'rcav[child]': input_params['num_children'],
        'rcav[eid]': property_.eid,
        f'rcav[IDs][{property_.eid}]': property_.product_id,
        'eid': property_.eid
    }
    base_url = property_.booking_url
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    url = f"{base_url}?{query_string}"
    return url

