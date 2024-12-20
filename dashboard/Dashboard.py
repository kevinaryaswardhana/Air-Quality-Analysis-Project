import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import folium
from sklearn.preprocessing import MinMaxScaler

# Load and preprocess data
@st.cache_data
def load_data():
    file_path = "dashboard/main_data.csv"
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Check if the file is empty
        if data.empty:
            st.error("The dataset is empty. Please check the file.")
            return pd.DataFrame()

        # Create 'date' column if not present
        if 'date' not in data.columns:
            try:
                data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']], errors='coerce')
            except KeyError:
                st.error("Required columns for creating 'date' are missing.")
                return pd.DataFrame()
        else:
            data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Add location coordinates
        location_coordinates = {
            'Aotizhongxin': (39.998, 116.326),
            'Changping': (40.215, 116.231),
            'Dongsi': (39.929, 116.417),
            'Dingling': (40.291, 116.220),
            'Guanyuan': (39.929, 116.345),
            'Gucheng': (39.911, 116.184),
            'Huairou': (40.375, 116.631),
            'Nongzhanguan': (39.937, 116.455),
            'Shunyi': (40.126, 116.656),
            'Tiantan': (39.886, 116.407),
            'Wanliu': (39.986, 116.305),
            'Wanshouxigong': (39.878, 116.351)
        }
        coordinates_df = pd.DataFrame.from_dict(location_coordinates, orient='index', columns=['latitude', 'longitude']).reset_index()
        coordinates_df.rename(columns={'index': 'location'}, inplace=True)

        data = data.merge(coordinates_df, on='location', how='left')
        return data

    except FileNotFoundError:
        st.error("File not found: dashboard/main_data.csv. Ensure the file exists and the path is correct.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("The dataset is empty. Please check the file.")
        return pd.DataFrame()

# Main function for Streamlit app
def main():
    st.title("Air Quality Analysis Dashboard 🌍")
    st.markdown("""
    **Name**: Kevin Arya Swardhana  
    **Email**: kevinaryastarigan@gmail.com  
    **Dicoding Profile**: [kevinaryastarigan](https://www.dicoding.com/users/kevinaryastarigan)
    """)

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    pages = ["Home", "Exploratory Data Analysis", "Visualization & Explanatory Analysis", "Advanced Analysis"]
    selected_page = st.sidebar.radio("Go to", pages)

    # Load data
    data = load_data()
    if data.empty:
        st.stop()

    # Render pages
    if selected_page == "Home":
        st.write("### Welcome to the Air Quality Analysis Dashboard")
        st.write("""
        This dashboard is designed to provide comprehensive insights into air quality data
        collected from various locations. Using this dashboard, you can:
        
        - Explore distributions and correlations in air quality data.
        - Analyze trends and identify key patterns in air pollution levels.
        - Perform advanced analysis, including geospatial visualization and clustering.
        - Gain actionable insights for improving air quality and public health.

        #### Features:
        - **Exploratory Data Analysis**: Explore distributions and correlations in the dataset.
        - **Visualization & Explanatory Analysis**: Analyze specific trends and relationships in air quality data.
        - **Advanced Analysis**: Perform RFM analysis, geospatial visualization, and clustering of PM2.5 levels.

        #### Data Sources:
        The dataset used in this dashboard includes air quality measurements from various locations,
        enriched with geospatial information for advanced analysis.
        
        #### Usage:
        Navigate through the dashboard using the sidebar to explore different sections of the analysis.
        """)

    elif selected_page == "Exploratory Data Analysis":
        st.write("## Exploratory Data Analysis (EDA)")
        
        # Display Key Statistics
        st.write("### Key Statistics of Numerical Variables")
        key_stats = data.describe(include=['float64', 'int64']).transpose()
        st.dataframe(key_stats)

        # Correlation Matrix
        st.write("### Correlation Matrix")
        plt.figure(figsize=(16, 10))
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix of Numerical Variables", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

    elif selected_page == "Visualization & Explanatory Analysis":
        st.write("## Visualization & Explanatory Analysis")

        # 1. PM2.5 Trends in Aotizhongxin
        st.write("### Trend of Average PM2.5 Levels in Aotizhongxin (Last 6 Months)")
        aotizhongxin_data = data[data['location'] == 'Aotizhongxin']
        last_6_months = aotizhongxin_data[aotizhongxin_data['date'] >= (aotizhongxin_data['date'].max() - pd.DateOffset(months=6))]
        monthly_avg_pm25 = last_6_months.groupby(last_6_months['date'].dt.to_period('M'))['PM2.5'].mean().reset_index()
        monthly_avg_pm25['date'] = monthly_avg_pm25['date'].dt.to_timestamp()

        plt.figure(figsize=(16, 8))
        sns.lineplot(data=monthly_avg_pm25, x='date', y='PM2.5', color='blue', marker='o')
        plt.axhline(y=150, color='red', linestyle='--', label='PM2.5 Threshold (150)')
        plt.legend()
        plt.title("PM2.5 Trend in Aotizhongxin (Last 6 Months)", fontsize=18)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel("Average PM2.5 (µg/m³)", fontsize=14)
        st.pyplot(plt.gcf())
        plt.clf()

        # 2. Days with Poor Air Quality
        st.write("### Days with Poor Air Quality (>150 PM2.5) Per Location")
        poor_quality_days = data[data['PM2.5'] > 150].groupby('location').size().reset_index(name='Days with Poor Air Quality')
        poor_quality_days = poor_quality_days.sort_values(by='Days with Poor Air Quality', ascending=False).head(5)

        plt.figure(figsize=(16, 8))
        sns.barplot(x='Days with Poor Air Quality', y='location', data=poor_quality_days, palette='Blues_r')
        plt.title("Top 5 Locations with Poor Air Quality", fontsize=18)
        plt.xlabel("Days", fontsize=14)
        plt.ylabel("Location", fontsize=14)
        st.pyplot(plt.gcf())
        plt.clf()

        # 3. Highest Average PM2.5 Levels
        st.write("### Locations with Highest Average PM2.5 Levels")
        avg_pm25 = data.groupby('location')['PM2.5'].mean().reset_index()
        highest_avg_pm25 = avg_pm25.sort_values(by='PM2.5', ascending=False).head(5)

        plt.figure(figsize=(16, 8))
        sns.barplot(data=highest_avg_pm25, x='PM2.5', y='location', palette='Blues_r')
        plt.title("Top 5 Locations with Highest Average PM2.5 Levels", fontsize=18)
        plt.xlabel("Average PM2.5 (µg/m³)", fontsize=14)
        plt.ylabel("Location", fontsize=14)
        st.pyplot(plt.gcf())
        plt.clf()

        # 4. Monthly and Seasonal Trends in Dongsi
        st.write("### Monthly and Seasonal Trends in Dongsi")
        dongsi_data = data[data['location'] == 'Dongsi']
        dongsi_monthly_avg = dongsi_data.groupby(dongsi_data['date'].dt.to_period('M'))['PM2.5'].mean().reset_index()
        dongsi_monthly_avg['date'] = dongsi_monthly_avg['date'].dt.to_timestamp()

        plt.figure(figsize=(16, 8))
        sns.lineplot(data=dongsi_monthly_avg, x='date', y='PM2.5', marker='o', color='blue')
        plt.axhline(y=150, color='red', linestyle='--', label='PM2.5 Threshold (150)')
        plt.legend()
        plt.title("Monthly PM2.5 Trend in Dongsi", fontsize=18)
        plt.xlabel("Date", fontsize=14)
        plt.ylabel("Average PM2.5 (µg/m³)", fontsize=14)
        st.pyplot(plt.gcf())
        plt.clf()

        # Seasonal Trends
        dongsi_data['season'] = dongsi_data['date'].dt.month % 12 // 3 + 1
        dongsi_data['season'] = dongsi_data['season'].replace({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
        seasonal_avg_pm25 = dongsi_data.groupby('season')['PM2.5'].mean().reset_index()

        plt.figure(figsize=(16, 8))
        sns.barplot(data=seasonal_avg_pm25, x='season', y='PM2.5', palette='Blues_r')
        plt.title("Seasonal PM2.5 Levels in Dongsi", fontsize=18)
        plt.xlabel("Season", fontsize=14)
        plt.ylabel("Average PM2.5 (µg/m³)", fontsize=14)
        st.pyplot(plt.gcf())
        plt.clf()


    elif selected_page == "Advanced Analysis":
        st.write("## Advanced Analysis")

        # Geospatial Analysis
        st.write("## Geospatial Analysis")
        geo_data = data.groupby('location').agg(
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
                popup=f"{row['location']}: {row['Avg_PM25']:.2f}"
            ).add_to(m)
        folium_static(m)

        # Clustering
        st.write("### Clustering Analysis")
        geo_data['PM25_Cluster'] = pd.cut(geo_data['Avg_PM25'], bins=[0, 50, 100, 150, 300],
                                          labels=['Low', 'Moderate', 'High', 'Very High'])
        plt.figure(figsize=(16, 8))
        sns.barplot(data=geo_data.sort_values('Avg_PM25', ascending=False), x='location', y='Avg_PM25', hue='PM25_Cluster', palette='coolwarm')
        plt.title("PM2.5 Clusters by Location", fontsize=14)
        plt.xlabel("Location")
        plt.ylabel("Average PM2.5")
        plt.xticks(rotation=45)
        plt.legend(title="PM2.5 Cluster")
        st.pyplot(plt.gcf())

# Run the app
if __name__ == "__main__":
    main()
