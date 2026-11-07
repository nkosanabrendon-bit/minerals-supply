import pandas as pd

df = pd.read_csv("candidates_supply.csv")
df = df[df["tracked_elements"].notna()].copy()

N = 100
top = df.sort_values("energy_Wh_kg", ascending=False).drop_duplicates("formula").head(N)

# lower number = less concentrated mining = lower supply risk
top = top.sort_values(["its_top_share_pct", "energy_Wh_kg"], ascending=[True, False])
pd.set_option("display.width", 230)
cols = ["formula", "energy_Wh_kg", "voltage_mp", "tracked_elements",
        "riskiest_element", "its_top_country", "its_top_share_pct"]

print("Among the top", N, "by energy (one row per formula), lowest supply risk first:")
print(top[cols].head(15).to_string(index=False))
print()
print("Highest supply risk among them:")
print(top[cols].tail(8).to_string(index=False))
print()
print("Average supply-risk number by riskiest element:")
print(top.groupby("riskiest_element")["its_top_share_pct"].agg(["count", "mean"]).sort_values("count", ascending=False).to_string())
top.to_csv("ranked_candidates.csv", index=False)
print("Saved ranked_candidates.csv")
