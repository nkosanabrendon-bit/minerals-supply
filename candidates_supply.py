import re
import pandas as pd

PRED = "predictions.csv"
SUPPLY = "element_supply.csv"

pred = pd.read_csv(PRED)
sup = pd.read_csv(SUPPLY).set_index("element")
tracked = set(sup.index)


def elements(formula):
    return sorted(set(re.findall(r"[A-Z][a-z]?", formula)))


rows = []
for _, r in pred.iterrows():
    els = elements(r["formula"])
    t = [e for e in els if e in tracked]
    other = [e for e in els if e not in tracked]
    if t:
        worst = max(t, key=lambda e: sup.loc[e, "top_share_pct"])
        worst_share = sup.loc[worst, "top_share_pct"]
        worst_country = sup.loc[worst, "top_country"]
    else:
        worst, worst_share, worst_country = "", 0.0, ""
    rows.append({
        "formula": r["formula"],
        "voltage_mp": r["voltage_mp"],
        "voltage_pred": r["voltage_pred"],
        "capacity_mAh_g": r["capacity_mAh_g"],
        "energy_Wh_kg": r["energy_Wh_kg"],
        "split": r["split"],
        "tracked_elements": " ".join(t),
        "not_tracked": " ".join(other),
        "riskiest_element": worst,
        "its_top_country": worst_country,
        "its_top_share_pct": worst_share,
        "has_south_africa_metal": any(sup.loc[e, "south_africa_pct"] >= 10 for e in t),
        "has_zimbabwe_metal": any(sup.loc[e, "zimbabwe_pct"] >= 5 for e in t),
    })

out = pd.DataFrame(rows)
out.to_csv("candidates_supply.csv", index=False)
pd.set_option("display.width", 220)

top = out.sort_values("energy_Wh_kg", ascending=False).head(25)
print("Top 25 by Materials Project energy:")
print(top[["formula", "voltage_mp", "energy_Wh_kg", "tracked_elements",
           "riskiest_element", "its_top_country", "its_top_share_pct"]].to_string(index=False))

print()
print("How often each tracked element appears in these top 25:")
counts = pd.Series(" ".join(top["tracked_elements"]).split()).value_counts()
print(counts.to_string())
print()
print("Top-25 materials with a South Africa metal:", int(top["has_south_africa_metal"].sum()))
print("Top-25 materials with a Zimbabwe metal:", int(top["has_zimbabwe_metal"].sum()))
print("Saved candidates_supply.csv")
