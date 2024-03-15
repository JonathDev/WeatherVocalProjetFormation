
import json
from geopy.geocoders import Nominatim
import time
from datetime import date
from datetime import datetime, timedelta
import re

def put_data_to_file_json(file_path='enregistrement.json', key_json=None, value=None):
    print("je rentre dans put-file")
    try:
        # Essayer de lire les données existantes si le fichier existe déjà
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
            data = {}

    # Mise à jour ou ajout de la nouvelle valeur pour la clé spécifiée
    data[key_json] = value

    # Réécrire le fichier JSON avec les données mises à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_file_enregistrement_json(file_path = 'enregistrement.json', key_json = "enregistrement"):
    print("je rentre dans read-file")
# Lire le contenu du fichier JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

# Accéder à une valeur spécifique en utilisant sa clé
    data_value = data.get(key_json)
    return data_value


def reset_file_json(file_path = 'enregistrement.json') :
    print("je rentre dans reset-file")
    # Suppression du contenu précédent du fichier JSON (si le fichier existe)
    open(file_path, 'w').close()    



def search_date_world(dates):
    print(f"Récupération des dates dans search_date_world: {dates}")
    search_text = ' '.join(dates) if isinstance(dates, list) else dates

    resultats = []
    pattern_date = r"(\d{1,2}) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) (\d{4})"
    pattern_date_sans_annee = r"(\d{1,2}) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)"
    terme_date = ["aujourd'hui", "demain", "après-demain", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

    for pattern in [pattern_date, pattern_date_sans_annee]:
        for match in re.finditer(pattern, search_text):
            resultats.append(match.group(0))

    for mot in terme_date:
        if mot in search_text:
            resultats.append(mot)

    print(f"Résultats trouvés dans search_date_world : {resultats}")
    return resultats if resultats else None


   
    
def convert_dates(search_dates = "samedi"):
    print(f'Récupération de la liste pour convert_dates {search_dates}', type(search_dates))
    converted_dates = []
    today = datetime.now()

    mois_en_anglais = {
        'janvier': 'January', 'février': 'February', 'mars': 'March', 'avril': 'April', 'mai': 'May',
        'juin': 'June', 'juillet': 'July', 'août': 'August', 'septembre': 'September',
        'octobre': 'October', 'novembre': 'November', 'décembre': 'December'
    }

    jours_de_la_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

    for date in search_dates:
        if date in ["aujourd'hui", "demain", "après-demain"]:
            offset = ["aujourd'hui", "demain", "après-demain"].index(date)
            converted_dates.append((today + timedelta(days=offset)).strftime('%Y-%m-%d'))
        elif date in jours_de_la_semaine:
            target_weekday = jours_de_la_semaine.index(date)
            days_until_target = (target_weekday - today.weekday() + 7) % 7
            days_until_target = 7 if days_until_target == 0 else days_until_target
            target_date = today + timedelta(days=days_until_target)
            converted_dates.append(target_date.strftime('%Y-%m-%d'))
        else:
            match = re.search(r"(\d{1,2}) (\w+) (\d{4})", date)
            if match:
                jour, mois, annee = match.groups()
                mois_en = mois_en_anglais[mois]
                date_obj = datetime.strptime(f"{jour} {mois_en} {annee}", "%d %B %Y")
                converted_dates.append(date_obj.strftime('%Y-%m-%d'))
            else:
                match = re.search(r"(\d{1,2}) (\w+)", date)
                if match:
                    jour, mois = match.groups()
                    mois_en = mois_en_anglais[mois]
                    date_obj = datetime.strptime(f"{jour} {mois_en} {today.year}", "%d %B %Y")
                    converted_dates.append(date_obj.strftime('%Y-%m-%d'))

    print(f'Résultats convertis pour convert_dates : {converted_dates}')
    return converted_dates

