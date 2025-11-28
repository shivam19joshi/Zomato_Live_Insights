import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zomato Live Dashboard", layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Live.csv")
    return df

df = load_data()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("Filters")

locations = sorted(df.location.dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

top_n = st.sidebar.slider("Show Top N Restaurants by Rating", 5, 20, 7)

palette = st.sidebar.selectbox("Select Color Palette", ["winter", "viridis", "cool", "magma"])

# -------------------------------
# Filter data based on location
# -------------------------------
lo = df[df.location == selected_location]

e = (
    lo.groupby("name")[["rate", "approx_cost"]]
    .mean()
    .nlargest(top_n, "rate")
    .reset_index()
)

st.title("🍽 Zomato Live Interactive Dashboard")
st.subheader(f"📍 Showing results for **{selected_location}**")

# -------------------------------
# Plot 1 – Cost
# -------------------------------
st.write("### 💰 Top Restaurants by Average Cost (for two)")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sb.barplot(x=e.name, y=e.approx_cost, palette=palette, ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# -------------------------------
# Plot 2 – Ratings
# -------------------------------
st.write("### ⭐ Top Restaurants by Rating")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sb.barplot(x=e.name, y=e.rate, palette=palette, ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# -------------------------------
# Data Table
# -------------------------------
st.write("### 🧾 Data Table of Selected Restaurants")
st.dataframe(e)
