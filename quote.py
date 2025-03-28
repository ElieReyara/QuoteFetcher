import requests

API_INFO = ("qustxpryrGJR+V5OGPjkVQ==nwDMWd6UTOfhEtKI", "https://api.api-ninjas.com/v1/quotes")
authors_seen = set() 
def get_randomQuote():
    API_KEY, url = API_INFO
    try:
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        if response.status_code == 200:
            data = response.json()
            authors_seen.add(data[0]['author'])
            return data
        else:
            print("Erreur: ", response.status_code, " Message: ", response.text)
            return None
    except requests.RequestException:
        print("Network error - check your internet!")
        return None

#Main
while  True:
    answer = input("Would you like to have an quote(Tape anything except quit that end the programm)?: ")
    if answer.lower() == 'quit':
        break
    test = get_randomQuote()
    if test is not None:
        print("Quote: ", test[0]['quote'], "\nAuthor: ", test[0]['author'], "\nCategory: ", test[0]['category'])
        print("History of authors seen: ", authors_seen)