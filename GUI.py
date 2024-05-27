from customtkinter import *
from config import Config

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
        self.insert_url_button = CTkButton(master=self.app, text="Вставить url из буфера", command=self.url_button_event(),
                  border_width=1, text_color="#F5F5F5")
        self.insert_url_button.pack(padx=20, pady=5)
        self.path_entry = CTkEntry(master=self.app, width=300,
                                   placeholder_text="Введите имя файла для выгрузки результата парсинга",
                                   border_width=1, border_color="#F5F5F5", text_color="#F5F5F5")
        self.path_entry.pack(pady=39, padx=10)
        self.parse_button = CTkButton(master=self.app, text="Выгрузить", command=self.parse_button_event(),
                  border_width=1, text_color="#F5F5F5")
        self.parse_button.pack(padx=20, pady=5)

        CTkProgressBar(master=self.app, width=400).pack(pady=10, padx=5)




    def url_button_event(self):
        pass

    def parse_button_event(self):
        print(3)
        if self.path_entry == "":
            print(True)
        else:
            cfg.set_url_to_parse(self.url_entry.get())
            cfg.set_location_of_result_file(self.path_entry.get())

    def run(self):
        self.app.mainloop()
