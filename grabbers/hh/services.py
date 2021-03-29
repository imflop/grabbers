import asyncio
import logging
import typing as t
from dataclasses import dataclass, field

import aiohttp


@dataclass(frozen=True)
class HHService:
    base_url: str = field(default="https://api.hh.ru/vacancies", init=False)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(f"{__name__}"))

    async def search(self, search_str: str) -> t.Iterable[t.Any]:
        self.logger.info("Preparing list of links")
        urls = await self._get_vacancies_links(search_str)
        self.logger.info(f"Handling {len(urls)} links")
        data = await self._collect_data(urls)
        self.logger.info("Data collected")
        return data

    async def _get_data(self, session: aiohttp.ClientSession, link: str, **kwargs) -> dict[t.Hashable, t.Any]:
        resp = await session.request("GET", url=link, params=kwargs)
        data = await resp.json()
        return data

    async def _collect_data(self, links: list) -> t.Iterable[t.Any]:
        async with aiohttp.ClientSession() as s:
            tasks = [self._get_data(session=s, link=link) for link in links]
            return await asyncio.gather(*tasks, return_exceptions=True)

    async def _get_vacancies_links(self, text: str) -> list[str]:
        """
        Create a vacancies url list
        """
        tasks, links, items = [], [], []
        params = dict(text=text)

        async with aiohttp.ClientSession() as s:
            raw_response = await self._get_data(session=s, link=self.base_url, **params)
            found = raw_response["found"]

            if found <= 100:
                params["per_page"] = found
                tasks = [self._get_data(session=s, link=self.base_url, **params)]
            else:
                # lookup 2 pages by 100 adverts
                for i in range(2):
                    params["per_page"] = str(100)
                    params["page"] = str(i)
                    tasks += [self._get_data(session=s, link=self.base_url, **params)]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            items = [item for result in results for item in result["items"]]
            links += [f"{self.base_url}/{_['id']}" for _ in items]

        return links
