import os.path
from openpyxl import Workbook
import pandas as pd
from tkinter import messagebox
# p
class ExcelStorage:
    headers = {
        'id': 'id',
        'title': 'Название',
        'url': 'Ссылка',
        'min_salary': 'Мин. зп',
        'max_salary': 'Макс. зп',
        'currency': 'Валюта',
        'salary_schedule': 'График выплат',
        'schedule': 'График работы',
        'experience': 'Опыт',
        'description': 'Описание',
        'employer': 'Работодатель',
        'link_to_employer': 'Ссылка на работодателя',
        'location': 'Местоположение',
        'date_of_publication': 'Дата публикации'
    }
    row_in_table = 2

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
            self.file = Workbook()
            ws = self.file.active
            for i, header in enumerate(self.headers.values(), start=1):
                cell = ws.cell(row=1, column=i)
                cell.value = header
            self.file.save(file_name)
        except:
            messagebox.showinfo("Ошибка", "Выбрано не валидное имя файла")

    def add_cell(self, parsed_item):
        self.data.append({header: getattr(parsed_item, attribute_name, '') for attribute_name, header in self.headers.items()})

    async def save_to_excel(self):
        df = pd.DataFrame(self.data)
        writer = pd.ExcelWriter(self.file_name, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()
