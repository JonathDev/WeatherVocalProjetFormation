"""

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
  
  
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["apparent_temperature"] = apparent_temperature
	hourly_data["precipitation"] = precipitation
	hourly_data["rain"] = rain
	hourly_data["wind_speed_10m"] = wind_speed_10m
	hourly_data["wind_direction_10m"] = wind_direction_10m
 
    hourly_dataframe = pd.DataFrame(data = hourly_data)
	print(hourly_dataframe)
 """
 
 """
# Charge les variables d'environnement depuis '.env'
load_dotenv()

SERVEUR = os.getenv('SERVEUR')
USER = os.getenv('ADMIUSER')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
print(USER)
# Chaîne de connexion stockée dans une variable
cnxn_str = f'Driver={'ODBC Driver 18 for SQL Server'};Server=tcp:{SERVEUR},1433;Database={DATABASE};Uid={USER};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Utiliser la chaîne de connexion pour établir une connexion
conn = pyodbc.connect(cnxn_str)

#creer un curser 
cursor = conn.cursor()

# Définition de la requête SQL pour créer une nouvelle table
"""
create_table_query = """
CREATE TABLE monitoringjo (
    Time DATETIME PRIMARY KEY,
    ServiceSTTAzureStatut int,
    ServiceSTTAzureResponse VARCHAR(1000),
    ModuleNlpStatut int,
    cityNlp VARCHAR(100),
    dateNlp VARCHAR(100), 
    statutLocalisatio int, 
    verificationLocationLatitude int,
    verificationLocationLongetude int,
    statutAPImeteo int, 
);
"""

supprimer = """DROP TABLE IF EXISTS monitoringjo;"""
"""


# Exécution de la requête pour créer la table
try:
    cursor.execute(create_table_query)
    cursor.commit()  # N'oubliez pas de valider (commit) la transaction si vous modifiez la base de données
    print("requête valide.")
except pyodbc.Error as e:
    print("Une erreur est survenue lors de la création de la table :", e)


    
cursor.close()
conn.close()
# Afficher un message pour confirmer l'établissement de la connexion
print("Connexion établie avec succès.")

# creation d'une table 
# insert des données sur la base youtube


"""
f"""
INSERT INTO tablejo (
    Time,
    ServiceSTTAzureStatut,
    ServiceSTTAzureResponse,
    cityNlp,
    dateNlp,
    statutLocalisatio,
    verificationLocalistaion,
    statutAPImeteo,
    parametreMetro,
    statusretourmeteo,
    StatutAPImap
) VALUES (
    '2023-03-13 12:34:56',  -- Time (DATETIME)
    1,                       -- ServiceSTTAzureStatut (int)
    'Réponse exemple',       -- ServiceSTTAzureResponse (VARCHAR)
    'Paris',                 -- cityNlp (VARCHAR)
    '2023-03-13',            -- dateNlp (VARCHAR)
    1,                       -- statutLocalisatio (int)
    'Vérification OK',       -- verificationLocalistaion (VARCHAR)
    1,                       -- statutAPImeteo (int)
    'Température, Humidité', -- parametreMetro (VARCHAR)
    1,                       -- statusretourmeteo (int)
    1                        -- StatutAPImap (int)
);
"""

from Stt_module import recognize_from_microphone
from cambert_module import nlp_data_stt, recup_date, recup_loc

from dbb_module import monitoring
from geocode_module import city_to_coordinates
from meteo_module import recup_data_meteo
from datetime import datetime
import json

def trigger_recognition_event():
    try:
        """recognize"""
        text_dict = recognize_from_microphone()
        text = text_dict['message']
        recognize_statut = text_dict['statut']
    except Exception as e:
        print(f"Error during recognition: {e}")
        return {"error": "Recognition failed"}

    try:
        """nlp"""
        data_dict = nlp_data_stt(text)
        location = data_dict['Location']
        dates = data_dict['Dates']
        message_nlp = data_dict['message']
        data_nlp_statut = data_dict['statut']
    except Exception as e:
        print(f"Error during NLP processing: {e}")
        return {"error": "NLP processing failed"}

    try:
        city = recup_loc(location)
        recup_location = city
        data_location_dict = city_to_coordinates(city)
        lat = data_location_dict['lat']
        lon = data_location_dict['lon']
        coordinates_statut = data_location_dict['statut']
        message_location = data_location_dict['message']
    except Exception as e:
        print(f"Error during location processing: {e}")
        return {"error": "Location processing failed"}

    try:
        donnée_date_dict = recup_date(dates)
        if len(donnée_date_dict) == 1:
            date_debut = date_fin = donnée_date_dict['Date_ref']
        elif len(donnée_date_dict) == 2:
            date_debut = donnée_date_dict['Date_debut']
            date_fin = donnée_date_dict['Date_fin']
        else:
            print("No dates found")
            return {"error": "No dates found"}
        date_debut_monitoring = json.dumps(date_debut)
        date_fin_monitoring = json.dumps(date_fin)
    except Exception as e:
        print(f"Error during date processing: {e}")
        return {"error": "Date processing failed"}

    try:
        recup_data_meteo_dict = recup_data_meteo(date_debut, date_fin, lat, lon)
        statut_api_meteo = recup_data_meteo_dict['statut']
        message_api_meteo = recup_data_meteo_dict['message']
        dataframe_api_meteo = recup_data_meteo_dict['data']
    except Exception as e:
        print(f"Error during weather data retrieval: {e}")
        return {"error": "Weather data retrieval failed"}

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = f"""
        INSERT INTO monitoringjo(
        Time,
        ServiceSttAzureStatut,
        ServiceSttAzureResponse,
        ModuleNlpStatut,
        MessageNlp,
        LocationNlp,
        DateBegin, 
        DateEnd, 
        StatutLocation,
        MessageLocation,
        Lat,
        Lon,
        StatutApiMeteo,
        MessageApiMeteo 
        ) VALUES (
        '{now}', 
        {recognize_statut},
        '{text}',
        {data_nlp_statut},
        '{message_nlp}',
        '{recup_location}',
        '{date_debut_monitoring}', 
        '{date_fin_monitoring}',
        {coordinates_statut},
        '{message_location}',
        {lat},
        {lon},
        {statut_api_meteo},
        '{message_api_meteo}'
        );"""

    try:
        monitoring(insert_query)
    except Exception as e:
        print(f"Error during database monitoring: {e}")
        return {"error": "Database monitoring failed"}

    return {'message': text, 'location': recup_location, 'lat': lat, 'lon': lon, 'date_debut': date_debut, 'date_fin': date_fin, 'data': dataframe_api_meteo}






CREATE TABLE monitoringjo (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Time DATETIME NOT NULL,
    Text NVARCHAR(MAX),
    RecognizeStatut NVARCHAR(255),
    NLPMessage NVARCHAR(MAX),
    NLPStatut NVARCHAR(255),
    Location NVARCHAR(255),
    Latitude FLOAT,
    Longitude FLOAT,
    CoordinatesStatut NVARCHAR(255),
    MessageLocation NVARCHAR(MAX),
    DateBegin NVARCHAR(255),
    DateEnd NVARCHAR(255),
    StatutApiMeteo NVARCHAR(255),
    MessageApiMeteo NVARCHAR(MAX),
    ErrorRecognition NVARCHAR(MAX),
    ErrorNLP NVARCHAR(MAX),
    ErrorLocation NVARCHAR(MAX),
    ErrorDateProcessing NVARCHAR(MAX),
    ErrorWeatherDataRetrieval NVARCHAR(MAX)
);