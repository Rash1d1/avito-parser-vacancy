import os

from loguru import logger



class Config:
    url_to_parse = ""
    scrapper_api = "37139fa7db77fc90ad7249ccb87b50f9"
    limit = 80
    location_of_result_file = ""
    proxies = {
        "https": "http://lte1:MIoQTQVFvO@65.21.29.211:50408",
        "http": "http://lte1:MIoQTQVFvO@65.21.29.211:50408"
    }
    def __init__(self, url, limit, filename):
        self.url_to_parse = url
        self.limit = limit
        self.set_location_of_result_file(filename)

    def set_location_of_result_file(self, file_name):
        script_dir = os.path.dirname(__file__)
        rel_path = "Results\\" + file_name + ".xlsx"
        self.location_of_result_file = os.path.join(script_dir, rel_path)
