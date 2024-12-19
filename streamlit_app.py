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

    # Display raw data (optional)
    if st.checkbox("Show raw data"):
        st.write(data)

    # Filter by "Set" using a dropdown
    sets = data['Set'].dropna().unique()

    # Custom order for the dropdown
    ordered_sets = ["Mythical Island", "Genetic Apex"] + sorted(
        set(sets) - {"Mythical Island", "Genetic Apex"}
    )
    selected_set = st.selectbox("Select a Set", list(ordered_sets))

    # Filter the data based on selected set
    chart_data = data[data['Set'] == selected_set]

    # Color mapping dictionary
    predefined_colors = {
        "Mewtwo": "purple",
        "Pikachu": "yellow",
        "Charizard": "orange",
        "Articuno": "#1e90ff",
        "Weezing": "black",
        "Ninetales": "#FFDBBB",
        "Celebi": "#B9FF66",
        "Marowak": "#D3B683",
        "Starmie": "#ADD8E6",
        "Other": "lightgrey",
    }

    # Function to determine color based on keywords
    def assign_color(deck_name):
        for keyword, color in predefined_colors.items():
            if keyword in deck_name:
                return color
        # Assign a random color if no match is found
        return "#%06x" % random.randint(0, 0xFFFFFF)

    # Apply colors to chart data
    colors = [assign_color(deck) for deck in chart_data["Deck"]]

    # Create a pie chart using Plotly
    fig = px.pie(
        chart_data,
        values="Count",
        names="Deck",
        title=f"Top 15 Decks by Number of Entries ({'All Sets' if selected_set == 'All' else selected_set})",
        hole=0.5  # Makes it a donut chart; set to 0 for a full pie chart
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
        ),
        height=700
    )

    # Create a scatter plot with lines connecting the same Decks
    fig_scatter = px.line(
        data,
        x="Set",
        y="Win %",
        color="Deck",
        title=f"Deck Win Percentage Trends ({'All Sets' if selected_set == 'All' else selected_set})",
        line_group="Deck",
        markers=True,  # Add markers at each point
        color_discrete_map={deck: assign_color(deck) for deck in data["Deck"].unique()},
    )

    # Adjust the layout to minimize overlapping names
    fig_scatter.update_traces(
        textposition="top center",
        marker_size=10,
    )
    fig_scatter.update_layout(
        xaxis=dict(title="Set"),
        yaxis=dict(title="Win Percentage", range=[40, 55]),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,  # Adjust this value to fine-tune vertical position
            xanchor="center",
            x=0.5,
        ),
        height=800
    )

    # Display the Plotly pie chart and scatter plot in Streamlit
    st.plotly_chart(fig)
    st.plotly_chart(fig_scatter)

except Exception as e:
    st.error(f"An error occurred: {e}")
