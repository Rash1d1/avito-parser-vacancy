import datetime
import time

from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json
import vacancy_serializer
import parsed_item
from api import API
from task_runner import TaskRunner
from config import LIMIT, url_to_parse

t = 1

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
    s = vacancy_serializer.VacancySerializer(job)
    parsed_job = parsed_item.ParsedItem(
        id=job["id"],
        title=job["title"],
        url=job["urlPath"],
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
    print(t)

    return parsed_job


def find_number_of_vacancies(r):
    data = response_to_json(r)
    if data is not None:
        for key in data:
            if "single-page" in key:
                number_of_vacancies = data[key]["data"]["totalCount"]
                return number_of_vacancies


def result(r):
    data = response_to_json(r)
    jobs = find_vacancy_catalog(data)
    parsed_jobs = []
    if isinstance(jobs, list):
        for job in jobs:
            if job.get("id"):
                parsed_job = vacancy(job)
                parsed_jobs.append(parsed_job)
    return parsed_jobs


async def parse_page(url):
    data = None
    while not data:
        r = await API.request(url)
        parsed_jobs = result(r)
        data = parsed_jobs
        # print(r.text)
        if (not data) or (data is None):
            time.sleep(3)
    print(url)
    print("_________________________________________________________________")


async def parse():
    await parse_page(url_to_parse)
    number_of_elements = find_number_of_vacancies(await API.request(url_to_parse))
    tasks = []
    url = url_to_parse + "&p=1"
    for i in range(2, min(LIMIT, 2 + number_of_elements // 50)):
        url = url.replace(f"&p={i - 1}", f"&p={i}")
        tasks.append(url)
    await TaskRunner().run_tasks(parse_page, tasks)
