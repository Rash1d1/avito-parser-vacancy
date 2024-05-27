import unicodedata
from config import logger
# p
class VacancySerializer:

    def __init__(self, job_data):
        self.data = job_data

    @logger.catch()
    def salary(self):

        min_max_arr = [None, None]
        salary_string = self.data["priceDetailed"]["fullString"]
        if "до" in salary_string:
            digits_only = ''.join(filter(str.isdigit, salary_string))
            min_max_arr[1] = digits_only
        elif "от" in salary_string:
            digits_only = ''.join(filter(str.isdigit, salary_string))
            min_max_arr[0] = digits_only
        elif "—" in salary_string:
            from_to_digits = salary_string.split("—")
            min_max_arr[0] = "".join(filter(str.isdigit, from_to_digits[0]))
            min_max_arr[1] = "".join(filter(str.isdigit, from_to_digits[1]))
        return min_max_arr

    @logger.catch()
    def currency(self):

        currency_symbols = ['$', '€', '£', '¥', '₹', '₽', '฿', '₿', '₴', '₩', '₺', '₸', '₮', '₦', '₱', '₲', '₳',
                            '₵',
                            '₡',
                            '₢', '₣', '₤', '₥', '₰', '₶', '₷', '₸', '₹', '₺', '₻', '₼', '₽', '₾', '₿']

        if isinstance(self.data["priceDetailed"]["fullString"], str):
            for char in self.data["priceDetailed"]["fullString"]:
                if unicodedata.category(char) == 'Sc' or char in currency_symbols:
                    return char

    @logger.catch()
    def salary_schedule(self):

        if "за смену" in self.data["priceDetailed"]["fullString"]:
            return "За смену"
        else:
            if isinstance(self.data["iva"]["ParamsStep"][0]["payload"]["text"], str):
                salary_schedule_string = self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
                for string in salary_schedule_string:
                    if "Выплаты" in string:
                        return string.replace("Выплаты", "").strip()

    @logger.catch()
    def schedule(self):

        return self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")[0]

    @logger.catch()
    def experience(self):

        if isinstance(self.data["iva"]["ParamsStep"][0]["payload"]["text"], str):
            schedule_string = self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
            for string in schedule_string:
                if "Опыт" in string:
                    return string.replace("Опыт", "").strip()

    @logger.catch()
    def employer(self):

        return self.data["iva"]["UserInfoStep"][0]["payload"]["profile"]["title"]

    @logger.catch()
    def employer_link(self):

        return "https://www.avito.ru" + str(self.data["iva"]["UserInfoStep"][0]["payload"]["profile"]["link"])

    @logger.catch()
    def location(self):

        s1 = self.data["coords"]["address_user"]
        s2 = self.data["iva"]["GeoStep"][0]["payload"]["geoForItems"]["formattedAddress"]
        return max(s1, s2, key=len)
