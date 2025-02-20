from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from schemas import GetWeatherInsert, GetWeatherOutput, WeatherResponse
from models import WeatherTempStorage, AppInfo
from typing import Dict
from uuid import UUID, uuid4
import weather_getter
import weather_stat
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

temp_storage: Dict[UUID, WeatherTempStorage] = {}

API_KEY = os.getenv("API_KEY")


@app.get("/")
async def root():
    """
    Root endpoint for the weather app.

    Returns:
        dict: A message indicating the purpose of the app.
    """
    return {"message": "Hi! This app will help you get weather information."}


@app.get("/info", response_model=AppInfo)
async def get_info():
    """
    Endpoint to retrieve information about the app.

    Returns:
        AppInfo: Returns information about the app such as version, service name, and author.
    """

    return AppInfo()


@app.get("/info/allresponses")
async def get_weather_data():
    """
    Endpoint to retrieve all weather data stored in the app.

    Raises:
        HTTPException: If the storage is empty, returns 404 error.

    Returns:
        dict: All weather data stored in the application.
    """
    if not temp_storage:
        raise HTTPException(status_code=404, detail="Storage is empty")
    return temp_storage


@app.get("/info/responce/{item_id}")
async def get_weather_data_by_id(item_id: UUID):
    """
    Endpoint to retrieve specific weather data by its unique ID.

    Args:
        item_id (UUID): The unique ID of the weather data.

    Raises:
        HTTPException: If the ID is not found in storage, returns 404 error.

    Returns:
        WeatherTempStorage: The weather data associated with the provided ID.
    """
    if item_id not in temp_storage:
        raise HTTPException(status_code=404, detail="ID not found")
    return temp_storage[item_id]


@app.get("/info/weather")
async def get_weather_data(
    geo_place: str = None, date_start: str = None, date_end: str = None
):
    """
    Endpoint to fetch and calculate weather statistics (average, median, min, max)
    for a specific location and date range.

    Args:
        geo_place (str, optional): The location to retrieve weather data for.
        date_start (str, optional): The start date for weather data.
        date_end (str, optional): The end date for weather data.

    Returns:
        WeatherResponse: The weather statistics (average, median, min, max) for the specified location and date range.
    """
    params = {k: v for k, v in locals().items() if v is not None}
    insert_data = GetWeatherInsert(**params)
    responce = weather_getter.get_temp_data(API_KEY, insert_data)
    weather_data = responce.json()
    weather_data = weather_data["days"]
    weather_data_calculated = GetWeatherOutput(
        average=weather_stat.calc_mean(weather_data),
        median=weather_stat.calc_median(weather_data),
        min=weather_stat.calc_min(weather_data),
        max=weather_stat.calc_max(weather_data),
    )

    weather_id = uuid4()

    weather_storage = WeatherTempStorage(
        id=weather_id,
        geo_place=insert_data.geo_place,
        date_start=insert_data.date_start,
        date_end=insert_data.date_end,
        temp_value=[item["temp"] for item in weather_data],
        median_value=weather_data_calculated.median,
        avg_value=weather_data_calculated.average,
        min_value=weather_data_calculated.min,
        max_value=weather_data_calculated.max,
    )

    temp_storage[weather_id] = weather_storage

    weather_response_data = {"weather_stats": weather_data_calculated}
    return WeatherResponse(data=weather_response_data)


@app.delete("/info/responcedel/{item_id}")
async def delete_weather_data_by_id(item_id: UUID):
    """
    Endpoint to delete specific weather data by its unique ID.

    Args:
        item_id (UUID): The unique ID of the weather data to be deleted.

    Raises:
        HTTPException: If the ID is not found in storage, returns 404 error.

    Returns:
        dict: A message indicating the successful deletion of the weather data.
    """
    if item_id not in temp_storage:
        raise HTTPException(status_code=404, detail="ID not found")
    del temp_storage[item_id]
    return {"message": "Deleted successfully"}
