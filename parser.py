import datetime
from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json
import vacancy_serializer
import parsed_item


class Parser:
    def __init__(self, response):
        self.r = response

    def response_to_json(self):
        scripts = HTMLParser(self.r.text).css('script')

        data = None

        for script in scripts:
            if "window.__initialData__" in script.text():
                json_text = script.text().split(";")[0].split("=")[-1].strip()
                json_text = unquote(json_text)
                json_text = json_text[1:-1]
                data = json.loads(json_text)

        return data

    def find_vacancy_catalog(self, data):
        if data is not None:
            for key in data:
                if "single-page" in key:
                    jobs = data[key]["data"]["catalog"]["items"]
                    if not jobs:
                        return "Не найдено вакансий"
                    else:
                        return jobs

    def vacancy(self, job):
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
        print(parsed_job)
        return parsed_job

    def find_number_of_vacancies(self):
        data = self.response_to_json()
        if data is not None:
            for key in data:
                if "single-page" in key:
                    number_of_vacancies = data[key]["data"]["totalCount"]
                    return number_of_vacancies

    def result(self):
        data = self.response_to_json()
        jobs = self.find_vacancy_catalog(data)
        parsed_jobs = []
        for job in jobs:
            if job.get("id"):
                parsed_job = self.vacancy(job)
                parsed_jobs.append(parsed_job)
        return parsed_jobs
