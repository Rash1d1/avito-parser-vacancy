import asyncio
import tkinter as tk
from asyncio import WindowsSelectorEventLoopPolicy
from GUI import VacancyParserGUI
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


async def main():
    root = tk.Tk()
    app = VacancyParserGUI(root)
    app.run()


if __name__ == '__main__':
    asyncio.run(main())
