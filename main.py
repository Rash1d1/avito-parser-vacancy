import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from GUI import ParserGUI

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
app = ParserGUI()

# start of program
def run_gui():
    app.run()


if __name__ == '__main__':
    run_gui()
