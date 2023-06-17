from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mounting static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})

@app.get("/market-trends")
def market_trends(request: Request):
    return templates.TemplateResponse("market-trends.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/portfolio/alexey_efimik")
def alexey_portfolio(request: Request):
    return templates.TemplateResponse("/portfolio/alexey_efimik.html", {"request": request})

@app.get("/portfolio/ilia_svetlichnyi")
def ilia_portfolio(request: Request):
    return templates.TemplateResponse("/portfolio/ilia_svetlichnyi", {"request": request})
