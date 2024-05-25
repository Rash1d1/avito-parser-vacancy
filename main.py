import datetime
import time
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from curl_cffi.requests import AsyncSession
import unicodedata
# from curl_cffi import requests

from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json


asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
LINK = "https://www.avito.ru"
s = AsyncSession()

def processSalary(salaryString):
    minMaxArr = [None, None]
    if "до" in salaryString:
        digits_only = ''.join(filter(str.isdigit, salaryString))
        minMaxArr[1] = digits_only
    elif "от" in salaryString:
        digits_only = ''.join(filter(str.isdigit, salaryString))
        minMaxArr[0] = digits_only
    elif "—" in salaryString:
        fromToDigits = salaryString.split("—")
        minMaxArr[0] = "".join(filter(str.isdigit, fromToDigits[0]))
        minMaxArr[1] = "".join(filter(str.isdigit, fromToDigits[1]))
    return minMaxArr
async def proccessCurrency(job):
    currency_symbols = ['$', '€', '£', '¥', '₹', '₽', '฿', '₿', '₴', '₩', '₺', '₸', '₮', '₦', '₱', '₲', '₳', '₵', '₡',
                        '₢', '₣', '₤', '₥', '₰', '₶', '₷', '₸', '₹', '₺', '₻', '₼', '₽', '₾', '₿']

    if isinstance(job["priceDetailed"]["fullString"], str):
        for char in job["priceDetailed"]["fullString"]:
            if unicodedata.category(char) == 'Sc' or char in currency_symbols:
                return char

    return None
async def proccessSalarySchedule(job):
    if "за смену" in job["priceDetailed"]["fullString"]:
        return "За смену"
    else:
        if isinstance(job["iva"]["ParamsStep"][0]["payload"]["text"], str):
            salaryScheduleString = job["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
            for string in salaryScheduleString:
                if "Выплаты" in string:
                    return string.replace("Выплаты", "").strip()
            return None
async def proccessSchedule(job):
    try:
        return job["iva"]["ParamsStep"][0]["payload"]["text"].split("·")[0]
    except:
        return None
async def proccessExperience(job):
    if isinstance(job["iva"]["ParamsStep"][0]["payload"]["text"], str):
        scheduleString = job["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
        for string in scheduleString:
            if "Опыт" in string:
                return string.replace("Опыт", "").strip()
        return None
async def proccessEmpoler(job):
    try:
        return job["iva"]["UserInfoStep"][0]["payload"]["profile"]["title"]
    except:
        return None
async def proccessEmpolerLink(job):
    try:
        return LINK + str(job["iva"]["UserInfoStep"][0]["payload"]["profile"]["link"])
    except:
        return None
async def proccessLocation(job):
    try:
        s1 = job["coords"]["address_user"]
        s2 = job["iva"]["GeoStep"][0]["payload"]["geoForItems"]["formattedAddress"]
        return max(s1, s2, key=len)
    except:
        return None
async def processJobTokens(job):
    tokens = {}
    tokens["Id"] = str(job["id"])
    tokens["Title"] = str(job["title"])
    tokens["Link"] = LINK + str(job["urlPath"])
    tokens["MinSalary"] = str(processSalary(job["priceDetailed"]["fullString"])[0])
    tokens["MaxSalary"] = str(processSalary(job["priceDetailed"]["fullString"])[1])
    tokens["Currency"] = str(await proccessCurrency(job))
    tokens["SalarySchedule"] = str(await proccessSalarySchedule(job))
    tokens["Schedule"] = str(await proccessSchedule(job))
    tokens["Experience"] = str(await proccessExperience(job))
    tokens["Description"] = str(job["description"])
    tokens["Employer"] = str(await proccessEmpoler(job))
    tokens["LinkToEmployer"] = str(await proccessEmpolerLink(job))
    tokens["Location"] = str(await proccessLocation(job))
    tokens["TimeOfPublication"] = str(datetime.datetime.fromtimestamp(int(job["sortTimeStamp"])/1000).strftime('%Y-%m-%d %H:%M:%S'))

    print(tokens)







async def parse(url):
    proxies = {
        'https': 'http://44C5XG0SL0:uK80EV4Sq9@65.108.12.231:10574',
        'http': 'http://44C5XG0SL0:uK80EV4Sq9@65.108.12.231:10574'
    }
    payload = {"api_key": "4f27ac93dc6fdd05736794124b7c468c", "url": url}
    # r = requests.get('https://api.scraperapi.com', params=payload)

    r = await s.get('https://api.scraperapi.com', params=payload)
    html = r.text
    tree = HTMLParser(html)
    scripts = tree.css('script')

    data = None
    for script in scripts:
        if "window.__initialData__" in script.text():
            jsonText = script.text().split(";")[0].split("=")[-1].strip()
            jsonText = unquote(jsonText)
            jsonText = jsonText[1:-1]
            data = json.loads(jsonText)
    if data != None:
        for key in data:
            if "single-page" in key:
                jobs = data[key]["data"]["catalog"]["items"]
                for job in jobs:
                    if job.get("id"):
                        await processJobTokens(job)
                print("______________________________________________")


async def startParsing(url):
    proxies = {
        'https': 'http://44C5XG0SL0:uK80EV4Sq9@65.108.12.231:10574',
        'http': 'http://44C5XG0SL0:uK80EV4Sq9@65.108.12.231:10574'
    }
    payload = {"api_key": "4f27ac93dc6fdd05736794124b7c468c", "url": url}
    r = await s.get('https://api.scraperapi.com', params=payload)

    html = r.text
    tree = HTMLParser(html)
    scripts = tree.css('script')

    data = None

    for script in scripts:
        if "window.__initialData__" in script.text():
            jsonText = script.text().split(";")[0].split("=")[-1].strip()
            jsonText = unquote(jsonText)
            jsonText = jsonText[1:-1]
            data = json.loads(jsonText)
    if data != None:
        for key in data:
            if "single-page" in key:
                numberOfJobs = data[key]["data"]["totalCount"]
                jobs = data[key]["data"]["catalog"]["items"]
                if jobs == []:
                    return "Не найдено вакансий"
                else:
                    for job in jobs:
                        if job.get("id"):
                            await processJobTokens(job)


    tasks = []
    url += "&p=1"
    for i in range(2, min(13, numberOfJobs / 50)):
        url = url.replace(f"&p={i - 1}", f"&p={i}")
        tasks.append(asyncio.create_task(parse(url)))
    await asyncio.gather(*tasks)



async def main():
    url = "https://www.avito.ru/tatarstan/vakansii?cd=1&q=%D0%BF%D0%BE%D0%B4%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0"
    await startParsing(url)



if __name__ == '__main__':
    asyncio.run(main())