import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class VacancyParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер вакансий")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{int(self.screen_width * 0.8)}x{int(self.screen_height * 0.8)}")
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self.root, text="URL:")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack(pady=5, fill=tk.X)

        self.check_button = tk.Button(self.root, text="Проверить количество найденных вакансий",
                                      command=self.check_vacancy_count)
        self.check_button.pack(pady=10, fill=tk.X)

        self.output_label = tk.Label(self.root, text="Имя файла для выгрузки данных:")
        self.output_label.pack(pady=10)

        self.output_entry = tk.Entry(self.root)
        self.output_entry.pack(pady=5, fill=tk.X)

        self.export_button = tk.Button(self.root, text="Выгрузить", command=self.export_data)
        self.export_button.pack(pady=10, fill=tk.X)

        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=int(self.screen_width * 0.6),
                                           mode="determinate")
        self.progressbar.pack(pady=20, fill=tk.X)
    def check_vacancy_count(self):
        messagebox.showinfo("Information", "Implement logic to check the number of found vacancies")

    def export_data(self):
        messagebox.showinfo("Information", "Implement logic to export data")

    def run(self):
        self.root.mainloop()