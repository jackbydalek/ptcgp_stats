import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Center the Streamlit app title
st.markdown(
    "<h1 style='text-align: center;'>Pokemon TCG Deck Data</h1>",
    unsafe_allow_html=True,
)

# URL of the Google Sheet (use CSV export link for simplicity)
sheet_url = "https://docs.google.com/spreadsheets/d/13L5Ftdyso3mo_8OptF3943mNqdtAU3R-WepHrAH1Qpg/export?format=csv"

# Load data
try:
    # Load data from the Google Sheet
    data = pd.read_csv(sheet_url)
    # st.write("Data loaded successfully!")
    
    # Display raw data (optional)
    if st.checkbox("Show raw data"):
        st.write(data)
    
    # Sort data by "Count" and calculate top 10 + "Other"
    data = data.sort_values(by="Count", ascending=False)
    top_decks = data.head(10)
    other_share = data.iloc[10:]["Count"].sum()
    
    # Add "Other" to the top decks
    other_row = pd.DataFrame({"Deck": ["Other"], "Count": [other_share]})
    chart_data = pd.concat([top_decks, other_row], ignore_index=True)

    # Move "Other" to the last row
    chart_data = pd.concat(
        [chart_data[chart_data["Deck"] != "Other"], other_row],
        ignore_index=True
    )
    
    # Assign colors to slices
    colors = []
    for deck in chart_data["Deck"]:
        if "Mewtwo" in deck:
            colors.append("purple")
        elif "Pikachu" in deck:
            colors.append("yellow")
        elif "Charizard" in deck:
            colors.append("orange")
        elif "Articuno" in deck:
            colors.append("#1e90ff")
        elif "Weezing" in deck:
            colors.append("black")
        elif "Ninetales" in deck:
            colors.append("#FFDBBB")
        elif "Other" in deck:
            colors.append("lightgrey")
        else:
            # Generate random color
            colors.append("#%06x" % random.randint(0, 0xFFFFFF))
    
    # Create a pie chart using Plotly
    fig = px.pie(
        chart_data,
        values="Count",
        names="Deck",
        title="Top 10 Decks by Win Percentage",
        hole=0.3  # Makes it a donut chart; set to 0 for a full pie chart
    )
    
    # Apply custom colors
    fig.update_traces(marker=dict(colors=colors))

    # Center legend
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,  # Adjust this value to fine-tune vertical position
            xanchor="center",
            x=0.5
        )
    )
    
    # Display the Plotly pie chart in Streamlit
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"An error occurred: {e}")
