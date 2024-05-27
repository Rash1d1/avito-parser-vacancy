import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from GUI import ParserGUI
# p
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

def run_gui():
    app = ParserGUI()
    app.run()


if __name__ == '__main__':
    run_gui()
