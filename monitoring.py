from Stt_module import recognize_from_microphone
from cambert_module import nlp_data_stt, recup_date, recup_loc

from dbb_module import monitoring
from geocode_module import city_to_coordinates
from meteo_module import recup_data_meteo
from datetime import datetime
import json

def trigger_recognition_event():
    errors = {}
    results = {}

    # Recognition
    try:
        text_dict = recognize_from_microphone()
        results['text'] = text_dict['message']
        results['recognize_statut'] = text_dict['statut']
    except Exception as e:
        errors['recognition'] = str(e)

    # NLP
    try:
        if 'text' in results:
            data_dict = nlp_data_stt(results['text'])
            results['location'] = data_dict['Location']
            results['dates'] = data_dict['Dates']
            results['message_nlp'] = data_dict['message']
            results['data_nlp_statut'] = data_dict['statut']
        else:
            raise ValueError("No text available for NLP")
    except Exception as e:
        errors['nlp'] = str(e)

    # Location
    try:
        if 'location' in results:
            city = recup_loc(results['location'])
            data_location_dict = city_to_coordinates(city)
            results['recup_location'] = city
            results['lat'] = data_location_dict['lat']
            results['lon'] = data_location_dict['lon']
            results['coordinates_statut'] = data_location_dict['statut']
            results['message_location'] = data_location_dict['message']
        else:
            raise ValueError("No location available for geocoding")
    except Exception as e:
        errors['location'] = str(e)

    # Date Processing
    try:
        if 'dates' in results:
            donnée_date_dict = recup_date(results['dates'])
    
            # Si seulement une date est disponible, définir cette date comme date de début et de fin
            if len(donnée_date_dict) == 1:
                unique_date = donnée_date_dict.get('Date_ref', '')[0] if donnée_date_dict.get('Date_ref') else None
                print(f'test date : {unique_date}', type(unique_date))
                # Assurez-vous que unique_date est formatée comme une chaîne 'YYYY-MM-DD'
                if isinstance(unique_date, str):
                    try:
                        formatted_date = datetime.strptime(unique_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                    except ValueError:
                        raise ValueError("Date is not in the expected format 'YYYY-MM-DD'")
                else :
                    formatted_date = unique_date.strftime('%Y-%m-%d')
                results['date_debut'] = formatted_date
                print(f"test sur results[debut] {results['date_debut']}", type(results['date_debut']) )
                results['date_fin'] = formatted_date
                """
                results['date_debut'] = formatted_date if isinstance(date_debut, str) else date_debut.strftime('%Y-%m-%d')
                results['date_fin'] = formatted_date if isinstance(date_fin, str) else date_fin.strftime('%Y-%m-%d')
                """
            # Si deux dates sont disponibles, les utiliser comme dates de début et de fin respectivement
            elif len(donnée_date_dict) == 2:
                # Assurez-vous que les dates sont correctement formatées
                date_debut = donnée_date_dict.get('Date_debut', '')
                date_fin = donnée_date_dict.get('Date_fin', '')
                results['date_debut'] = date_debut if isinstance(date_debut, str) else date_debut.strftime('%Y-%m-%d')
                results['date_fin'] = date_fin if isinstance(date_fin, str) else date_fin.strftime('%Y-%m-%d')
                print(f"a la c'est quoi : {results['date_debut']}", type(results['date_debut']))
            else:
                raise ValueError("Invalid date data found")
        else:
            raise ValueError("No dates available for processing")
    except Exception as e:
        errors['date_processing'] = str(e)
    
    
    # Weather Data Retrieval
    try:
        if all(k in results for k in ['date_debut', 'date_fin', 'lat', 'lon']):
            recup_data_meteo_dict = recup_data_meteo(results['date_debut'], results['date_fin'], results['lat'], results['lon'])
            results['statut_api_meteo'] = recup_data_meteo_dict['statut']
            results['message_api_meteo'] = recup_data_meteo_dict['message']
            results['dataframe_api_meteo'] = recup_data_meteo_dict['data']
        else:
            raise ValueError("Incomplete data for weather retrieval")
    except Exception as e:
        errors['weather_data_retrieval'] = str(e)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Log the data and errors
    log_monitoring_data(now, results, errors)

    # Optionally, return results and errors for further processing
    return {'results': results, 'errors': errors}


def log_monitoring_data(timestamp, results, errors):
    # Assurez-vous que les valeurs de lat et lon peuvent être traitées correctement, même lorsqu'elles sont NULL.
    lat = results.get('lat')
    lon = results.get('lon')
    lat_value = 'NULL' if lat is None else str(lat)
    lon_value = 'NULL' if lon is None else str(lon)
     # Les dates doivent être passées directement sans conversion en chaîne pour 'NULL'
    date_debut = results.get('date_debut')
    date_fin = results.get('date_fin')
    print(date_debut)

    # Convertir en objet date si ce sont des chaînes
    from datetime import datetime
    if isinstance(date_debut, str):
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
    if isinstance(date_fin, str):
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()

    # Construction sécurisée de la requête SQL en évitant les erreurs de syntaxe pour les chaînes et dates.
    insert_query = f"""
    INSERT INTO monitoringjo (
        Time,
        Text, 
        RecognizeStatut, 
        NLPMessage, 
        NLPStatut, 
        Location, 
        Latitude, 
        Longitude, 
        CoordinatesStatut, 
        MessageLocation, 
        DateBegin, 
        DateEnd, 
        StatutApiMeteo, 
        MessageApiMeteo, 
        ErrorRecognition, 
        ErrorNLP, 
        ErrorLocation, 
        ErrorDateProcessing, 
        ErrorWeatherDataRetrieval
    ) VALUES (
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
    );
    """
    # Préparation des valeurs à insérer pour éviter les injections SQL et gérer correctement les chaînes et NULL
    values = (
        timestamp, 
        results.get('text', ''),
        results.get('recognize_statut', ''),
        results.get('message_nlp', ''),
        results.get('data_nlp_statut', ''),
        results.get('recup_location', ''),
        float(lat) if lat is not None else None,
        float(lon) if lon is not None else None,
        results.get('coordinates_statut', ''),
        results.get('message_location', ''),
        date_debut, 
        date_fin,
        results.get('statut_api_meteo', ''),
        results.get('message_api_meteo', ''),
        errors.get('recognition', ''),
        errors.get('nlp', ''),
        errors.get('location', ''),
        errors.get('date_processing', ''),
        errors.get('weather_data_retrieval', '')
    )
    
    try:
        # Supposons que `monitoring` est votre fonction pour exécuter des requêtes SQL.
        # Remplacez cette ligne par votre méthode d'exécution de requêtes SQL, en passant `insert_query` et `values`.
        # Exemple si vous utilisez pyodbc, cela pourrait ressembler à cursor.execute(insert_query, values)
        monitoring(insert_query, values)
    except Exception as e:
        print(f"Error during database logging: {e}")


test = trigger_recognition_event()
print(test)
print(test['results']['text'], type(test['results']))
print(test['results']['dataframe_api_meteo'], type(test['results']))