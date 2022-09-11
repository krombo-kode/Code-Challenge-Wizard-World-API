import requests
from pprint import pprint
from requests.exceptions import HTTPError
from collections import Counter

try: 
    response = requests.get('https://wizard-world-api.herokuapp.com/Wizards')
    response.raise_for_status()
    wizardList = response.json()
except HTTPError as http_err:
    print(f'Https error occured: {http_err}')
except Exception as err:
    print(f'Other error occured: {err}')


elixirList = {}
for wizard in wizardList:
    for elixir in wizard["elixirs"]:
        # pprint(elixir)
        if elixir["name"] not in elixirList:
            elixirList[elixir["name"]] = 1
        else:
            elixirList[elixir["name"]] = elixirList[elixir["name"]]+1

elixirCounter = Counter(dict(sorted(elixirList.items())))
topThreeElixirs = elixirCounter.most_common(3)

print("Top Three Elixirs:\n" + 50*"~")
for i in range(0, len(topThreeElixirs)):
    print(f'{i+1}. {topThreeElixirs[i][1]} wizards have the elixir "{topThreeElixirs[i][0]}".')
print("\n")


try:
    response = requests.get('https://wizard-world-api.herokuapp.com/Elixirs?Name='+topThreeElixirs[0][0].replace(" ","%20"))
    response.raise_for_status()
    topElixirProfile = response.json()
except HTTPError as http_err:
    print(f'Https error occured: {http_err}')
except Exception as err:
    print(f'Other error occured: {err}')
# pprint(topElixirProfile)
print(f'The top elixir has a side effect of: {topElixirProfile[0]["sideEffects"]}')

