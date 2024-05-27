from config import Config
from curl_cffi.requests import AsyncSession

s = AsyncSession()


class API:
    @classmethod
    async def request(cls, url):
        # proxies_used = proxies - in case proxies will be used instead of scrapperAPI
        payload = {"api_key": Config.scrapper_api, "url": url}
        r = await s.get('https://api.scraperapi.com', params=payload)
        return r
