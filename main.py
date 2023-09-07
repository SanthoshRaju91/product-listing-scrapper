from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from scrapper import scrape_item_page

app = FastAPI()


class PageScrape(BaseModel):
    url: str


@app.post("/scrapping/perform")
def perform_scrapping(scrape: PageScrape):
    url = scrape.url
    details = scrape_item_page(url)
    return JSONResponse(content=details)

