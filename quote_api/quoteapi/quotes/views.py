from django.http import HttpResponse
from django.http import JsonResponse
import requests
import os
from dotenv import find_dotenv,load_dotenv

#Il va retrouver le fichier .env
dotenv_path = find_dotenv()
#On va charger tout les var d'enrironnements
load_dotenv(dotenv_path)

def index(request):
    return HttpResponse("Hello, world. You're at the quote index.")

def random(request):
    return HttpResponse("Bonjour Random")

def quote(request):
    KEY_USER = os.getenv("KEY_USER")
    API_INFO = (KEY_USER, "https://api.api-ninjas.com/v1/quotes")
    API_KEY, url = API_INFO
    try:
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        if response.status_code == 200:
            data = response.json()
            return JsonResponse({'quote': data[0]['quote'], 'author': data[0]['author'], 'category': data[0]['category']})
        else:
            return JsonResponse({'error': f"API error: {response.status_code}"})
    except requests.RequestException as e:
        return JsonResponse({'error':str(e)})
