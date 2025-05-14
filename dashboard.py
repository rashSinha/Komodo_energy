
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

st.set_page_config(page_title="Komodo Energy Dashboard", layout="wide")
st.title("⚡ Komodo Energy Dashboard")

# Load cleaned usage data
df = pd.read_csv("household_usage_cleaned.csv")
df["datetime"] = pd.to_datetime(df["datetime"])
df["hour"] = df["datetime"].dt.hour

# Load agile pricing data
with open("agile_price_example.json") as f:
    price_json = json.load(f)
price_df = pd.json_normalize(price_json["results"])
price_df["datetime"] = pd.to_datetime(price_df["valid_from"]).dt.tz_localize(None)

# Update price_df to match the format of dataframe
price_df["price_per_kwh"] = price_df["value_inc_vat"] / 100
price_df = price_df[["datetime", "price_per_kwh"]].sort_values("datetime")
df = df.sort_values("datetime")

# Merge pricing
df = pd.merge_asof(df, price_df, on="datetime", direction="backward")
df["cost_agile"] = df["usage_kwh"] * df["price_per_kwh"]
df["cost_flat"] = df["usage_kwh"] * 0.20

# Sidebar filter
household_filter = st.sidebar.multiselect("Select household types", df["household_type"].unique(), default=df["household_type"].unique())
df = df[df["household_type"].isin(household_filter)]

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Hourly Usage", "💰 Cost Comparison", "⚡ Flexibility Scoring"])

with tab1:
    st.subheader("Hourly Average Usage by Household Type")
    hourly_avg = df.groupby(["hour", "household_type"])["usage_kwh"].mean().reset_index()
    fig1 = plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_avg, x="hour", y="usage_kwh", hue="household_type", marker="o")
    plt.grid(True)
    plt.ylabel("Average kWh")
    st.pyplot(fig1)

with tab2:
    st.subheader("Daily Cost Comparison (Agile vs Flat Rate)")
    cost_summary = df.groupby("household_type")[["cost_agile", "cost_flat"]].sum().reset_index()
    cost_summary.set_index("household_type", inplace=True)
    st.bar_chart(cost_summary)

with tab3:
    st.subheader("Flexibility Event Scores")

    with open("flexibility_opportunity.json") as f:
        flex_json = json.load(f)
    flex_df = pd.DataFrame(flex_json["flexibility_opportunities"])

    def score_event(row, start, end, max_kwh, reward):
        hour = row["datetime"].hour
        if start <= hour <= end:
            return min(row["usage_kwh"], max_kwh) * reward
        return 0

    for i, event in flex_df.iterrows():
        start = int(event["start_time"].split(":")[0])
        end = int(event["end_time"].split(":")[0])
        max_kwh = event["max_flexibility_kWh"]
        reward = event["price_per_kWh"]
        label = f"score_{event['event_type']}"
        df[label] = df.apply(lambda r: score_event(r, start, end, max_kwh, reward), axis=1)

    score_cols = [col for col in df.columns if col.startswith("score_")]
    score_summary = df.groupby("household_type")[score_cols].sum()
    st.dataframe(score_summary)
    st.bar_chart(score_summary)
