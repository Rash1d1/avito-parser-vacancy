from config import Config
from curl_cffi.requests import AsyncSession
from curl_cffi import requests 


s = AsyncSession()


class API:
    @classmethod
    async def request(cls, url):
        payload = {"api_key": Config.scrapper_api, "url": url}
        r = await s.get("https://api.scraperapi.com", params=payload)
        #r = await s.get(url, proxies=Config.proxies, impersonate="chrome101")
        return r
    @classmethod
    def synchronic_request(cls, url):
        payload = {"api_key": Config.scrapper_api, "url": url}
        r = requests.get("https://api.scraperapi.com", params=payload)
        #r = requests.get(url, proxies=Config.proxies, impersonate="chrome101")
        return r
