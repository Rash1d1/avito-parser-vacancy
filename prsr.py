import asyncio
import datetime
from excel_storage import ExcelStorage
from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json
import vacancy_serializer
import parsed_item
from api import API
from task_runner import TaskRunner


app = None
data_base = None
t = 1


class ParserState:
    number_of_items = 0

    def find_number_of_items(self, url):
        self.number_of_items = find_number_of_vacancies(url)


parser_state = ParserState()


def response_to_json(r):
    scripts = HTMLParser(r.text).css('script')

    data = None

    for script in scripts:
        if "window.__initialData__" in script.text():
            json_text = script.text().split(";")[0].split("=")[-1].strip()
            json_text = unquote(json_text)
            json_text = json_text[1:-1]
            data = json.loads(json_text)

    return data


def find_vacancy_catalog(data):
    if data is not None:
        for key in data:
            if "single-page" in key:
                jobs = data[key]["data"]["catalog"]["items"]
                if (not jobs) or (jobs is None):
                    return "Не найдено вакансий"
                else:
                    return jobs


def vacancy(job):
    global t
    global data_base
    s = vacancy_serializer.VacancySerializer(job)
    parsed_job = parsed_item.ParsedItem(
        id=job["id"],
        title=job["title"],
        url="https://www.avito.ru" + job["urlPath"],
        min_salary=s.salary()[0],
        max_salary=s.salary()[1],
        currency=s.currency(),
        salary_schedule=s.salary_schedule(),
        schedule=s.schedule(),
        experience=s.experience(),
        description=job["description"],
        employer=s.employer(),
        link_to_employer=s.employer_link(),
        location=s.location(),
        date_of_publication=str(
            datetime.datetime.fromtimestamp(int(job["sortTimeStamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    )
    t += 1
    print(t, parsed_job)
    data_base.add_cell(parsed_job)
    return parsed_job


def find_number_of_vacancies(url):
    r = API.synchronic_request(url)
    data = response_to_json(r)
    if data is not None:
        for key in data:
            if "single-page" in key:
                number_of_vacancies = data[key]["data"]["mainCount"]
                return number_of_vacancies


async def result(r):
    global t
    global app
    data = response_to_json(r)
    jobs = find_vacancy_catalog(data)
    parsed_jobs = []
    if isinstance(jobs, list):
        for job in jobs:
            if job.get("id"):
                parsed_job = vacancy(job)
                parsed_jobs.append(parsed_job)
    await data_base.save_to_excel()
    app.move_progress(t)
    app.app.update()

    return parsed_jobs


async def parse_page(url):
    max_retries = 2
    retry_delay = 2
    for retry in range(max_retries):
        try:
            r = await API.request(url)
            parsed_jobs = await result(r)
            data = parsed_jobs
            if (not data) or (data is None):
                await asyncio.sleep(retry_delay)
            else:
                return
        except Exception as e:
            raise e


async def parse(cfg, app_):
    global app
    global data_base
    global t
    global parser_state
    app = app_
    parser_state.find_number_of_items(cfg.url_to_parse)
    data_base = ExcelStorage(cfg.location_of_result_file)
    num = parser_state.number_of_items
    await parse_page(cfg.url_to_parse)
    tasks = []
    url = cfg.url_to_parse + "&p=1"
    for i in range(2, min(cfg.limit + 1, 2 + num // 50)):
        url = url.replace(f"&p={i - 1}", f"&p={i}")
        tasks.append(url)
    await TaskRunner().run_tasks(parse_page, tasks)
    print(t)
