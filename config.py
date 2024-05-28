import os

from loguru import logger

logger.add("out.log", format="{time}, {level}, {message}", level="DEBUG")

class Config:
    url_to_parse = ""
    scrapper_api = "4f27ac93dc6fdd05736794124b7c468c"
    limit = 80
    location_of_result_file = ""
    proxies = {
        "https": "http://IKbS7Ni7cn:IMSO7V1FP9@51.15.15.230:10318",
        "http": "http://IKbS7Ni7cn:IMSO7V1FP9@51.15.15.230:10318"
    }
    def set_url_to_parse(self, url):
        self.url_to_parse = url

    def set_location_of_result_file(self, file_name):
        script_dir = os.path.dirname(__file__)
        rel_path = "Results\\" + file_name + ".xlsx"
        self.location_of_result_file = os.path.join(script_dir, rel_path)
