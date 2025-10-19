# Checks the average power + toughness / converted mana cost for English creature cards that are legal in commander.
# Formula: (P + T) / cmc

import json
import matplotlib.pyplot as plt

# Load Data
file = 'default-cards-full-10-14.json'

try:
    with open(file, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: file not found. Please ensure the file exists.")
except json.JSONDecodeError:
    print("Error: Could not decode JSON from file. Check file format.")

# Clean Data
cards = [

]


# name, lang, released_at, cmc, power, toughness, colors, type_line (creature, legendary creature, land, sorcery...), reprint

# Filters:
#   - English Cards
#   - Legal in Commander
#   - No Dual-Sided Cards (i.e. The Restoration of Eiganjo // Architect of Restoration)
#   - Creature / Legendary Creature
#   - No Reprints

# Data:
#   - Year
#   - Power + Toughness
#   - Converted Mana Cost

uniq = set()
i = 0

for card in data:
    # Filters
    if card["lang"] != "en":
        continue
    if card.get("legalities", {}).get("commander", "") != "legal":
        continue
    if "//" in card["name"]:
        continue
    if "Creature" not in card["type_line"]:
        continue
    if card["reprint"] == True:
        continue

    uniq.add(card["name"])
    i = i + 1


    date = card["released_at"]
    year = int(date[:4])

    pt = card["power"] + card["toughness"]
    cmc = card["cmc"]
    
    #cards.append({card["name"], year})

print(len(uniq))
print(i)

# 45,865 filtered cards
# 15,916 unique filtered cards (set)
# 20,642 filtered non-reprints ???