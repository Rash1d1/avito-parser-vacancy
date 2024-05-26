import api
from parser import result, find_number_of_vacancies
import task_runner


async def parse(url):
    r = await api.API.request(url)
    parsed_jobs = result(r)
    print("_________________________________________________________________")


async def execute(starting_page_url):
    await parse(starting_page_url)
    number_of_jobs = find_number_of_vacancies(await api.API.request(starting_page_url))
    tasks = []
    url = starting_page_url + "&p=1"
    for i in range(2, min(80, number_of_jobs // 50)):
        url = url.replace(f"&p={i - 1}", f"&p={i}")
        tasks.append(url)
    await task_runner.TaskRunner().run_tasks(parse, tasks)
