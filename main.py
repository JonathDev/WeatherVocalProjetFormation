from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from monitoring import trigger_recognition_event
from utilities import put_data_to_file_json, reset_file_json

#Création de l'Application
app = FastAPI()

#Récupération des fichiers du dossier static
app.mount("/static", StaticFiles(directory='static'), name='static')


#Récupération des fichiers du dossier templates
templates = Jinja2Templates(directory='templates')



@app.get("/home")
async def root(request: Request):
    names = "lapin"
    return templates.TemplateResponse("home.html", {"request": request, "name": names})






@app.post("/home")
async def enregistement(request: Request):

    #global_enregistement = ""
    data_enregistrement=trigger_recognition_event()
    enregistrement = data_enregistrement['message']
  
    
    reset_file_json()
    put_data_to_file_json(file_path = 'enregistrement.json', key_json ="enregistrement",value=enregistrement)
    
    
    #result = recup_data_meteo()
    #print(result)
    return templates.TemplateResponse("home.html", {"request":request, "enregistrement":enregistrement, "result" : "result"})

