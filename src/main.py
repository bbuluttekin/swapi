"""
To enable asynchronous call between each network calls this work assumes
that all the URLs to pagination calls are known.
"""
import asyncio
import datetime
import json
import logging
from typing import List, Optional

import aiohttp
from aiohttp import ClientSession
from pydantic import BaseModel


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger()


class Planet(BaseModel):
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: Optional[List[str]]
    films: List[str]
    created: datetime.datetime
    edited: datetime.datetime
    url: str


async def get_api_result(url: str, session: ClientSession, response_collection: dict, **kwargs) -> None:
    """Utility function to retrieve api response.

    Args:
        url (str): API main or page url
        session (ClientSession): aiohttp session object
        response_collection (dict): Final collection dictionary to gather all the data
    """
    response = await session.request(method="GET", url=url, **kwargs)
    response.raise_for_status()
    logger.info(f"Got {response.status} response for URL: {url}")
    result = json.loads(await response.text())
    planets: List[Planet] = [Planet(**record)
                             for record in result["results"]]
    for planet in planets:
        response_collection[planet.name] = planet.residents.__len__()


async def main(urls: List) -> None:
    """Main entry point to script

    Args:
        urls (List): List of API urls to retrive
    """
    planets = {}
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            logger.info(url)
            tasks.append(get_api_result(
                url, session, response_collection=planets))
        await asyncio.gather(*tasks)
        logger.info(
            f"Number of people in all planets: {sum(planets.values())}")
        logger.info(f"Number of planets: {len(planets)}")
        logger.info(planets)


if __name__ == "__main__":
    urls = [
        "https://swapi.dev/api/planets",
        "https://swapi.dev/api/planets/?page=2",
        "https://swapi.dev/api/planets/?page=3",
        "https://swapi.dev/api/planets/?page=4",
        "https://swapi.dev/api/planets/?page=5",
        "https://swapi.dev/api/planets/?page=6"
    ]
    asyncio.run(main(urls))
