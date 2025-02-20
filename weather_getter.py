import requests
from schemas import GetWeatherInsert


def get_temp_data(API_KEY, insert_data: GetWeatherInsert):
    """
    Fetches weather data from the VisualCrossing API for a specified location and date range.

    Args:
        API_KEY (str): The API key required to authenticate the request.
        insert_data (GetWeatherInsert): An object containing the location (geo_place)
                                         and the date range (date_start and date_end) for the weather data request.

    Returns:
        Response: The response object from the requests library containing the weather data.
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{insert_data.geo_place}/{insert_data.date_start}/{insert_data.date_end}?key={API_KEY}&include=days&elements=temp,datetime&unitGroup=metric"
    response = requests.get(url)
    return response
