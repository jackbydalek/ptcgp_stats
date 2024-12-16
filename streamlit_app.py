import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit app title
st.title("Top 10 Pokémon TCG Decks by Win Percentage")

# URL of the Google Sheet (use CSV export link for simplicity)
sheet_url = "https://docs.google.com/spreadsheets/d/13L5Ftdyso3mo_8OptF3943mNqdtAU3R-WepHrAH1Qpg/export?format=csv"

# Load data
try:
    data = pd.read_csv(sheet_url)
    st.write("Data loaded successfully!")
    
    # Display raw data (optional)
    if st.checkbox("Show raw data"):
        st.write(data)
    
    # Sort data by win percentage and get top 10 decks
    top_decks = data.sort_values(by="Win %", ascending=False).head(10)
    
    # Create a pie chart using Plotly
    fig = px.pie(
        top_decks,
        values="Win %",
        names="Deck Name",
        title="Top 10 Decks by Win Percentage",
        hole=0.3  # Makes it a donut chart; set to 0 for a full pie chart
    )
    
    # Display the Plotly pie chart in Streamlit
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"An error occurred: {e}")
