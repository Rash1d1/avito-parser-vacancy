from fastapi import APIRouter, Request, File, HTTPException
from fastapi.responses import JSONResponse, Response
from config import Config
from fastapi.templating import Jinja2Templates
from excel_storage import ExcelStorage
import asyncio
from prsr import Parser, ParserState
from fastapi.routing import APIRoute
from typing import Optional, Dict


class MultiMethodRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        self.methods = kwargs.pop("methods", ["GET"])
        super().__init__(*args, **kwargs)


router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
    route_class=MultiMethodRoute
)

templates = Jinja2Templates(directory="templates")
request_status: str = ""


@router.route("/templates/index", methods=["GET", "POST"])
async def post_base_page(request: Request):
    global request_status
    if request.method == "POST":
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

        asyncio.create_task(p.parse())
        try:
            with open("C:/Users/Rash/PycharmProjects/avito-parser-vacancy/Results/Результат.xlsx", 'rb') as f:
                content = f.read()  # Read the binary data from the file

                # Create a FastAPI Response object with the binary data
                response = Response(content=content,
                                    media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                # Set the response headers to force the browser to download the file
                response.headers['Content-Disposition'] = 'attachment; filename=file.xlsx'

                # Mark the request as complete
                request_status = "1"

                # Return the file as a downloadable object
                return response
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail='File not found')
    else:
        print("GET try")
        return request_status



@router.get("/status")
async def get_status():
    return request_status
