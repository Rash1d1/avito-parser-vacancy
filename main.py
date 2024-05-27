import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from GUI import ParserGUI
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


async def main():
    app = ParserGUI()
    app.run()


if __name__ == '__main__':
    asyncio.run(main())
