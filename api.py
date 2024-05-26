from config import scrapper_api, proxies
from curl_cffi.requests import AsyncSession

s = AsyncSession

class API:
    async def request(self, url):
        # proxies_used = proxies - in case proxies will be used instead of scrapperAPI
        payload = {"api_key": scrapper_api, "url": url}
        r = await s.get('https://api.scraperapi.com', params=payload)
        return r