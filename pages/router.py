from fastapi import APIRouter, Request, File, HTTPException
from fastapi.responses import JSONResponse, Response
from config import Config
from fastapi.templating import Jinja2Templates
from excel_storage import ExcelStorage
import asyncio
from prsr import Parser, ParserState

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@router.post("/base")
async def post_base_page(request: Request):
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

    asyncio.get_event_loop().run_until_complete(p.parse())

    try:
        with open("C:/Users/Rash/PycharmProjects/avito-parser-vacancy/Results/Результат.xlsx", 'rb') as f:
            # Create a FastAPI Response object from the open file object
            response = Response(f, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # Set the response headers to force the browser to download the file
            response.headers['Content-Disposition'] = 'attachment; filename=file.xlsx'
            # Return the file as a downloadable object
            return response
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='File not found')
