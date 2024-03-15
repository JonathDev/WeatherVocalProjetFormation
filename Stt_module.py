"""
export SPEECH_KEY=your-key
export SPEECH_REGION=your-region
source ~/.bashrc
"""
"""
pip install azure-cognitiveservices-speech
d25e17b49cb744948327f82459b9d2b5
"""

"""pip install python-dotenv"""
import os
import azure.cognitiveservices.speech as speechsdk
#from dotenv import load_dotenv
from dotenv import dotenv_values
#load_dotenv()

recupkey = dotenv_values('.env')
stt_key =recupkey['AZURE_KEY_STT']
stt_region=recupkey['SPEECH_REGION']

#stt_key = os.getenv("AZURE_KEY_STT")
#stt_region = os.getenv("SPEECH_REGION")
#database_url = os.getenv("DATABASE_URL")
print(stt_key)
print(stt_region)
print(type(stt_key))
print(type(stt_region))



def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    #print(f"v2 :{stt_key}")
    #print(f"v2 :{stt_region}")
    speech_config = speechsdk.SpeechConfig(subscription=stt_key, region=stt_region)
    speech_config.speech_recognition_language="fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {'statut': 200, 'message': speech_recognition_result.text}

    # Cas où aucune parole n'est reconnue
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return {'statut': 300, 'message': "Aucune parole n'a pu être reconnue : {}".format(speech_recognition_result.no_match_details)}

    # Cas où la reconnaissance est annulée
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            return {'statut': 500, 'message': "Détails de l'erreur : {}".format(cancellation_details.error_details)}
        else:
            return {'statut': 400, 'message': "Annulation due à : {}".format(cancellation_details.reason)}

