import unicodedata
from config import LINK

class VacancySerializer:

    def __init__(self, job_data):
        self.data = job_data

    def salary(self):
        try:
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
        except:
            return None

    def currency(self):
        try:
            currency_symbols = ['$', '€', '£', '¥', '₹', '₽', '฿', '₿', '₴', '₩', '₺', '₸', '₮', '₦', '₱', '₲', '₳',
                                '₵',
                                '₡',
                                '₢', '₣', '₤', '₥', '₰', '₶', '₷', '₸', '₹', '₺', '₻', '₼', '₽', '₾', '₿']

            if isinstance(self.data["priceDetailed"]["fullString"], str):
                for char in self.data["priceDetailed"]["fullString"]:
                    if unicodedata.category(char) == 'Sc' or char in currency_symbols:
                        return char

            return None
        except:
            return None

    def salary_schedule(self):
        try:
            if "за смену" in self.data["priceDetailed"]["fullString"]:
                return "За смену"
            else:
                if isinstance(self.data["iva"]["ParamsStep"][0]["payload"]["text"], str):
                    salary_schedule_string = self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
                    for string in salary_schedule_string:
                        if "Выплаты" in string:
                            return string.replace("Выплаты", "").strip()
                    return None
        except:
            return None


    def schedule(self):
        try:
            return self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")[0]
        except:
            return None

    def experience(self):
        try:
            if isinstance(self.data["iva"]["ParamsStep"][0]["payload"]["text"], str):
                schedule_string = self.data["iva"]["ParamsStep"][0]["payload"]["text"].split("·")
                for string in schedule_string:
                    if "Опыт" in string:
                        return string.replace("Опыт", "").strip()
                return None
        except:
            return None

    def employer(self):
        try:
            return self.data["iva"]["UserInfoStep"][0]["payload"]["profile"]["title"]
        except:
            return None

    def employer_link(self):
        try:
            return LINK + str(self.data["iva"]["UserInfoStep"][0]["payload"]["profile"]["link"])
        except:
            return None

    def location(self):
        try:
            s1 = self.data["coords"]["address_user"]
            s2 = self.data["iva"]["GeoStep"][0]["payload"]["geoForItems"]["formattedAddress"]
            return max(s1, s2, key=len)
        except:
            return None


