from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import plotly.express as px
import json
from bokeh.plotting import figure
from bokeh.embed import json_item
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data_visualization import create_market_trend_figure
import plotly.graph_objects as go
from pydantic import BaseModel

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
    return templates.TemplateResponse("/portfolio/ilia_svetlichnyi.html", {"request": request})



@app.get("/data_for_plot")
async def get_data_for_plot():
    return create_market_trend_figure()

@app.get("/plot")
def get_plot():
    # Create a new plot
    p = figure(width=400, height=400)
    # Add a circle glyph to the figure p
    p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
    # Return the plot as a JSON object
    return JSONResponse(json_item(p, "myplot"))


class Chart(BaseModel):
    data: dict
    layout: dict

@app.get("/bar_chart")
async def bar_chart():
    chart_data = go.Bar(x=['giraffes', 'orangutans', 'monkeys'], y=[20, 14, 23])
    layout = go.Layout(title='Hello World Bar Chart')

    chart = Chart(data=chart_data.to_plotly_json(), layout=layout.to_plotly_json())

    return JSONResponse(content=json.loads(chart.json(by_alias=True)))
