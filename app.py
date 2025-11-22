import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Page Tab Title Settings Section
st.set_page_config(
    page_title="FIFA Player Analysis",
    page_icon="⚽",
    layout="wide"
)


# Dataset loading and preprocessing function
# @st.cache_data caches data, making the dashboard run faster
@st.cache_data
def loadAndCleanData(dataset:str="male_players.csv"):

    df = pd.read_csv(dataset,sep=",")

    # Cleaning unnecessary columns
    cols_to_drop = ['Unnamed: 0', 'Unnamed: 0.1', 'url']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # Set NaNs in goalkeeper data to 0
    gkCols = ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']
    for col in gkCols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Set NaNs in text data to 'None'
    df['Alternative positions'] = df['Alternative positions'].fillna("None")
    df['play style'] = df['play style'].fillna("None")

    # Take the data in the Height column, for example "182" from the format "182cm / 6'0" and convert it to a number
    if 'Height' in df.columns:
        df['Height'] = df['Height'].astype(str).str.split('cm').str[0].astype(int)

    # Take the data in the Weight column, for example "75" from the "75kg / 165lb" format and convert it to a number
    if 'Weight' in df.columns:
        df['Weight'] = df['Weight'].astype(str).str.split('kg').str[0].astype(int)

    return df

# Load dataset
df = loadAndCleanData()

# Creating and customizing sidebars
st.sidebar.image("ea_sports_fc_25-logo.png")

# League Selection (Multiselect)
# User can select multiple leagues
allLeagues = sorted(df['League'].unique())
selectedLeagues = st.sidebar.multiselect(
    "League:",
    options=allLeagues,
    default=allLeagues[:]  # All leagues are selected by default
)

# Nation Selection (Multiselect)
allNations = sorted(df['Nation'].unique())
selectedNations = st.sidebar.multiselect(
    "Nation:",
    options=allNations,
    default=allNations[:]  # Default Selections
)

# Age Range (Slider)
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
selectedAgeRange = st.sidebar.slider(
    "Age:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Data Filtering Section
# All charts will use this 'filtered_df' variable
filtered_df = df[
    (df['League'].isin(selectedLeagues)) &
    (df['Nation'].isin(selectedNations)) &
    (df['Age'] >= selectedAgeRange[0]) &
    (df['Age'] <= selectedAgeRange[1])
    ]

# Main Dashboard
st.title("⚽ FIFA 25 Player Analysis",width="stretch")
st.markdown("""
Graphical visualizations of the FIFA 25 game are presented using various attributes over player datasets.""")

# Summary Statistics
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Players", f"{len(filtered_df):,}")
    col2.metric("Average OVR", f"{filtered_df['OVR'].mean():.1f}")
    col3.metric("Average Age", f"{filtered_df['Age'].mean():.1f}")
    col4.metric("Total Number of Distinct Teams", filtered_df['Team'].nunique())


st.subheader("Analysis and Visualizations")

# Üye1 grraphs
uye1col1,uye1col2,uye1col3= st.columns(3)

with uye1col1:
    # Sunburst: Number of Players and Average Power
    with st.container(border=True):
        st.subheader("Player Density and Quality Based on Foot Preference")
        st.markdown("""
                A sunburst graph showing the distribution of left-handed/right-handed players by position.
                * **Slice Size:** Number of players at that position. (Larger slice = More players).
                * **Color:**: Overall (Green/Dark = More skilled group).
                """)

        if not filtered_df.empty:
            # Make a copy of the data for the chart
            dfChart = filtered_df.copy()

            # For counting we give the value 1 to each row
            dfChart['CountOfPlayers'] = 1

            figCountOvr = px.sunburst(
                dfChart,

                # Hierarchy: Foot - Position
                path=['Preferred foot', 'Position'],

                # Size: Number of Players
                values='CountOfPlayers',

                # Color: Average Power (OVR)
                # Plotly automatically calculates the weighted average using the values overall column.
                color='OVR',

                # Color Scale: 'RdYlGn' (Red -> Yellow -> Green)
                # Low ratings appear red, high ratings appear green.
                color_continuous_scale='RdYlGn',

                # Hover: Show name and team when hovering over them
                hover_data=['Name', 'Team']
            )

            figCountOvr.update_layout(margin=dict(t=40, l=10, r=10, b=10))

            st.plotly_chart(figCountOvr, width="stretch")
        else:
            st.warning("Data hasn't been found...")

with uye1col2:
    #Radar Chart: To compare at least three players
    with st.container(border=True):
        st.subheader("Player Comparison")
        st.markdown("""Radar Map : Compares two or three players based on Pace, Shot, Dribbling, 
                        Passing, Defence, and Physicality metrics.
                        """)
        defaultPlayers = ["Kylian Mbappé", "Erling Haaland"]
        availablePlayers = filtered_df["Name"].unique().tolist()
        preset = [p for p in defaultPlayers if p in availablePlayers][:2]
        players = st.multiselect(
            "Select Player (Max 3)",
            options=availablePlayers,
            default=preset,
            max_selections=3,
        )
        categories = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
        if players:
            figRadar = go.Figure()
            for player in players:
                player_stats = (
                    filtered_df.loc[filtered_df["Name"] == player, categories]
                    .mean()
                    .tolist()
                )
                figRadar.add_trace(
                    go.Scatterpolar(
                        r=player_stats,
                        theta=categories,
                        fill="toself",
                        name=player,
                        hovertemplate="%{theta}: %{r}<extra>" + player + "</extra>",
                    )
                )
            figRadar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                legend=dict(orientation="h", y=-0.2),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=20),
            )
            st.plotly_chart(figRadar, width="stretch")
        else:
            st.info("Select at least one player to compare.")

