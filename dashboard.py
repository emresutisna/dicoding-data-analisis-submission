import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def create_per_season_df(df):
    per_season_df = df.groupby(by=["yr", "season"]).agg({
        "cnt": "sum"
    }).reset_index()
    per_season_df.rename(columns={
        "yr": "year",
        "cnt": "total"
    }, inplace=True)
    return per_season_df


def create_workingday_df(df):
    workingday_df = df.groupby(by=["yr", "workingday"]).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    workingday_df.rename(columns={
        "yr": "year",
        "cnt": "total"
    }, inplace=True)
    workingday_df['workingday'] = workingday_df['workingday'].replace(
        {0: 'Weekend', 1: 'Weekday'})
    return workingday_df


def create_per_hour_df(df):
    per_hour_df = df.groupby(by=["yr", "season", "hr"]).agg({
        "cnt": "sum"
    }).reset_index()
    per_hour_df.rename(columns={
        "yr": "year",
        "hr": "hour",
        "cnt": "total"
    }, inplace=True)
    return per_hour_df


all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="yr", inplace=True)
all_df.reset_index(inplace=True)

years = all_df["yr"].unique()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/9/99/Bike_Share_Toronto_logo.png",
        width=150)

    # Mengambil start_date & end_date dari date_input
    selected_year = st.selectbox(
        'Pilih Tahun', years
    )

main_df = all_df.loc[all_df['yr'] == selected_year]

per_season_df = create_per_season_df(main_df)
workingday_df = create_workingday_df(main_df)
per_hour_df = create_per_hour_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Transaction Per Season')

col1, col2 = st.columns(2)

with col1:
    data_max = per_season_df.total.max()
    st.metric("Maximum ", value=data_max)
with col2:
    totals = per_season_df.total.sum()
    st.metric("Total transactions", value=totals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    per_season_df["season"],
    per_season_df["total"]
)
ax.set_xlabel('Season')
ax.set_ylabel('Total Transaction')

st.pyplot(fig)

st.subheader('Transaction Per Day Type')

col1, col2 = st.columns(2)

with col1:
    data_max = workingday_df.total.max()
    st.metric("Maximum ", value=data_max)
with col2:
    totals = workingday_df.total.sum()
    st.metric("Total transactions", value=totals)

fig, ax = plt.subplots()

ax.bar(workingday_df['workingday'],
       workingday_df['casual'], width=0.4, label='Casual', align='edge')
ax.bar(workingday_df['workingday'], workingday_df['registered'],
       width=-0.4, label='Registered', align='edge')

ax.set_xlabel('Day Type')
ax.set_ylabel('Total Transaction')

ax.legend()

st.pyplot(fig)

fig, ax = plt.subplots()

st.subheader('Transaction Per Hour')
for season in per_hour_df['season'].unique():
    data_season = per_hour_df.loc[per_hour_df['season'] == season]
    ax.plot(data_season["hour"], data_season["total"],
            marker='o', linewidth=2, label=season)

ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
ax.set_xticks(np.arange(0, 24))
ax.legend()
fig.set_figwidth(10)
ax.set_xlabel('Hour')
ax.set_ylabel('Total Transaction')
st.pyplot(fig)
