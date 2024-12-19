import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import folium
from sklearn.preprocessing import MinMaxScaler

# Set page configuration
st.set_page_config(
    page_title="Air Quality Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the dataset
@st.cache
def load_data():
    file_path = 'submission/dashboard/main_data.csv'
    return pd.read_csv(file_path)

data = load_data()

# Sidebar: Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Dashboard", "Conclusion", "About Me"])

if menu == "Dashboard":
    # Title Dashboard
    st.title("Air Quality Analysis Dashboard")
    st.markdown("## Project Overview")
    st.markdown("""
    This dashboard provides a comprehensive analysis of air quality trends, pollution hotspots, and their correlation with environmental variables. 
    Utilize the interactive filters and visualizations to explore insights derived from PM2.5 data collected across various locations.
    """)

    # Sidebar: Filters
    st.sidebar.header("Filters")
    locations = st.sidebar.multiselect(
        "Select Locations",
        options=data['location'].unique(),
        default=data['location'].unique()
    )
    date_range = st.sidebar.slider(
        "Select Date Range",
        min_value=pd.to_datetime(data['date']).min(),
        max_value=pd.to_datetime(data['date']).max(),
        value=(pd.to_datetime(data['date']).min(), pd.to_datetime(data['date']).max())
    )

    # Filter dataset
    data['date'] = pd.to_datetime(data['date'])
    filtered_data = data[
        (data['location'].isin(locations)) &
        (data['date'] >= date_range[0]) & 
        (data['date'] <= date_range[1])
    ]

    # Metrics
    st.markdown("### Key Metrics")
    avg_pm25 = filtered_data['PM2.5'].mean()
    max_pm25 = filtered_data['PM2.5'].max()
    days_poor_quality = len(filtered_data[filtered_data['PM2.5'] > 150])

    col1, col2, col3 = st.columns(3)
    col1.metric("Average PM2.5", f"{avg_pm25:.2f}")
    col2.metric("Max PM2.5", f"{max_pm25:.2f}")
    col3.metric("Days with PM2.5 > 150", f"{days_poor_quality}")

    # Visualizations
    st.markdown("### Visualizations")

    # Line Plot
    st.subheader("PM2.5 Trends Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=filtered_data, x='date', y='PM2.5', hue='location', ax=ax)
    ax.axhline(150, color='red', linestyle='--', label='Unhealthy Threshold (150)')
    ax.set_title("PM2.5 Trends Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("PM2.5")
    ax.legend()
    st.pyplot(fig)

    # Bar Plot for Average PM2.5 by Location
    st.subheader("Average PM2.5 by Location")
    avg_pm25_location = filtered_data.groupby('location')['PM2.5'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=avg_pm25_location, x='location', y='PM2.5', palette='coolwarm', ax=ax)
    ax.axhline(150, color='red', linestyle='--', label='Unhealthy Threshold (150)')
    ax.set_title("Average PM2.5 by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Average PM2.5")
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Scatter Plot for DEWP vs. PM2.5
    st.subheader("Relationship Between Humidity (DEWP) and PM2.5")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=filtered_data, x='DEWP', y='PM2.5', alpha=0.6, color='blue', ax=ax)
    ax.set_title("Humidity vs. PM2.5")
    ax.set_xlabel("Dew Point (DEWP)")
    ax.set_ylabel("PM2.5")
    st.pyplot(fig)

    # Geospatial Analysis
    st.subheader("Geospatial Analysis")
    geo_data = filtered_data.groupby('location').agg(
        Avg_PM25=('PM2.5', 'mean'),
        Latitude=('latitude', 'mean'),
        Longitude=('longitude', 'mean')
    ).reset_index()

    m = folium.Map(location=[geo_data['Latitude'].mean(), geo_data['Longitude'].mean()], zoom_start=10)
    for _, row in geo_data.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=min(row['Avg_PM25'] / 10, 20),
            color='red' if row['Avg_PM25'] > 150 else 'green',
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(f"{row['location']}: {row['Avg_PM25']:.2f} PM2.5", parse_html=True)
        ).add_to(m)

    folium_static(m)

elif menu == "Conclusion":
    # Title Conclusion
    st.title("Conclusion")
    st.markdown("""
    ### Key Findings:
    1. **Trend Analysis**: The average PM2.5 levels at **Aotizhongxin** show significant seasonal variation, with higher values observed during winter months (December to February), potentially due to increased heating and industrial activities.
    2. **Poor Air Quality**: Locations with the highest number of days exceeding the PM2.5 threshold (>150) are **Guanyuan** and **Gucheng**, which are likely impacted by heavy traffic and industrial activities in these areas.
    3. **Pollution Hotspots**: The location with the highest average PM2.5 is **Guanyuan**, with an average level of approximately 178.45 µg/m³, indicating a consistent pollution hotspot that requires immediate intervention.
    4. **Correlation**: A strong positive correlation (approximately 0.78) exists between **DEWP (Dew Point)** and **PM2.5**, suggesting that higher humidity levels may enhance the suspension of particulate matter in the atmosphere, increasing pollution levels.
    5. **Seasonal Changes**: Monthly air quality trends in **Dongsi** reveal a pattern of elevated PM2.5 levels during the winter months, with significant drops during summer (June to August). This pattern indicates the influence of seasonal factors such as heating and weather conditions on air quality.

    ### Recommendations:
    - Prioritize pollution control measures in identified hotspots such as **Guanyuan** and **Gucheng**.
    - Monitor seasonal variations to implement targeted strategies during critical months (e.g., winter).
    - Use insights from humidity correlation to anticipate high PM2.5 levels during humid periods and take proactive measures to reduce exposure.
    """)

elif menu == "About Me":
    # About Me Section
    st.title("About Me")
    st.markdown("""
    **Name**: Kevin Arya Swardhana
    **Email**: kevinaryastarigan@gmail.com  
    **Dicoding Profile**: [kevinaryastarigan](https://www.dicoding.com/users/kevinaryastarigan)
    """)