with uye1col3:
    # Graph: Position vs. Ball Control Analysis
    with st.container(border=True):
        st.subheader("Ball Control According to Positions")
        st.markdown("""
                This chart shows the distribution of **Ball Control** skills among players at each position.
                * **Sorting:** The chart automatically sorts positions from best ball control to worst (left to right).
                * **Outliers:** Dots represent players who are significantly above or below the overall standard for that position.
        """)

        if not filtered_df.empty:

            fig_ball_control = px.box(
                filtered_df,
                x="Position",
                y="Ball Control",
                color="Position",

                # SORT LOGIC:
                # Sort positions from highest to lowest based on the median 'Ball Control' value.
                # This will place the positions with the most technical players on the far left.
                category_orders={
                    "Position": filtered_df.groupby("Position")["Ball Control"].median().sort_values(
                        ascending=False).index
                },

                # Extra information to appear when hovering
                hover_data=["Name", "Team", "Age"]
            )

            # Other settings related to the chart (axis name, etc.)
            fig_ball_control.update_layout(xaxis_title="Position",yaxis_title="Ball Control Point (0-100)",
                showlegend=False)
            st.plotly_chart(fig_ball_control, use_container_width=True)
        else:
            st.warning("Data has not been found...")

# Üye2 Graphs
uye2col1, uye2col2, uye2col3 = st.columns(3)

with uye2col1:
    with st.container(border=True):

        st.subheader("Country OVR Average")
        st.markdown("""FC25 World Overall Map colored according to overall averages by country.""")
        nation_stats = (filtered_df.groupby("Nation")["OVR"].mean().reset_index())
        if not nation_stats.empty:
            fig_map = px.choropleth(
                nation_stats,
                locations="Nation",
                locationmode="country names",
                color="OVR",
                color_continuous_scale="Viridis",
            )
            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                geo=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig_map, use_container_width=True)

with uye2col2:
    with st.container(border=True):
        st.subheader("Top Leagues and Teams")
        st.markdown("""
                        A treemap that groups and shares leagues, then teams within each league based on their total overall points.
                                """)
        df_tree = filtered_df.nlargest(500, 'OVR')
        if not df_tree.empty:
            fig_tree = px.treemap(
                df_tree,
                path=[px.Constant("World"), "League", "Team", "Name"],
                values="OVR",
                color="OVR",
                color_continuous_scale="RdBu",
            )
            fig_tree.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_tree, width="stretch")

with uye2col3:
    with st.container(border=True):

        st.subheader("Pace vs Dribbling")
        st.markdown("""Scatter plot showing the relationship between pace and dribbling.""")
        # Scatter plot çok kalabalık olmasın diye limitliyoruz
        scatter_data = filtered_df.head(1000)
        fig_scatter = px.scatter(
            scatter_data,
            x="PAC",
            y="DRI",
            color="Position",
            hover_data=["Name", "OVR"],
            size="OVR",
            size_max=8
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.2),
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)


st.divider()  # Line

# Dataset Representation
st.header("Filtered Data Set")
st.write("The data set changes according to the filters made from the left menu.")
st.dataframe(filtered_df)

st.divider()
