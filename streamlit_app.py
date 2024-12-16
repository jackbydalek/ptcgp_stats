import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit app title
st.title("Top 10 Pokémon TCG Decks by Win Percentage")

# URL of the Google Sheet (use CSV export link for simplicity)
sheet_url = "https://docs.google.com/spreadsheets/d/13L5Ftdyso3mo_8OptF3943mNqdtAU3R-WepHrAH1Qpg/export?format=csv"

# Load data
try:
    # Load data from the Google Sheet
    data = pd.read_csv(sheet_url)
    st.write("Data loaded successfully!")
    
    # Display raw data (optional)
    if st.checkbox("Show raw data"):
        st.write(data)
    
    # Sort data by "Share" and calculate top 10 + "Other"
    data = data.sort_values(by="Count", ascending=False)
    top_decks = data.head(10)
    other_share = data.iloc[10:]["Count"].sum()
    
    # Add "Other" to the top decks
    other_row = pd.DataFrame({"Deck": ["Other"], "Count": [other_share]})
    chart_data = pd.concat([top_decks, other_row], ignore_index=True)
    
    # Create a pie chart using Plotly
    fig = px.pie(
        chart_data,
        values="Count",
        names="Deck",
        title="Top 10 Decks and Other by Win Percentage",
        hole=0.3  # Makes it a donut chart; set to 0 for a full pie chart
    )
    
    # Display the Plotly pie chart in Streamlit
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"An error occurred: {e}")
