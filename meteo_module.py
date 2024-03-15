import requests
import requests_cache
from retry_requests import retry
import openmeteo_requests
import pandas as pd
from datetime import datetime


def recup_data_meteo(date_debut="2024-03-14", date_fin="2024-03-16", lat=52.52, lon=13.41):
    print(date_debut, date_fin, lat, lon)
    try:
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
            "start_date": date_debut,
            "end_date": date_fin
        }
        response = cache_session.get(url, params=params)
        data = response.json()  # Supposons une réponse JSON

        if 'daily' in data:
            daily_data = data['daily']
            dates = pd.date_range(start=date_debut, end=date_fin)
            daily_dataframe = pd.DataFrame(daily_data, index=dates)
            print(daily_dataframe)
            return {'statut': 200, 'message': 'réussit', 'data': daily_dataframe}
        else:
            return {'statut': 500, 'message': "Données quotidiennes manquantes dans la réponse de l'API"}
    except Exception as e:
        return {'statut': 500, 'message': f"Une erreur est survenue lors de la récupération des données météo : {e}"}



async def read_dataFrame_for_information(id = 0, label = "temperature_2m_max"):
    df = recup_data_meteo()
    print(df) 
    return df.at[id, label]





