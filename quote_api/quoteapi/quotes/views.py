from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
import json
import os
from dotenv import find_dotenv,load_dotenv
from quotes.models import Quote

#Il va retrouver le fichier .env
dotenv_path = find_dotenv()
#On va charger tout les var d'enrironnements
load_dotenv(dotenv_path)

def quote(request):
    KEY_USER = os.getenv("KEY_USER")
    API_INFO = (KEY_USER, "https://api.api-ninjas.com/v1/quotes")
    API_KEY, url = API_INFO
    try:
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        if response.status_code == 200:
            data = response.json()
            #Je cree un dictionnaire que je vais serealiser
            quote_data = {
                'text': data[0]['quote'],
                'author': data[0]['author'],
                'category': data[0]['category'],
            }
            # Sérialise le dictionnaire en une chaîne JSON
            json_quote_data = json.dumps(quote_data)
            #On cree un objet (enregistrement) et on le sauvegarde dans la base
            #quote = Quote(text=data[0]['quote'], author=data[0]['author'], category=data[0]['category'])
            return render(request, 'quotes/acceuil.html', {
                'quote':quote_data,
                'json_quote_data': json_quote_data
                })
        else:
            return JsonResponse({'error': f"API error: {response.status_code}"})
    except requests.RequestException as e:
        return JsonResponse({'error':str(e)})

def saveQuote(request):
    if request.method == 'POST': 
        quoteDataJson = request.POST.get('json_quote_data')
        quoteData = json.loads(quoteDataJson)
        quote = Quote(text=quoteData['text'], author=quoteData['author'], category=quoteData['category'])
        quote.save()
        #redirect('quote', {'quote':quote})
        return redirect('quote')
    else:
        return HttpResponse("Ca n'a pas marche mec")


def retrieveSavedQuote(request):
    #objects etant le manager du model
    querySet = Quote.objects.all().values('text', 'author', 'category')
    if querySet.exists():
        authorSeen = Quote.objects.values('author').distinct()
        allQuote = list(querySet)
        authorSeen = [item['author'] for item in authorSeen]
        return JsonResponse({'quotes':allQuote, 'authors':authorSeen}, safe=False)
    else:
        return JsonResponse({'message':f"Pas encore de citation sauvegarde"})