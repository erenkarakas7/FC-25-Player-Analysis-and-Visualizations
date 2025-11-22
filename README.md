# ⚽ FIFA 25 Player Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)
![Plotly](https://img.shields.io/badge/Plotly-Express-yellowgreen)

## 📘 Project Description
This project is an interactive exploratory data visualization dashboard. The dashboard analyzes FIFA 25 player attributes, providing insights into player stats, team distributions, and skill comparisons across different leagues and nations.

The application allows users to filter data dynamically and explore relationships between physical attributes and technical skills using advanced visualization techniques.

## 📊 Dataset Details
* **Source:** [FIFA 25 Player Dataset (sourced from Kaggle/FC 25 Database)](https://www.kaggle.com/datasets/nyagami/ea-sports-fc-25-database-ratings-and-stats).
* **Content:** The dataset includes over 15,000+ players with attributes such as Overall Rating (OVR), Pace, Shooting, Dribbling, Physicality, Height, Weight, etc.
* **Preprocessing:**
    * Cleaned unnecessary columns (`Unnamed: 0`, `url`).
    * Handled missing values for Goalkeeper stats and text data.
    * Converted `Height` (cm/ft) and `Weight` (kg/lbs) columns into numerical integers for analysis.

## 🚀 Features & Visualizations
The dashboard includes interactive visualizations designed to uncover specific insights:

### 1. Player Density & Quality (Sunburst Chart)
* **Insight:** visualizes the distribution of players based on their preferred foot and position, colored by their average Overall Rating (OVR).
* **Interactivity:** Click to expand segments, hover for details.

### 2. Player Comparison (Radar Chart)
* **Insight:** A multi-variable comparison tool allowing users to compare up to 3 players side-by-side on metrics: PAC, SHO, PAS, DRI, DEF, PHY.
* **Interactivity:** Multi-select dropdown for player selection.

### 3. Ball Control by Position (Box Plot)
* **Insight:** Analyzing the distribution of 'Ball Control' skills across positions, sorted by median skill level to identify the most technical positions.
* **Interactivity:** Hover for outlier player details.

### 4. Global Skill Distribution (Choropleth Map)
* **Insight:** A geographical representation of average player quality (OVR) by nation.

### 5. Top Leagues & Teams Hierarchy (Treemap)
* **Insight:** Hierarchical view of the top 500 players grouped by League and Team, sized by their Overall Rating.

### 6. Pace vs. Dribbling Analysis (Scatter Plot)
* **Insight:** Correlation analysis between a player's speed (Pace) and technical ability (Dribbling), sized by OVR.

## 🛠️ Installation & Setup

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/fifa25-analysis.git](https://github.com/your-username/fifa25-analysis.git)
    cd fifa25-analysis
    ```

2.  **Install required libraries:**
    It is recommended to create a virtual environment.
    ```bash
    pip install pandas streamlit plotly
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

4.  **Access the Dashboard:**
    Open your browser and navigate to `http://localhost:8501`.

## 👥 Team Contributions
*Per the assignment requirements, individual contributions are listed below:*

| Team Member | Responsibilities & Contributions |
| :--- | :--- |
| **[Eren Karakaş]** | **Data Preprocessing:** Cleaning null values and unit conversion.<br>**Visualizations:** Sunburst Chart (Foot/Position), Radar Chart (Comparison), Box Plot (Ball Control).<br>**Dashboard Layout:** 
| **[Muhammed Gözlek]** | **Visualizations:** Choropleth Map (Nation OVR), Treemap (Leagues/Teams), Scatter Plot (Pace vs Dribbling) Sidebar implementation. |.<br>**Documentation:** Report preparation and code structuring. |
| **[Rabia Kurt]** | ---


## 📂 File Structure
* `app.py`: Main Streamlit application file containing visualization logic.
* `male_players.csv`: The dataset file (ensure this is in the root directory).
* `README.md`: Project documentation.

---
