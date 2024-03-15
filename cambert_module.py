from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from utilities import convert_dates, put_data_to_file_json, search_date_world

def nlp_data_stt(text):
    try:
        # Chargement du tokenizer et du modèle
        tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")

        # Initialisation du pipeline NLP
        nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

        # Exécution du pipeline sur le texte fourni
        results = nlp(text)
        
        # Initialisation des listes pour collecter les dates et les lieux
        dates = []
        locations = []

        # Filtrage et collecte des dates et des lieux
        for result in results:
            if result['entity_group'] == 'DATE':
                dates.append(result['word'])
            elif result['entity_group'] == 'LOC':
                locations.append(result['word'])

        # Retourne les dates et lieux trouvés avec un statut 200
        return {'statut': 200,"message" : "réussit" ,'Dates': dates, 'Location': locations}

    except Exception as e:
        # Gestion des exceptions avec un message d'erreur et un statut 500
        return {'statut': 500, 'message': f'Une erreur est survenue lors de l\'analyse du texte : {e}'}


def recup_loc(location):
    location =  location
    #print(data_stt)
    #location = data_stt['Location']
    loc = ''.join(location)
    #print(loc)
    put_data_to_file_json(file_path='enregistrement.json', key_json='city', value=loc)
    return loc


def recup_date(dates):
    #data_stt = recup_data_stt() # Assurez-vous que cette fonction retourne les données attendues
    #print(f'recup_data_stt{data_stt}', type(data_stt))
 
    #dates = data_stt['Dates']
    #print(f'recup_data_date_stt{dates}', type(dates))
    
    
    if not dates:  # Vérifie si la liste est vide ou None
        return "Veuillez indiquer une date plus prècise"
    
    processed_dates = []

    for date in dates:
        word = date.lower()  # Normalisation pour la comparaison
        # Ajouter directement les dates spécifiques trouvées par le NER
        if word in ["demain", "après-demain"]:
            processed_dates.append(word)
    

    # Vérification avec search_date_world
    dates_trouvees = search_date_world(dates)
    print("Dates trouvées après search_date_world:", dates_trouvees, type(dates_trouvees))
    # Cas où une seule date est trouvée

    if len(dates_trouvees) == 1:
        date = dates_trouvees
        #date = ''.join(dates_trouvees)
        #print(date)
        date_result = convert_dates(date)
        for key in ['date_debut', 'date_fin']:
            put_data_to_file_json(file_path='enregistrement.json', key_json=key, value=date_result)
           # print(f"resultat cas 1 de recup_date : {date_result}")
        return {"Date_ref" : date_result } 
    
    # Cas où plusieurs dates sont trouvées
    elif len(dates_trouvees) > 1:
        #Utilisation de la compréhension de liste pour simplifier
        #print(f"voir les dates {dates_trouvees}", type(dates_trouvees))
        dates_modify = convert_dates(dates_trouvees) 
        
        
        sorted_dates_datetime = sorted(dates_modify)
        

        debut_date, fin_date = sorted_dates_datetime[0], sorted_dates_datetime[-1] # Assumption: les deux premières dates sont les dates de début et de fin
        
        put_data_to_file_json(file_path='enregistrement.json', key_json='date_debut', value=debut_date)
        put_data_to_file_json(file_path='enregistrement.json', key_json='date_fin', value=fin_date)
        #print(f"resultat cas 2 de recup_date : {debut_date} {fin_date}")
        return {'Date_debut' :debut_date, 'Date_fin': fin_date}
    elif dates_trouvees == None:
        return 'veuillez être plus précis dans la date'
    # Cas où aucune date n'est trouvée
    else:
        return("Aucune date n'a été enregistrée")

