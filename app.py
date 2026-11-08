import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Battery Minerals: Who Mines What", page_icon="⛏️", layout="wide")

st.title("⛏️ Battery Minerals: Who Mines What?")
st.warning(
    "Student project, first draft. Mining data: USGS Mineral Commodity Summaries 2026 (2025 estimates). "
    "Battery energy values: computed (DFT) by the Materials Project, not measured in a lab. "
    "The supply-risk number is a simple score I chose and is NOT a real risk assessment."
)

supply = pd.read_csv("element_supply.csv")
cand = pd.read_csv("candidates_supply.csv")
cand = cand[cand["tracked_elements"].notna()].copy()
cand = cand.sort_values("energy_Wh_kg", ascending=False).drop_duplicates("formula")

tab1, tab2, tab3 = st.tabs(["Who mines each metal", "Battery candidates", "Limits"])

with tab1:
    st.subheader("Share of world mining held by the biggest producing country")
    chart_df = supply.sort_values("top_share_pct", ascending=False)
    bars = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("element:N", sort=list(chart_df["element"]), title="Metal"),
        y=alt.Y("top_share_pct:Q", title="Biggest producer's share of world mining (%)"),
        color=alt.Color("top_country:N", title="Biggest producer"),
        tooltip=["element", "top_country", "top_share_pct", "south_africa_pct", "zimbabwe_pct"],
    )
    st.altair_chart(bars, width="stretch")

    st.subheader("Southern Africa in the data")
    c1, c2, c3 = st.columns(3)
    mn = supply[supply["element"] == "Mn"].iloc[0]
    cr = supply[supply["element"] == "Cr"].iloc[0]
    li = supply[supply["element"] == "Li"].iloc[0]
    c1.metric("South Africa, manganese", str(mn["south_africa_pct"]) + " % of world mining")
    c2.metric("South Africa, chromium", str(cr["south_africa_pct"]) + " % of world mining")
    c3.metric("Zimbabwe, lithium", str(li["zimbabwe_pct"]) + " % of world mining")

    st.dataframe(
        supply[["element", "top_country", "top_share_pct", "south_africa_pct", "zimbabwe_pct", "num_producers", "unit"]],
        hide_index=True,
    )
    st.caption("Chromium is in gross ore weight, manganese in metal content. Mining is not refining.")

with tab2:
    st.subheader("High-energy lithium battery materials and their riskiest metal")
    n = st.slider("How many top materials by energy to look at", 10, 300, 100, step=10)
    top = cand.head(n)
    options = sorted(top["riskiest_element"].dropna().unique())
    chosen = st.multiselect("Show materials whose riskiest metal is", options, default=options)
    top = top[top["riskiest_element"].isin(chosen)]

    st.write("**" + str(len(top)) + " materials shown.** Energy is the Materials Project value (Wh/kg).")
    counts = top["riskiest_element"].value_counts().reset_index()
    counts.columns = ["riskiest_element", "materials"]
    st.altair_chart(
        alt.Chart(counts).mark_bar().encode(
            x=alt.X("riskiest_element:N", sort="-y", title="Riskiest metal in the material"),
            y=alt.Y("materials:Q", title="Number of materials"),
            tooltip=["riskiest_element", "materials"],
        ),
        width="stretch",
    )
    st.altair_chart(
        alt.Chart(top).mark_circle(size=60, opacity=0.6).encode(
            x=alt.X("its_top_share_pct:Q", title="Riskiest metal: biggest producer's share of world mining (%)"),
            y=alt.Y("energy_Wh_kg:Q", title="Energy (Wh/kg)"),
            color=alt.Color("riskiest_element:N", title="Riskiest metal"),
            tooltip=["formula", "energy_Wh_kg", "voltage_mp", "tracked_elements", "riskiest_element", "its_top_country"],
        ),
        width="stretch",
    )
    st.caption("Dots line up in columns because every material with the same riskiest metal gets the same number.")
    st.dataframe(
        top[["formula", "energy_Wh_kg", "voltage_mp", "tracked_elements", "riskiest_element", "its_top_country", "its_top_share_pct"]],
        hide_index=True,
    )

with tab3:
    st.markdown(
        """
**Honest limits**
- USGS shows where ore is **mined**, not where it is **refined**. Refining is often in other countries.
- All mining numbers are estimates. Units differ by metal, and some country values are withheld.
- The supply-risk score uses only the single most concentrated metal in a formula. It ignores how much of that metal the material contains, recycling, prices and politics.
- Battery energy values are computed (DFT), not measured. Some entries look strange and are unchecked.
- The ranking uses the Materials Project energy value, not my GNN. The formula column leaves out lithium, so Zimbabwe lithium does not appear in the candidate ranking.
- Only 14 metals are covered. Oxygen, fluorine, phosphorus and other elements without a USGS table are not tracked.

Code and data: github.com/nkosanabrendon-bit/minerals-supply
"""
    )
