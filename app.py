import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zomato Live Dashboard", layout="wide")
sb.set_style("whitegrid")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Zomato_Live.csv")

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("🔍 Filters")

# Location Filter (Multiple)
locations = sorted(df.location.dropna().unique())
selected_locations = st.sidebar.multiselect("Select Location(s)", locations, default=locations[:1])

# Search Bar
search = st.sidebar.text_input("Search Restaurant Name")

# Rating Filter
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, step=0.1)

# Cost Range
min_cost, max_cost = st.sidebar.slider(
    "Cost Range (For Two)",
    int(df.approx_cost.min()),
    int(df.approx_cost.max()),
    (200, 2000)
)

# Sort by
sort_by = st.sidebar.selectbox("Sort By", ["rate", "approx_cost"])

# Number of restaurants
top_n = st.sidebar.slider("Show Top N Restaurants", 5, 30, 10)

# Color Palette
palette = st.sidebar.selectbox("Color Palette", 
                               ["winter", "viridis", "cool", "magma", "inferno"])

# Chart Type Toggle
chart_type = st.sidebar.radio("Chart Type", ["Barplot", "Lineplot", "Scatter"])

# -------------------------------
# Filter Data
# -------------------------------
filtered = df[df.location.isin(selected_locations)]
filtered = filtered[filtered.rate >= min_rating]
filtered = filtered[(filtered.approx_cost >= min_cost) & (filtered.approx_cost <= max_cost)]

if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]

# Group and sort
result = (
    filtered.groupby("name")[["rate", "approx_cost"]]
    .mean()
    .sort_values(sort_by, ascending=False)
    .head(top_n)
    .reset_index()
)

# -------------------------------
# Tabs Layout
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Visualization", "📄 Data Table", "⬇ Download"])

# -------------------------------
# Visualization
# -------------------------------
with tab1:
    st.subheader(f"Top {top_n} Restaurants (Sorted by {sort_by})")
    
    fig, ax = plt.subplots(figsize=(12, 6))

    if chart_type == "Barplot":
        sb.barplot(data=result, x="name", y=sort_by, palette=palette, ax=ax)
    elif chart_type == "Lineplot":
        sb.lineplot(data=result, x="name", y=sort_by, marker="o", ax=ax)
    elif chart_type == "Scatter":
        sb.scatterplot(data=result, x="name", y=sort_by, s=200, ax=ax)

    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Additional chart:
    st.write("### 💰 Cost vs Rating Comparison")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sb.scatterplot(data=result, x="approx_cost", y="rate", size="rate", hue="rate", palette=palette, ax=ax2)
    st.pyplot(fig2)

# -------------------------------
# Data Table
# -------------------------------
with tab2:
    st.subheader("📄 Filtered Restaurant Data")
    st.dataframe(result)

# -------------------------------
# Download Button
# -------------------------------
with tab3:
    st.subheader("Download Results")
    csv = result.to_csv(index=False)
    st.download_button("Download CSV", csv, "filtered_zomato_data.csv", "text/csv")

