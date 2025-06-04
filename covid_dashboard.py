import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🌍 COVID-19 Data Dashboard")

# Load data
df = pd.read_csv("Dataset.csv")
df.columns = df.columns.str.strip()
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df['vaccinated'] = pd.to_numeric(df['vaccinated'].replace('unknown', pd.NA), errors='coerce')
df.dropna(subset=['NEW Cases', 'NEW_DEATHS'], inplace=True)
df['CUM_CASES'] = df.groupby('country')['NEW Cases'].cumsum()
df['CUM_DEATHS'] = df.groupby('country')['NEW_DEATHS'].cumsum()

# Sidebar country selector
country_list = df['country'].dropna().unique()
selected_country = st.sidebar.selectbox("Select a Country", sorted(country_list))

# Filter country data
country_df = df[df['country'] == selected_country]

# Show line plots
st.subheader(f"📈 COVID-19 Trends for {selected_country}")

fig, ax = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
sns.lineplot(data=country_df, x='DATE', y='NEW Cases', ax=ax[0], color='blue')
ax[0].set_title("New Cases per Day")
sns.lineplot(data=country_df, x='DATE', y='NEW_DEATHS', ax=ax[1], color='red')
ax[1].set_title("New Deaths per Day")
sns.lineplot(data=country_df, x='DATE', y='vaccinated', ax=ax[2], color='green')
ax[2].set_title("Vaccinated Over Time")
st.pyplot(fig)

# Bar chart for global summary
st.subheader("🌐 Top 10 Countries by Total Cases, Deaths, and Vaccination")
agg_df = df.groupby('country').agg({
    'NEW Cases': 'sum',
    'NEW_DEATHS': 'sum',
    'vaccinated': 'max'
}).sort_values(by='NEW Cases', ascending=False).head(10)

st.bar_chart(agg_df)

# Scatter Plot
st.subheader("💉 Vaccinations vs Total Cases")
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.scatterplot(data=agg_df, x='vaccinated', y='NEW Cases', hue=agg_df.index, s=200, ax=ax2)
plt.xlabel("People Vaccinated")
plt.ylabel("Total COVID-19 Cases")
plt.title("Vaccinated vs Cases")
st.pyplot(fig2)
