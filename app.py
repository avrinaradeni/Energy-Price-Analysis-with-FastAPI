"""
strompris fastapi app entrypoint
"""
from __future__ import annotations
from typing import List, Optional
import datetime
import os
import altair as alt
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices, 
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Check if the '_build' directory exists before StaticFiles
build_directory = "docs/_build"
if os.path.exists(build_directory):
    app.mount("/help", StaticFiles(directory=build_directory, html=True), name="help")


# `GET /` should render the `strompris.html` template
# with inputs:
# - request (Request): The incoming FastAPI Request object.
# - location_codes (dict): Dictionary mapping location codes to location names.
# - today (date): The current date.
@app.get("/")
async def root(request: Request):
    """
    Render the `strompris.html` template with the specific inputs.

    Args:
        request (Request): The incoming FastAPI Request object.
    
    Returns:
        TemplateResponse: Rendered response using the `strompris.html` template.
    """
    return templates.TemplateResponse("strompris.html", {
        "request": request,
        "location_codes": LOCATION_CODES,
        "today": datetime.date.today()
    })

# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)
@app.get("/plot_prices.json")
async def plot_prices_json(
    locations: Optional[List[str]] = Query(None),
    end: Optional[str] = None,
    days: Optional[int] = 7
):
    """
    Get a JSON chart for energy prices over time.

    Args:
        locations (List[str], optional): List of location codes. Defaults to all locations.
        end (str, optional): End date. Defaults to the current date.
        days (int, optional): Number of days. Defaults to 7.

    Returns:
        dict: Vega-Lite JSON chart produced by `plot_prices`.
    """
    # Use all locations if not provided
    locations = locations or list(LOCATION_CODES.keys())

    # Convert the end date to a datetime object
    if end:
        end_date = datetime.date.fromisoformat(end)
    else:
        end_date = datetime.date.today()

    # Fetch prices and create the chart
    df = fetch_prices(end_date=end_date, days=days, locations=locations)
    chart = plot_prices(df)
    return chart.to_dict()

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date
@app.get("/activity")
async def activity(request: Request):
    """
    Render the `activity.html` template with the specified inputs.

    Args:
        request (Request): The incoming FastAPI Request object.
    
    Returns:
        TemplateResponse: Rendered response using the `activity.html` template.
    """
    return templates.TemplateResponse("activity.html", {
        "request": request,
        "location_codes": LOCATION_CODES,
        "activities": ACTIVITIES,
        "today": datetime.date.today()
    })

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)
@app.get("/plot_activity.json")
async def plot_activity_json(
    location: str = "NO1",
    activity: str = "shower",
    minutes: int = 10
):
    """
    Get a JSON chart for the specified activity.

    Args:
        location (str, optional): Location code. Defaults to "NO1".
        activity (str, optional): Name of the activity. Defaults to "shower".
        minutes (int, optional): Duration of the activity in minutes. Defaults to 10.

    Returns:
        dict: JSON chart produced by `plot_activity_prices`.
    """
    # Get the current date
    end_date = datetime.date.today()
    # Fetch prices for the current day
    df = fetch_prices(end_date=end_date, days=1, locations=[location])
    # Create a chart using the fetched data and specified activity parameters
    chart = plot_activity_prices(df, activity, minutes)
    # Convert the chart to a dictionary format for response and return it 
    return chart.to_dict()


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    main()
