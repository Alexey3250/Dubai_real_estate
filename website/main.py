from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import plotly.express as px
import asyncio
from bokeh.embed import json_item
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data_visualization import create_market_trend_figure



import logging


# Initialize logging
logging.basicConfig(level=logging.INFO)



app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mounting static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})

'''
@app.get("/market-trends")
def market_trends(request: Request):
    return templates.TemplateResponse("market-trends.html", {"request": request})
'''

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/portfolio/alexey_efimik")
def alexey_portfolio(request: Request):
    return templates.TemplateResponse("/portfolio/alexey_efimik.html", {"request": request})

@app.get("/portfolio/ilia_svetlichnyi")
def ilia_portfolio(request: Request):
    return templates.TemplateResponse("/portfolio/ilia_svetlichnyi.html", {"request": request})



# Function to load transaction data
async def load_transaction_data():
    global dashboard_data
    logging.info("Starting to load transaction data...")
    dashboard_data = pd.read_csv(r"C:\Users\Alex\Dubai_real_estate\website\data\transaction_data.csv")
    dashboard_data['instance_date'] = pd.to_datetime(dashboard_data['instance_date'])
    logging.info("Transaction data loaded successfully.")

# Function to prepare data for quarterly charts
async def prepare_quarterly_data():
    global quarterly_data, dashboard_data
    logging.info("Starting to prepare data for quarterly charts...")
    await asyncio.sleep(2)  # Simulate delay for processing

    # Create Year and Quarter columns
    dashboard_data['Year'] = dashboard_data['instance_date'].dt.year
    dashboard_data['Quarter'] = dashboard_data['instance_date'].dt.to_period("Q").astype(str)  # Convert to str

    # Aggregate by Year and Quarter
    quarterly_aggregate = dashboard_data.groupby(['Year', 'Quarter']).agg({
        'actual_worth': 'mean',
        'transaction_id': 'count'
    }).reset_index()

    quarterly_data = quarterly_aggregate
    logging.info("Quarterly data prepared successfully.")

# Startup event to load all necessary data
@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the application...")
    await load_transaction_data()
    await prepare_quarterly_data()
    logging.info("Background tasks completed.")

@app.get("/market-trends")
async def get_market_trends(request: Request):
    global dashboard_data, quarterly_data
    
    if 'instance_date' in dashboard_data.columns:
        if pd.api.types.is_datetime64_any_dtype(dashboard_data['instance_date']):
            dashboard_data['instance_date'] = dashboard_data['instance_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    clean_data = dashboard_data.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    response_data = {
        "transaction_data": clean_data.to_dict(),
        "quarterly_data": quarterly_data.to_dict(orient='records') if quarterly_data is not None else "Loading..."
    }
    
    return templates.TemplateResponse("market-trends.html", {"request": request, "data": response_data})


