import asyncio
from prsr import start_parsing, find_number_of_vacancies
from customtkinter import *
from config import Config
import pyperclip
from tkinter import messagebox
# p

cfg = Config()

class ParserGUI:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("600x500")
        set_appearance_mode("dark")
        set_default_color_theme("blue")
        CTkLabel(master=self.app, text="Парсер Авито", fg_color="transparent", font=("Arial", 20),
                 text_color="#F5F5F5").pack(pady=50, padx=20)
        self.url_entry = CTkEntry(master=self.app, width=400,
                                  placeholder_text="Введите url первой страницы для парсинга",
                                  border_width=1, border_color="#F5F5F5", text_color="#F5F5F5")
        self.url_entry.pack(pady=5, padx=20)
        self.insert_url_button = CTkButton(master=self.app, text="Вставить url из буфера", command=self.url_button_event,
                  border_width=1, text_color="#F5F5F5")
        self.insert_url_button.pack(padx=20, pady=5)
        self.frame = CTkFrame(master=self.app, width=100, height=15)
        self.frame.pack(pady=20, padx=20)
        self.number_of_elems_label = CTkLabel(master=self.frame, text="Кол-во элементов: 0. Кол-во страниц: 0",  fg_color="transparent", font=("Arial", 20),
                 text_color="#F5F5F5")
        self.number_of_elems_label.pack(pady=5, padx=20)
        self.number_of_elems_button = CTkButton(master=self.frame, text="Проверить кол-во найденных элементов", command=self.number_of_elems_button_event,
                                      border_width=1, text_color="#F5F5F5")
        self.number_of_elems_button.pack(padx=20, pady=5)
        self.path_entry = CTkEntry(master=self.app, width=300,
                                   placeholder_text="Введите имя файла для выгрузки результата парсинга",
                                   border_width=1, border_color="#F5F5F5", text_color="#F5F5F5")
        self.path_entry.pack(pady=39, padx=10)
        self.parse_button = CTkButton(master=self.app, text="Выгрузить", command=self.parse_button_event,
                  border_width=1, text_color="#F5F5F5")
        self.parse_button.pack(padx=20, pady=5)

        self.progressbar = CTkProgressBar(master=self.app, width=400).pack(pady=10, padx=5)

    def number_of_elems_button_event(self):
        if self.url_entry.get() == "":
            messagebox.showinfo("Ошибка", "Введите url!")
        else:
            try:
                cfg.set_url_to_parse(self.url_entry.get())
                async def process_url():
                    n = await find_number_of_vacancies(cfg.url_to_parse)
                    self.number_of_elems_label.configure(
                        text=f"Кол-во элементов: {n}. Кол-во страниц: {n // 50 + 1}")
                    cfg.set_found_elements_number(n)

                # Create and run an event loop to execute the asynchronous function
                loop = asyncio.get_event_loop()
                loop.run_until_complete(process_url())
                loop.stop()
            except Exception as e:
                messagebox.showinfo("Ошибка", "Введен не валидный url")
                print(e)

    def url_button_event(self):
        self.url_entry.insert(0, pyperclip.paste())

    def parse_button_event(self):
        if self.path_entry.get() == "":
            messagebox.showinfo("Ошибка", "Введите имя файла для выгрузки результата!")
        else:
            cfg.set_url_to_parse(self.url_entry.get())
            cfg.set_location_of_result_file(self.path_entry.get())
            asyncio.run(start_parsing(cfg))
            messagebox.showinfo("Успех", str(Config.location_of_result_file))

    def run(self):
        self.app.mainloop()
