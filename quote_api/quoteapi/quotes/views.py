from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
from dotenv import find_dotenv,load_dotenv
from quotes.models import Quote

#Il va retrouver le fichier .env
dotenv_path = find_dotenv()
#On va charger tout les var d'enrironnements
load_dotenv(dotenv_path)

def index(request):
    return render(request, 'quotes/index.html')

def quote(request):
    KEY_USER = os.getenv("KEY_USER")
    API_INFO = (KEY_USER, "https://api.api-ninjas.com/v1/quotes")
    API_KEY, url = API_INFO
    try:
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        if response.status_code == 200:
            data = response.json()
            #On cree un objet (enregistrement) et on le sauvegarde dans la base
            quote = Quote(text=data[0]['quote'], author=data[0]['author'], category=data[0]['category'])
            quote.save()
            return JsonResponse({'quote': data[0]['quote'], 'author': data[0]['author'], 'category': data[0]['category']})
        else:
            return JsonResponse({'error': f"API error: {response.status_code}"})
    except requests.RequestException as e:
        return JsonResponse({'error':str(e)})

def savedQuotes(request):
    #objects etant le manager du model
    querySet = Quote.objects.all().values('text', 'author', 'category')
    if querySet.exists():
        authorSeen = Quote.objects.values('author').distinct()
        allQuote = list(querySet)
        authorSeen = [item['author'] for item in authorSeen]
        return JsonResponse({'quotes':allQuote, 'authors':authorSeen}, safe=False)
    else:
        return JsonResponse({'message':f"Pas encore de citation sauvegarde"})