#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
from __future__ import annotations
import datetime
import warnings
import altair as alt
import pandas as pd
import requests
import requests_cache
from datetime import datetime, timedelta

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1
def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API
    
    Args:
        date (datetime.date, optional): The date to fetch prices. Defaults to the current date if not provided.
        location (str, optional): The location code to fetch prices. Defaults to "NO1" if not provided.
    
    Returns:
        pd.DataFrame: A DataFrame containing the fetched prices.
    """
    if date is None:
        date = datetime.now().date()

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month:02d}-{date.day:02d}_{location}.json"
    
    # Using the requests library in Python to send an HTTP GET request to a specified URL
    r = requests.get(url)
   
    # Convert the r to JSON
    data = r.json()
    
    # Create a dataframe using the json data
    df = pd.DataFrame(data)
    
    # Converts the "time_start" column in the DataFrame to datetime format, assuming it is in UTC, and then converts the time zone to "Europe/Oslo."
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")

    # Return the DataFrame
    return df

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand ",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
    }

# task 5.1: 
def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame
    
    Args:
        end_date (datetime.date, optional): The end date for fetching prices. Defaults to None, the current date is used.
        days (int, optional): The number of days for which to fetch prices. Defaults to 7.
        locations (list[str], optional): The list of location codes for which to fetch prices. Defaults to all location codes in LOCATION_CODES.
    
    Returns:
        pd.DataFrame: A DataFrame containing the fetched prices.
    ...
    """
    # If end_date is not provided, set it to the current date
    if end_date is None:
        end_date = end_date or datetime.now().date()

    # Calculate the start date based on the provided number of days
    start_date = end_date - timedelta(days=days - 1)

    # Initialize an empty list to store the fetched data
    data = []

    # Loop through each date within the specified range
    for date in (start_date + timedelta(n) for n in range(days)):

        # For each date, fetch prices for all specified locations and extend the data list
        data.extend(fetch_day_prices(date, location).assign(
            location_code = location,
            location = LOCATION_CODES[location]
        ) for location in locations)
        
    # Concatenate the data list into a single DataFrame and return it
    return pd.concat(data, ignore_index=True)

# task 5.1:  
def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time
    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    
    Returns:
        alt.Chart: Altair chart displaying energy prices over time, with x-axis as 'time_start'
        and y-axis as 'NOK_per_kWh'', each location represented by its own line.

    """
    # Aggregate the data by taking the average of 'NOK_per_kWh' for each 'time_start' and 'location'
    aggregated_df = df.groupby(['time_start', 'location']).agg({'NOK_per_kWh': 'mean'}).reset_index()

    chart = alt.Chart(df).mark_line().encode(
        # Define the x-axis: time_start, with custom title, axis format, and label angle
        x = alt.X('time_start:T', title='time_start', axis=alt.Axis(format='%-e %b', labelAngle=-45)),
        # Define the y-axis: NOK_per_kWh as quantitative variable
        y ='NOK_per_kWh:Q',
        # Color the lines based on the 'location' variable
        color ='location:N',
        # Display tooltips for specified variables
        tooltip =['location', 'NOK_per_kWh', 'time_start']
    )
    return chart

# Task 5.4
def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...

# Task 5.6
# Defining activities and the engery used
ACTIVITIES = {
    "shower": 2.5,
    "cooking": 3.0,
    "watch_tv": 1.0,
    "baking": 2.0,  
    "heat": 1.5,    
} 

def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Args:
        df (pd.DataFrame): DataFrame containing energy prices.
        activity (str): Name of the specific activity (e.g., 'shower', 'heat') for which to plot prices.
        minutes (float): Duration of the activity in minutes.

    Returns:
        alt.Chart: Altair chart displaying energy prices for the specified activity.
    """

    if activity not in ACTIVITIES:
        raise ValueError(f"Invalid activity: {activity}. Available activities: {', '.join(ACTIVITIES.keys())}")

    # Add the 'activity' column to the DataFrame
    df['activity'] = activity

    # Filter data for specified activity
    data_for_activity = df[df['activity'] == activity]

    # Calculate cost for the activity 
    data_for_activity['cost'] = data_for_activity['NOK_per_kWh'] * ACTIVITIES[activity] * (minutes / 60)

    # Creating altair chart
    chart = alt.Chart(data_for_activity).mark_line().encode(
        x=alt.X('time_start:T', title='Time in hour'),
        y=alt.Y('cost:Q', title='Cost(øre/kWh)'),
        color='location:N',
        tooltip=['location', 'cost', 'time_start']
    ).properties(
        title=f'Cost of {activity} over time'
    )
    return chart


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
