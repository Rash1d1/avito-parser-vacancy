
import asyncio
from prsr import parse
from asyncio import WindowsSelectorEventLoopPolicy

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

async def main():
    await parse()

if __name__ == '__main__':
    asyncio.run(main())
