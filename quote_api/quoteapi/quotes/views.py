import os, json, requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
        try:
            quote = json.loads(currentQuoteJson)
        except json.JSONDecodeError:
            #A ameliorer
            print("Erreur: La chaîne JSON stockée dans la session est mal formée.")
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
        #  Vérifier si les données JSON sont présentes
        if quoteDataJson:
            try:
                quoteData = json.loads(quoteDataJson)
                try:
                    quote = Quote(text=quoteData['text'], author=quoteData['author'], category=quoteData['category'])
                    quote.save()
                    messages.success(request, "Citation sauvegardée avec succès !") # Message de succès
                    return redirect('displayQuote') # Redirige vers l'affichage de la citation (qui peut montrer la même ou une nouvelle selon ta logique)                    
                except Exception as db_error:
                    # Gérer les erreurs spécifiques à la base de données (longueur de champ, intégrité, etc.)
                    messages.error(request, f"Erreur lors de l'enregistrement de la citation : {db_error}")
                    return redirect('displayQuote')
                quote.save()
                return redirect('displayQuote')
            except json.JSONDecodeError as e:
                # Erreur si la chaîne JSON est malformée
                messages.error(request, "Erreur : Le format des données de la citation est invalide.")
                return redirect('displayQuote')
            except Exception as general_error:
                # Attrape toute autre erreur inattendue
                messages.error(request, f"Une erreur inattendue est survenue : {general_error}")
                return redirect('displayQuote')
        else:
            messages.error(request, "Erreur : La citation à sauvegarder est introuvable.")
            return redirect('displayQuote')
    else:
        messages.error(request, "Accès non autorisé à cette page.")
        return redirect('displayQuote')

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