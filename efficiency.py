# Checks the average power + toughness / converted mana cost for
#   English creature cards that are legal in commander.
# Formula: (P + T) / cmc
# Excludes cards with zero cmc to avoid div by zero errors.

import json
import matplotlib.pyplot as plt
from collections import defaultdict


# Load Data
file = 'default-cards-full-10-14.json'

try:
    with open(file, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: file not found. Please ensure the file exists.")
except json.JSONDecodeError:
    print("Error: Could not decode JSON from file. Check file format.")

# Data Structures
uniq = set()
year_to_efficiency = defaultdict(list)
year_to_zero_cmc = defaultdict(list)


# Filters:
#   - English Cards
#   - Legal in Commander
#   - No Dual-Sided Cards (i.e. The Restoration of Eiganjo // Architect of Restoration)
#   - Creature / Legendary Creature
#   - No Reprints
#   - Excludes cards with non-decimal power/toughness
#   - Excludes (and tracks) cards with zero cmc

# Data:
#   - Year
#   - Power + Toughness
#   - Converted Mana Cost
for card in data:
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
    if card["name"] in uniq:
        continue
    if not card["power"].isdecimal() or not card["toughness"].isdecimal():
        continue


    # Extract name, year, power + toughness, cmc
    name = card["name"]
    year = int(card["released_at"][:4])
    pt = int(card["power"]) + int(card["toughness"])
    cmc = card["cmc"]

    # Add card name to unique set (to avoid alt art copies)
    uniq.add(name)

    # Card not parsable because zero cmc
    if cmc == 0:
        year_to_zero_cmc[year].append(name)
        continue

    # Add to dictionary
    year_to_efficiency[year].append(pt / cmc)

# Compute averages
year_to_avg = {
    year: sum(e_list) / len(e_list)
    for year, e_list in year_to_efficiency.items()
    if e_list  # avoid divide-by-zero
}


# Print or inspect average card efficiency by year
print("Average card efficiency by year:")
for y in sorted(year_to_avg.keys()):
    print(f"{y}: {year_to_avg[y]:.2f}")

# Print or inspect number of cards with zero cmc by year
print("Number of cards with zero cmc by year:")
for y in sorted(year_to_zero_cmc.keys()):
    print(f"{y}: {len(year_to_zero_cmc[y])}")

# Plot
plt.figure(figsize=(10,5))
plt.plot(sorted(year_to_avg.keys()), [year_to_avg[y] for y in sorted(year_to_avg.keys())], marker='*')
plt.title("Average Efficiency per Card by Year (Commander Legal, No Dual-Side, Creatures Only, Non-Reprint, EN)")
plt.xlabel("Year")
plt.ylabel("Average Efficiency")
plt.grid(True)
plt.show()

# 45,865 filtered cards
# 20,642 filtered non-reprints (includes alt-arts)
# 15,916 unique filtered cards (no alt-arts)
# 15,711 unique filtered cards (set) without */+ power/toughness
    # 205 cards with * or + (negligible)
# 15,690 unique filtered cards (set) without */+ power/toughness or zero cmc <-- this one
    # 21  cards with 0 cmc (negligible)

# Challenges:
    # How to define power/toughness */+ (Lhurgoyf)
    # How to handle cards with zero converted mana cost (Ornithopter)
