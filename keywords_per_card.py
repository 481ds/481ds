# Count average keywords/card by year
# Includes: English Cards, Legal in Commander, No Reprints or Alt Arts

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


# Filters:
#   - English Cards
#   - Legal in Commander
#   - No Reprints

# Data:
#   - Year
#   - Number of Keywords

uniq = set()
year_to_keywords = defaultdict(list)

for card in data:
    # Filters
    if card["lang"] != "en":
        continue
    if card.get("legalities", {}).get("commander", "") != "legal":
        continue
    if card["reprint"] == True:
        continue
    if card["name"] in uniq:
        continue

    # Extract name, year, and keyword count
    name = card["name"]
    year = int(card["released_at"][:4])
    keyword_count = len(card.get("keywords", []))

    # Add to dictionary
    year_to_keywords[year].append(keyword_count)

    # Add card name to unique set (to avoid alt art copies)
    uniq.add(card["name"])

# Compute averages
year_to_avg = {
    year: sum(kw_list) / len(kw_list)
    for year, kw_list in year_to_keywords.items()
    if kw_list  # avoid divide-by-zero
}

# Print or inspect
print("Average keywords per card by year:")
for y in sorted(year_to_avg.keys()):
    print(f"{y}: {year_to_avg[y]:.2f}")

# Plot
plt.figure(figsize=(10,5))
plt.plot(sorted(year_to_avg.keys()), [year_to_avg[y] for y in sorted(year_to_avg.keys())], marker='*')
plt.title("Average Keywords per Card by Year (Commander Legal, Non-Reprint, EN)")
plt.xlabel("Year")
plt.ylabel("Average Keywords")
plt.grid(True)
plt.show()

# 29,672 Unique Cards
