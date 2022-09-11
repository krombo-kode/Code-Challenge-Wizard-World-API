import requests
from pprint import pprint
from requests.exceptions import HTTPError
from collections import Counter


## Top Three Elixirs
try: 
    response = requests.get('https://wizard-world-api.herokuapp.com/Wizards')
    response.raise_for_status()
    wizardList = response.json()
except HTTPError as http_err:
    print(f'Https error occured: {http_err}')
except Exception as err:
    print(f'Other error occured: {err}')


elixirInventory = {}
for wizard in wizardList:
    for elixir in wizard["elixirs"]:
        # pprint(elixir)
        if elixir["name"] not in elixirInventory:
            elixirInventory[elixir["name"]] = 1
        else:
            elixirInventory[elixir["name"]] = elixirInventory[elixir["name"]]+1

elixirCounter = Counter(dict(sorted(elixirInventory.items())))
topThreeElixirs = elixirCounter.most_common(3)

print("Top Three Elixirs:\n" + 50*"~")
for i in range(0, len(topThreeElixirs)):
    print(f'{i+1}. {topThreeElixirs[i][1]} wizards have the elixir "{topThreeElixirs[i][0]}".')
print("\n")

## Top Elixir Side Effects
try:
    response = requests.get('https://wizard-world-api.herokuapp.com/Elixirs?Name='+topThreeElixirs[0][0].replace(" ","%20"))
    response.raise_for_status()
    topElixirProfile = response.json()[0]
except HTTPError as http_err:
    print(f'Https error occured: {http_err}')
except Exception as err:
    print(f'Other error occured: {err}')
# pprint(topElixirProfile)
print(f'The top elixir has a side effect of: {topElixirProfile["sideEffects"]}\n')


## Elixirs Sharing Ingredients with Top Elixir
try:
    response = requests.get('https://wizard-world-api.herokuapp.com/Elixirs')
    response.raise_for_status()
    elixirList = response.json()
except HTTPError as http_err:
    print(f'Https error occured: {http_err}')
except Exception as err:
    print(f'Other error occured: {err}')

topElixirIngredients = [ingredient['name'] for ingredient in topElixirProfile['ingredients']]
commonIngredientElixirs = []
# Iterate through JSON response items, adding any item that has ingredients in common with the top elixir to a list if it is not already present.
for elixir in elixirList:
    for ingredient in elixir['ingredients']:
        if ingredient['name'] in topElixirIngredients and elixir['name'] not in commonIngredientElixirs:
            commonIngredientElixirs.append(elixir['name'])
commonIngredientElixirs.remove(topElixirProfile['name'])
commonIngredientElixirs.sort()

print(f'Elixirs That Share an Ingredient With "{topElixirProfile["name"]}":')
print(50*"~")
for i in range(0, len(commonIngredientElixirs)):
    print(f'{i+1}. {commonIngredientElixirs[i]}')