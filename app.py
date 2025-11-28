import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zomato Dashboard", layout="wide")

# -------------------------------
# Load & Clean Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../DataSets/zomato.csv")
    df = df.drop(['url','address','phone','dish_liked','reviews_list',
                  'menu_item','listed_in(type)','listed_in(city)'], axis=1)

    df = df.fillna(0)
    df = df.rename(columns={'approx_cost(for two people)': 'approx_cost'})

    df.approx_cost = df.approx_cost.replace('[,]', '', regex=True).astype('int64')
    df.rate = df.rate.replace('NEW', 0)
    df.rate = df.rate.replace('-', 0)
    df.rate = df.rate.replace('[/5]', '', regex=True)
    df.rate = df.rate.replace('', 0)
    df.rate = df.rate.astype(float)

    return df

df = load_data()

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header("Filters")

locations = sorted(df.location.unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

top_n = st.sidebar.slider("Select Number of Top Restaurants", 5, 20, 7)

palette = st.sidebar.selectbox("Select Color Palette", 
                               ["viridis", "winter", "cool", "magma", "plasma"])

# -------------------------------
# Filter Data
# -------------------------------
lo = df[df.location == selected_location]

e = (
    lo.groupby("name")[["rate", "approx_cost"]]
    .mean()
    .nlargest(top_n, "rate")
    .reset_index()
)

# -------------------------------
# Dashboard Display
# -------------------------------
st.title("🍽️ Zomato Interactive Dashboard")
st.subheader(f"📍 Location: **{selected_location}**")

st.write("### 📊 Top Restaurants Based on Ratings")

col1, col2 = st.columns(2)

# -------------------------------
# Barplot - Cost
# -------------------------------
with col1:
    st.write("#### 💰 Average Cost for Two")
    fig, ax = plt.subplots(figsize=(10, 5))
    sb.barplot(x=e.name, y=e.approx_cost, palette=palette, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -------------------------------
# Barplot - Ratings
# -------------------------------
with col2:
    st.write("#### ⭐ Average Ratings")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sb.barplot(x=e.name, y=e.rate, palette=palette, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# -------------------------------
# Data Table
# -------------------------------
st.write("### 🧾 Data Table")
st.dataframe(e.style.background_gradient(cmap="winter"))
