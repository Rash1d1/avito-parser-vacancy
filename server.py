from fastapi import FastAPI
from pages.router import router as router_page
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI(title = "DemoParser")

app.include_router(router_page)

#uvicorn server:app --reload

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

