import asyncio
import datetime
import urllib
from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json
import vacancy_serializer
import parsed_item
from api import API
from task_runner import TaskRunner



class ParserState:
    number = 0

    def __init__(self, url):
        data = None
        retry = 0
        while data is None:
            if retry == 10:
                print("Неудача при попытке обратиться к серверу")
                return
            r = API.synchronic_request(url)
            scripts = HTMLParser(r.text).css('script')
            for script in scripts:
                if "window.__initialData__" in script.text():
                    json_text = script.text().split(";")[0].split("=")[-1].strip()
                    json_text = unquote(json_text)
                    json_text = json_text[1:-1]
                    data = json.loads(json_text)
                    if data is not None:
                        for key in data:
                            if "single-page" in key:
                                number_of_items = data[key]["data"]["mainCount"]
                                self.number = number_of_items
                                return
            retry += 1


class Parser:
    number_of_items = 0
    number_of_parsed_items = 1

    def __init__(self, cfg_, data_storage_, state_, progress_callback=None):
        self.cfg = cfg_
        self.data_storage = data_storage_
        self.number_of_items = state_.number
        self.progress_callback = progress_callback
    def response_to_json(self, r):
        scripts = HTMLParser(r.text).css('script')
        for script in scripts:
            if "window.__initialData__" in script.text():
                json_text = script.text().split(";")[0].split("=")[-1].strip()
                json_text = unquote(json_text)
                json_text = json_text[1:-1]
                data = json.loads(json_text)
                return data

    def find_catalog(self, data):
        if data is not None:
            for key in data:
                if "single-page" in key:
                    jobs = data[key]["data"]["catalog"]["items"]
                    if (not jobs) or (jobs is None):
                        return "Не найдено вакансий"
                    else:
                        return jobs

    def process(self, item):
        s = vacancy_serializer.VacancySerializer(item)
        parsed_job = parsed_item.ParsedItem(
            id=item["id"],
            title=item["title"],
            url="https://www.avito.ru" + item["urlPath"],
            min_salary=s.salary()[0],
            max_salary=s.salary()[1],
            currency=s.currency(),
            salary_schedule=s.salary_schedule(),
            schedule=s.schedule(),
            experience=s.experience(),
            description=item["description"],
            employer=s.employer(),
            link_to_employer=s.employer_link(),
            location=s.location(),
            date_of_publication=str(
                datetime.datetime.fromtimestamp(int(item["sortTimeStamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
        )
        if not ((parsed_job.min_salary == 0) and (parsed_job.max_salary == 0)):
            print(self.number_of_parsed_items)
            self.number_of_parsed_items += 1
            self.data_storage.add_cell(parsed_job)
            if self.progress_callback is not None:
                self.progress_callback(self.number_of_parsed_items)
            return parsed_job

    def result(self, r):
        data = self.response_to_json(r)
        # with open("data.json", "w", encoding='utf=8') as file:
        #     json.dump(data, file, ensure_ascii=False, indent=4)
        items = self.find_catalog(data)
        parsed_jobs = []
        if isinstance(items, list):
            for item in items:
                if item.get("id"):
                    parsed_item = self.process(item)
                    parsed_jobs.append(parsed_item)
        self.data_storage.save_to_excel()
        # app.move_progress(t)
        return parsed_jobs

    async def parse_page(self, url):
        max_retries = 6
        retry_delay = 30
        for retry in range(max_retries):
            r = None
            try:
                r = await API.request(url)
                parsed_items = self.result(r)
                data = parsed_items
                if (not data) or (data is None):
                    await asyncio.sleep(retry_delay)
                else:
                    return
            except Exception as e:
                print(e)
                print(f"Try {retry + 1} was unsuccessful, one more time...")
                await asyncio.sleep(retry_delay)

    async def parse(self):
        num = self.number_of_items
        await self.parse_page(self.cfg.url_to_parse)
        tasks = []
        base_url = self.cfg.url_to_parse
        for i in range(2, min(self.cfg.limit + 1, 2 + num // 50)):
            if bool(urllib.parse.urlparse(base_url).query):
                param_prefix = "&"
            else:
                param_prefix = "?"

            url = f"{base_url}{param_prefix}p={i}"

            tasks.append(url)
        await TaskRunner().run_tasks(self.parse_page, tasks)
        print(self.number_of_parsed_items)
