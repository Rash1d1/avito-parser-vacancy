from fastapi import FastAPI
from excel_storage import ExcelStorage
from fastapi.responses import HTMLResponse
from fastapi import Request
from prsr import Parser, ParserState
from config import Config
import asyncio
from fastapi.responses import Response
app = FastAPI(title="DemoParser")




# uvicorn server:app --reload

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


result = False
state_ = None

@app.post("/parse")
async def start(request: Request):
    global result
    global state_
    data = await request.json()
    url = data['url']
    page_limit = data['pageLimit']
    cfg = Config()
    cfg.set_url_to_parse(url)
    cfg.limit = page_limit
    cfg.set_location_of_result_file("Результат")
    storage = ExcelStorage(cfg.location_of_result_file)
    state = ParserState(url)

    p = Parser(cfg, storage, state)
    state_ = p
    task = asyncio.create_task(p.parse())
    await asyncio.gather(task)

    # закончилось
    result = True


@app.get("/result")
def get_result():
    global result
    global state_
    if result:
        with open("C:/Users/Rash/PycharmProjects/avito-parser-vacancy/Results/Результат.xlsx", 'rb') as f:
            content = f.read()
            response = Response(content=content,
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            response.headers['Content-Disposition'] = 'attachment; filename=file.xlsx'
            return response
    else:
        response = Response(status_code=204)
        response.headers['X-Result'] = 'false'
        response.headers['total'] = str(state_.number_of_items)
        response.headers['parsed'] = str(state_.number_of_parsed_items)
        return response