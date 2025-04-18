from django.http import HttpResponse
from django.http import JsonResponse
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the quote index.")

def random(request):
    return HttpResponse("Bonjour Random")

def quote(request):
    KEY_USER = "qustxpryrGJR+V5OGPjkVQ==nwDMWd6UTOfhEtKI"
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
