import asyncio
from prsr import Parser, ParserState
from customtkinter import *
from config import Config
import pyperclip
from tkinter import messagebox
from config import logger
from excel_storage import ExcelStorage

cfg = None
state = None

class ParserGUI:
    def __init__(self):
        self.init_app()
        self.init_widgets()
        self.init_layout()

    def init_app(self):
        self.app = CTk()
        self.app.geometry("600x550")
        set_appearance_mode("dark")
        set_default_color_theme("blue")

    def init_widgets(self):
        CTkLabel(master=self.app, text="Парсер Авито", fg_color="transparent", font=("Arial", 20),
                 text_color="#F5F5F5").pack(pady=50, padx=20)
        self.url_entry = CTkEntry(master=self.app, width=400,
                                  placeholder_text="Введите url первой страницы для парсинга",
                                  border_width=1, border_color="#F5F5F5", text_color="#F5F5F5")
        self.insert_url_button = CTkButton(master=self.app, text="Вставить url из буфера",
                                           command=self.url_button_event,
                                           border_width=1, text_color="#F5F5F5")
        self.frame = CTkFrame(master=self.app, width=100, height=15)
        self.number_of_elems_label = CTkLabel(master=self.frame, text="Кол-во элементов: 0. Кол-во страниц: 0",
                                              fg_color="transparent", font=("Arial", 20),
                                              text_color="#F5F5F5")
        self.number_of_elems_button = CTkButton(master=self.frame, text="Проверить кол-во найденных элементов",
                                                command=self.number_of_elems_button_event,
                                                border_width=1, text_color="#F5F5F5")
        self.path_entry = CTkEntry(master=self.app, width=300,
                                   placeholder_text="Введите имя файла для выгрузки результата парсинга",
                                   border_width=1, border_color="#F5F5F5", text_color="#F5F5F5")
        self.parse_button = CTkButton(master=self.app, text="Выгрузить", command=self.parse_button_event,
                                      border_width=1, text_color="#F5F5F5")
        self.progressbar = CTkProgressBar(master=self.app, width=400)
        self.progress_label = CTkLabel(master=self.app, text="Прогресс: _")

    def init_layout(self):
        self.url_entry.pack(pady=5, padx=20)
        self.insert_url_button.pack(padx=20, pady=5)
        self.frame.pack(pady=20, padx=20)
        self.number_of_elems_label.pack(pady=5, padx=20)
        self.number_of_elems_button.pack(padx=20, pady=5)
        self.path_entry.pack(pady=39, padx=10)
        self.parse_button.pack(padx=20, pady=5)
        self.progressbar.pack(pady=10, padx=5)
        self.progressbar.set(0)
        self.progress_label.pack(pady=3, padx=5)

    def process_url(self):
        global state
        try:
            state = ParserState(self.url_entry.get())
            n = state.number
            self.number_of_elems_label.configure(
                text=f"Кол-во элементов: {n}. Кол-во страниц: {min(n // 50 + 1, 100)}")
        except Exception as e:
            print(e)
            messagebox.showinfo("Ошибка", "Произошла ошибка при обработке URL")

    @logger.catch()
    def number_of_elems_button_event(self):
        if self.url_entry.get() == "":
            messagebox.showinfo("Ошибка", "Введите URL!")
        else:
            self.process_url()

    @logger.catch()
    def url_button_event(self):
        global state
        self.url_entry.insert(0, pyperclip.paste())

    @logger.catch()
    def parse_button_event(self):
        global state, cfg
        if self.path_entry.get() == "":
            messagebox.showinfo("Ошибка", "Введите имя файла для выгрузки результата!")
        elif self.url_entry.get() == "":
            messagebox.showinfo("Ошибка", "Введите URL!")
        else:
            cfg = Config(
                url=self.url_entry.get(),
                filename=self.path_entry.get(),
                limit=80
            )
            storage = ExcelStorage(cfg.location_of_result_file)
            def move_progress(i):
                self.progressbar.set(i / min(cfg.limit * 50, state.number))
                self.progress_label.configure(
                    text=f"Завершено на {round(i / min(cfg.limit * 50, state.number) * 100, 1)}%")
                self.app.update()

            state = ParserState(self.url_entry.get())
            p = Parser(cfg, storage, state, progress_callback=move_progress)
            asyncio.get_event_loop().run_until_complete(p.parse())
            self.progressbar.set(1)
            self.progress_label.configure(
                text=f"Завершено на 100%")
            self.app.update()

            messagebox.showinfo("Успех", str(Config.location_of_result_file))

    @logger.catch()
    def run(self):
        self.app.mainloop()


