from fastapi import FastAPI
from excel_storage import ExcelStorage
from fastapi.responses import HTMLResponse
from fastapi import Request
from prsr import Parser, ParserState
from config import Config
import asyncio
from fastapi.responses import Response


app = FastAPI(title="Parser")



# uvicorn server:app --reload
# ngrok http 8000 --domain killdeer-up-hawk.ngrok-free.app
# https://killdeer-up-hawk.ngrok-free.app

@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

class User:
    result = None
    parser: Parser = None
    config: Config = None
    ip: str

users: dict[str, User] = {}

def get_user(request: Request):
    global users
    ip = request.client.host
    user = users.get(ip)
    if not user:
        user = User()
        user.ip = ip
        users[ip] = user
    return user

@app.post("/parse")
async def start(request: Request):
    user = get_user(request)
    data = await request.json()

    cfg = Config(
        url=data['url'],
        filename=data.get('filename', "результат"),
        limit=data['pageLimit']
    )
    storage = ExcelStorage(cfg.location_of_result_file)
    state = ParserState(url=data['url'])

    user.config = cfg

    p = Parser(cfg, storage, state)

    user.parser = p
    task = asyncio.create_task(p.parse())

    await asyncio.gather(task)
    users[user.ip].result = True


@app.get("/result")
def get_result(request: Request):
    user = get_user(request)
    parsed = 0
    total = 0
    if user.parser:
        parsed = user.parser.number_of_parsed_items
        total = user.parser.number_of_items

    response = None
    if user.result:
        with open(user.parser.cfg.location_of_result_file, 'rb') as f:
            content = f.read()
            response = Response(content=content,
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            response.headers['Content-Disposition'] = 'attachment; filename=file.xlsx'
            users[user.ip].result = False
    else:
        response = Response(status_code=204)
        response.headers['X-Result'] = 'false'

    response.headers['parsed'] = str(parsed)
    response.headers['total'] = str(total)
    return response



@app.post("/check")
async def get_result(request: Request):
    data = await request.json()
    state = ParserState(url=data['url'])
    print(state.number)
    response = Response(status_code=204)
    response.headers['total'] = str(state.number)
    return response