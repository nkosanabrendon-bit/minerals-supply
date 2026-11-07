import numpy as np
import pandas as pd

df = pd.read_csv("MCS2026_Commodities_Data.csv", encoding="latin-1")
w = df[df["Section"].str.contains("World", na=False)
       & (df["Statistics"] == "Production") & (df["Year"] == "2025")].copy()


def num(v):
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        return np.nan


w["val"] = w["Value"].map(num)

spec = {
    "Mn": ("MANGANESE", "Mine production"),
    "V": ("VANADIUM", "Mine production"),
    "Cr": ("CHROMIUM", "Mine production"),
    "Co": ("COBALT", "Mine production"),
    "Ni": ("NICKEL", "Mine production"),
    "Li": ("LITHIUM", "Mine production"),
    "Cu": ("COPPER", "Mine production"),
    "Mo": ("MOLYBDENUM", "Mine production"),
    "Nb": ("NIOBIUM (COLUMBIUM)", "Mine production"),
    "Fe": ("IRON ORE", "Mine production: Iron content"),
    "Ti": ("TITANIUM MINERAL CONCENTRATES", "Mine production: Ilmenite"),
    "W": ("TUNGSTEN", "Mine production"),
    "Zn": ("ZINC", "Mine production"),
    "Sn": ("TIN", "Mine production"),
}

rows = []
for el, (chapter, detail) in spec.items():
    x = w[(w["MCS chapter"] == chapter) & (w["Statistics_detail"] == detail)]
    c = x[(x["Country"] != "World total") & x["val"].notna()]
    c = c[~c["Country"].str.contains("ther", na=False)]
    t = x[x["Country"] == "World total"]["val"]
    total = float(t.iloc[0]) if len(t) and not np.isnan(t.iloc[0]) else c["val"].sum()
    top = c.sort_values("val", ascending=False).iloc[0]

    def share(country):
        v = c[c["Country"] == country]["val"]
        return round(100 * float(v.iloc[0]) / total, 1) if len(v) else 0.0

    s = c["val"] / c["val"].sum()
    rows.append({
        "element": el, "usgs_chapter": chapter, "unit": x["Unit"].iloc[0],
        "world_total": total, "top_country": top["Country"],
        "top_share_pct": round(100 * top["val"] / total, 1),
        "south_africa_pct": share("South Africa"), "zimbabwe_pct": share("Zimbabwe"),
        "num_producers": len(c), "concentration_hhi": round(float((s ** 2).sum()) * 10000),
    })

out = pd.DataFrame(rows).sort_values("top_share_pct", ascending=False)
out.to_csv("element_supply.csv", index=False)
pd.set_option("display.width", 200)
print(out.drop(columns=["usgs_chapter", "unit"]).to_string(index=False))
print("Saved element_supply.csv")
