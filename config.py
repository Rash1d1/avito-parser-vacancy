import os


class Config():
    url_to_parse = "https://www.avito.ru/tatarstan/vakansii?q=%D1%82%D0%BE%D0%BA%D0%B0%D1%80%D1%8C"
    LINK = "https://www.avito.ru"
    scrapper_api = "4f27ac93dc6fdd05736794124b7c468c"
    LIMIT = 80
    location_of_result_file = ""
    def set_url_to_parse(self, url):
        self.url_to_parse = url
    def set_location_of_result_file(self, file_name):
        script_dir = os.path.dirname(__file__)
        rel_path = "Results/" + file_name + ".xlsx"
        self.location_of_result_file = os.path.join(script_dir, rel_path)
