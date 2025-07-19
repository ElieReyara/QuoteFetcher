from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
import os
from dotenv import find_dotenv,load_dotenv
from quotes.models import Quote

#Il va retrouver le fichier .env
dotenv_path = find_dotenv()
#On va charger tout les var d'enrironnements
load_dotenv(dotenv_path)

def generateQuote(request):
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
            request.session['json_quote_data'] = json_quote_data
            return redirect('displayQuote')
        else:
            return JsonResponse({'error': f"API error: {response.status_code}"})
    except requests.RequestException as e:
        return JsonResponse({'error':str(e)})

def displayQuote(request):
    currentQuoteJson = request.session.get('json_quote_data')
    if currentQuoteJson:
        quote = json.loads(currentQuoteJson)
    else:
        quoteDict = {
                'text': 'Today is an opportunity to create the tomorrow you want',
                'author': 'Anonymous',
                'category': 'Self-Improvement',
            }
        # Sérialise le dictionnaire en une chaîne JSON
        quote = json.dumps(quoteDict)
    context = {
        'quote':quote,
        'json_quote_data':currentQuoteJson,
    }
    return render(request, 'quotes/acceuil.html',context)

def saveQuote(request):
    if request.method == 'POST': 
        quoteDataJson = request.POST.get('json_quote_data')
        quoteData = json.loads(quoteDataJson)
        quote = Quote(text=quoteData['text'], author=quoteData['author'], category=quoteData['category'])
        quote.save()
        #redirect('quote', {'quote':quote})
        return redirect('displayQuote')
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