# Battery Minerals: Where Do the Elements in Battery Candidates Come From?

Live demo: https://python3 - << 'PY'
import subprocess
url = subprocess.check_output(["pbpaste"]).decode().strip()
if not url.startswith("http"):
    url = "https://" + url
assert "streamlit.app" in url, "Copy the app link first"
t = open("README.md").read()
note = "\nLive demo: " + url + "\n"
first = t.index("\n")
t = t[:first + 1] + note + t[first + 1:]
open("README.md", "w").write(t)
print("Added link:", url)
PY
head -4 README.md
git add README.md
git commit -m "Add link to live app"

A small data project that links battery electrode materials (Materials Project data, from my battery-materials-explorer project) to where their metals are mined (USGS Mineral Commodity Summaries 2026).

Data source for mining: USGS Mineral Commodity Summaries 2026, world mine production by country, 2025 estimates. https://doi.org/10.3133/mcs2026

## What it does
1. element_supply.py reads the USGS data and, for 14 metals, finds the biggest producing country, its share of world mining, and the shares of South Africa and Zimbabwe.
2. candidates_supply.py takes my lithium battery candidates (predictions.csv) and lists the metals in each formula and the riskiest metal (the one whose mining is most concentrated in one country).
3. rank_both.py looks at the top 100 materials by energy and counts their riskiest metals.

## Findings
- South Africa mines about 48 percent of the world's chromium and about 40 percent of the world's manganese. Zimbabwe mines about 10 percent of the world's lithium (USGS estimates, 2025).
- Cobalt (Congo about 75 percent), vanadium (China about 72 percent) and nickel (Indonesia about 72 percent) are the most concentrated of the 14 metals checked.
- In the top 25 materials by energy, vanadium appears 13 times.
- In the top 100 materials by energy (one row per formula), the riskiest metal is cobalt for 30, manganese for 19, vanadium for 16, chromium for 13, iron for 10, nickel for 9 and copper for 3.

## Honest limits
- USGS shows where ore is mined, not where it is refined. Refining is often in other countries.
- Numbers are estimates. Units differ by metal (chromium is gross ore weight, manganese is metal content). Some country values are withheld.
- The supply-risk score is a simple first draft: it uses only the single most concentrated metal in the formula and ignores how much of it the material contains, recycling, prices and politics.
- Energy values are computed (DFT), not measured, and some entries look strange and are unchecked.
- Ranking uses the Materials Project energy value, not my GNN. The formula column leaves out lithium, so Zimbabwe lithium does not show up in the candidate ranking.
- Oxygen, fluorine, phosphorus and other elements without a USGS table are not tracked.
- Only 14 metals are covered.

## How to run it
Download the CSV from the USGS data release and put MCS2026_Commodities_Data.csv in this folder. Then run element_supply.py, candidates_supply.py and rank_both.py with Python and pandas.
