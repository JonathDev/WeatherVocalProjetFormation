import pyodbc
from dotenv import load_dotenv
import os


def monitoring(insert_query, values=None):
    load_dotenv()

    # Récupère les variables d'environnement
    SERVEUR = os.getenv('SERVEUR')
    ADMIUSER = os.getenv('ADMIUSER')
    DATABASE = os.getenv('DATABASE')
    PASSWORD = os.getenv('PASSWORD')
    
    # Configuration de votre connexion à la base de données
    conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVEUR},1433;Database={DATABASE};Uid={ADMIUSER};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    
    try:
        # Établissement de la connexion à la base de données
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                if values:
                    cursor.execute(insert_query, values)
                else:
                    cursor.execute(insert_query)
                # Valide les modifications si nécessaire
                conn.commit()
    except Exception as e:
        print(f"Error during database operation: {e}")
    


create_table_query = """
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
);"""


supprimer = """DROP TABLE IF EXISTS monitoringjo;"""
#monitoring(create_table_query)