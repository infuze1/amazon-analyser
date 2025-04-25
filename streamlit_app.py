# amazon_keyword_optimizer_app.py
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Amazon Keyword Optimizer - Rotate & Optimize Tool")
st.write("Upload your Helium 10 keyword CSV and get automatic keyword health scoring!")

uploaded_file = st.file_uploader("Choose your Helium 10 CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Rename relevant columns
    df = df.rename(columns={
        'Keyword': 'Keyword',
        'Search Volume': 'Search Volume (Current)',
        'Organic Rank': 'Organic Rank'
    })

    # Placeholder columns
    df['Search Volume (30 Days Ago)'] = df['Search Volume (Current)']
    df['CTR (%)'] = 0.3
    df['CVR (%)'] = 10

    # Calculate Search Volume Change
    df['Search Volume Change (%)'] = ((df['Search Volume (Current)'] - df['Search Volume (30 Days Ago)']) / df['Search Volume (30 Days Ago)'] * 100).round(1)

    # Determine Status
    def determine_status(row):
        if row["Search Volume (Current)"] > 100 and row["CTR (%)"] > 0.3 and row["CVR (%)"] > 10:
            return "Good"
        elif row["Search Volume (Current)"] < 100 or row["CTR (%)"] < 0.2 or row["CVR (%)"] < 5:
            return "Replace"
        else:
            return "Watch"

    df["Status"] = df.apply(determine_status, axis=1)
    df["Action"] = df["Status"].map({
        "Good": "Keep",
        "Watch": "Monitor",
        "Replace": "Replace"
    })
    df["Notes"] = ""

    st.dataframe(df)

    # Download button
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    st.download_button(
        label="Download Optimized Tracker",
        data=output.getvalue(),
        file_name="Amazon_Keyword_Tracker.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
