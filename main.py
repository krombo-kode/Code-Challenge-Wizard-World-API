import requests
from requests.exceptions import HTTPError
from collections import Counter

### Functions
def requestFromAPI(data):
    try: 
        response = requests.get(f'https://wizard-world-api.herokuapp.com/{data}')
        response.raise_for_status()
        responseJSON = response.json()
    except HTTPError as http_err:
        print(f'Https error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')
    return responseJSON

### Routine

## Top Three Elixirs
wizardList= requestFromAPI("Wizards")

elixirInventory = {}
for wizard in wizardList:
    for elixir in wizard["elixirs"]:
        if elixir["name"] not in elixirInventory:
            elixirInventory[elixir["name"]] = 1
        else:
            elixirInventory[elixir["name"]] = elixirInventory[elixir["name"]]+1

elixirCounter = Counter(dict(sorted(elixirInventory.items())))
topThreeElixirs = elixirCounter.most_common(3)

print("Top Three Elixirs".center(60) + '\n' + 60*"~")
for i in range(0, len(topThreeElixirs)):
    print(f'{i+1}. {topThreeElixirs[i][1]} wizards have the elixir "{topThreeElixirs[i][0]}".')

## Top Elixir Side Effects
topElixirRequestString = "Elixirs?Name="+topThreeElixirs[0][0].replace(" ","%20")
topElixirProfile = requestFromAPI(topElixirRequestString)[0]
print(f'\nThe top elixir has a side effect of: {topElixirProfile["sideEffects"]}\n')


## Elixirs Sharing Ingredients with Top Elixir
elixirList = requestFromAPI("Elixirs")
topElixirIngredients = [ingredient['name'] for ingredient in topElixirProfile['ingredients']]
commonIngredientElixirs = []
# Iterate through JSON response items, adding any item that has ingredients in common with the top elixir to a list if it is not already present.
for elixir in elixirList:
    for ingredient in elixir['ingredients']:
        if ingredient['name'] in topElixirIngredients and elixir['name'] not in commonIngredientElixirs:
            commonIngredientElixirs.append(elixir['name'])
commonIngredientElixirs.remove(topElixirProfile['name'])
commonIngredientElixirs.sort()

print(f'Elixirs That Share an Ingredient With "{topElixirProfile["name"]}"'.center(60)+'\n' + 60*"~")
for i in range(0, len(commonIngredientElixirs)):
    print(f'{str(i+1)+".":<4}{commonIngredientElixirs[i]}')
print()



## Spell Types
spellList = requestFromAPI("Spells")
## Generate list of spell types
spellTypes = {}
for spell in spellList:
        if spell["type"] not in spellTypes:
            spellTypes[spell["type"]] = 1
        else:
            spellTypes[spell["type"]] = spellTypes[spell["type"]]+1
## Get count of spells with that type
spellTypeCounter = Counter(dict(sorted(spellTypes.items())))
spellTypeCounts = spellTypeCounter.most_common()

print('Spell Types and Number of Spells with that Type'.center(60) + '\n' + 60*'~')
# for i in range(0, len(spellTypeCounts)):
    # print(f'{str(i+1)+".":<4}{spellTypeCounts[i][0]:<35} x {spellTypeCounts[i][1]}')
i = 1
for spellName, spellCount in spellTypeCounts:
    print(f'{str(i)+".":<4}{spellName:<35} x {spellCount}')
    i += 1
