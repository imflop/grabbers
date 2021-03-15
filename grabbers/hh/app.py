import asyncio
import json
import logging
import typing as t
from datetime import datetime

import aiohttp
from aiomisc.log import (
    LogFormat,
    LogLevel,
    basic_config,
)


basic_config(LogLevel.info, LogFormat.color, buffered=True)
log = logging.getLogger(__name__)


async def get_data(session: aiohttp.ClientSession, link: str, **kwargs) -> dict[t.Hashable, t.Any]:
    resp = await session.request("GET", url=link, params=kwargs)
    data = await resp.json()
    return data


async def get_vacancies_links(text: str) -> list[str]:
    """
    Create a vacancies url list
    """
    tasks, links, items = [], [], []
    _base_url = "https://api.hh.ru/vacancies"
    params = dict(text=text)
    async with aiohttp.ClientSession() as s:
        raw_response = await get_data(session=s, link=_base_url, **params)
        found = raw_response["found"]
        if found <= 100:
            params["per_page"] = found
            tasks = [get_data(session=s, link=_base_url, **params)]
        else:
            # lookup 2 pages by 100 adverts
            for i in range(2):
                params["per_page"] = str(100)
                params["page"] = str(i)
                tasks += [get_data(session=s, link=_base_url, **params)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        items = [item for result in results for item in result["items"]]
        links += [f"{_base_url}/{_['id']}" for _ in items]
    return links


async def collect_data(links: list) -> t.Iterable[t.Any]:
    async with aiohttp.ClientSession() as s:
        tasks = [get_data(session=s, link=link) for link in links]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def save(data: t.Iterable) -> str:
    """
    Dummy save data
    """
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"/tmp/hh_{today}.json"
    with open(file_name, "w") as f:
        json.dump(data, f, ensure_ascii=False)
        return file_name


async def run(search_str: str) -> None:
    log.info("Starts receiving data from api.hh.ru")
    urls = await get_vacancies_links(search_str)
    data = await collect_data(urls)
    log.info("Finished receiving data from api.hh.ru")
    result = await save(data)
    log.info("Data saved at %s", result)


async def run_at() -> None:
    import time

    time.monotonic
