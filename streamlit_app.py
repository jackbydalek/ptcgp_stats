import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app
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
    
    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(
        top_decks["Win %"],
        labels=top_decks["Deck Name"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)
except Exception as e:
    st.error(f"An error occurred: {e}")
