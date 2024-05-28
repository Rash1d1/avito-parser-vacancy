from fastapi import FastAPI
from pages.router import router as router_page

app = FastAPI(title = "DemoParser")

app.include_router(router_page)


@app.get("/")
def hello():
    return "hello"