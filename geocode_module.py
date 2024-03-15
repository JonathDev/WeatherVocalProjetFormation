from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeopyError
from cambert_module import recup_loc
from utilities import put_data_to_file_json


def city_to_coordinates(city):
    geolocator = Nominatim(user_agent="vocal_weather_app")
    
    try:
        # Tente de récupérer les informations de localisation pour la ville donnée
        location = geolocator.geocode(city)
        
        # Si la localisation est trouvée, extrait les coordonnées
        if location:
            lat = location.latitude
            lon = location.longitude
            put_data_to_file_json(file_path='enregistrement.json', key_json='lat', value=lat)
            put_data_to_file_json(file_path='enregistrement.json', key_json='lon', value=lon)
            return {'statut': 200,"message" : "reussit", 'lat': lat, 'lon': lon}
        else:
            # Si la localisation n'est pas trouvée, retourne un message d'erreur
            return {'statut': 404, 'message': 'La ville spécifiée ne peut pas être trouvée.'}

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        # Gestion des erreurs liées à un timeout ou un service indisponible
        return {'statut': 503, 'message': 'Le service de géolocalisation est temporairement indisponible.'}

    except GeopyError as e:
        # Gestion des autres types d'erreurs
        return {'statut': 500, 'message': f'Une erreur est survenue lors de la recherche de la ville : {e}'}
