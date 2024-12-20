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

        # Combined distributions of numerical columns
        st.write("### Distributions of Numerical Columns")
        numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns

        # Calculate the grid size for subplots
        n_cols = 3  # Number of columns
        n_rows = -(-len(numerical_columns) // n_cols)  # Ceiling division to determine rows

        plt.figure(figsize=(n_cols * 6, n_rows * 4))  # Adjust figure size dynamically
        for i, col in enumerate(numerical_columns, 1):
            plt.subplot(n_rows, n_cols, i)  # Create subplots with calculated rows and columns
            sns.histplot(data[col], kde=True, color='blue', bins=30)  # Adjust bins for clarity
            plt.title(f"Distribution of {col}", fontsize=12)  # Adjust font size
            plt.xlabel(col, fontsize=10)
            plt.ylabel("Frequency", fontsize=10)
            plt.xticks(fontsize=8)  # Adjust tick font size
            plt.yticks(fontsize=8)

        plt.tight_layout()  # Ensure everything fits without overlap
        st.pyplot(plt.gcf())
        plt.clf()

        # Correlation matrix
        st.write("### Correlation Matrix")
        plt.figure(figsize=(16, 10))
        correlation_matrix = data[numerical_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix of Numerical Variables", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

    elif selected_page == "Visualization & Explanatory Analysis":
        st.write("## Visualization & Explanatory Analysis")

        # PM2.5 Trends in Aotizhongxin
        st.write("### PM2.5 Trends in Aotizhongxin (Last 6 Months)")
        data_aotizhongxin = data[data['location'] == 'Aotizhongxin']
        last_6_months = data_aotizhongxin[data_aotizhongxin['date'] >= '2016-09-01']
        plt.figure(figsize=(16, 8))
        sns.lineplot(data=last_6_months, x='date', y='PM2.5', color='blue')
        plt.axhline(y=150, color='red', linestyle='--', label='PM2.5 Threshold (150)')
        plt.legend()
        plt.title("PM2.5 Trend in Aotizhongxin (Last 6 Months)", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

        # Poor air quality days by location
        st.write("### Days with Poor Air Quality (>150 PM2.5) by Location")
        poor_quality_days = data[data['PM2.5'] > 150].groupby('location').size().reset_index(name='Days')
        plt.figure(figsize=(16, 8))
        sns.barplot(x='Days', y='location', data=poor_quality_days, palette='Blues_r')
        plt.title("Days with Poor Air Quality by Location", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

        # Highest average PM2.5
        st.write("### Location with Highest Average PM2.5")
        avg_pm25 = data.groupby('location')['PM2.5'].mean().reset_index()
        highest_avg_pm25 = avg_pm25.sort_values(by='PM2.5', ascending=False).head(1)
        plt.figure(figsize=(16, 8))
        sns.barplot(data=highest_avg_pm25, x='location', y='PM2.5', palette='Blues_r')
        plt.title("Location with Highest Average PM2.5", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

        # Monthly Air Quality in Dongsi
        st.write("### Monthly Air Quality Trend in Dongsi")
        data_dongsi = data[data['location'] == 'Dongsi']
        data_dongsi['Month'] = data_dongsi['date'].dt.to_period('M')
        monthly_avg_pm25 = data_dongsi.groupby('Month')['PM2.5'].mean().reset_index()
        monthly_avg_pm25['Month'] = monthly_avg_pm25['Month'].dt.to_timestamp()
        plt.figure(figsize=(16, 8))
        sns.lineplot(data=monthly_avg_pm25, x='Month', y='PM2.5', color='blue')
        plt.title("Monthly Air Quality Trend in Dongsi", fontsize=18)
        st.pyplot(plt.gcf())
        plt.clf()

    elif selected_page == "Advanced Analysis":
        st.write("## Advanced Analysis")

        # RFM Analysis
        st.write("## RFM Analysis")
        rfm_data = data.groupby('location').agg(
            Recency=('date', lambda x: (data['date'].max() - x.max()).days),
            Frequency=('PM2.5', 'count'),
            Monetary=('PM2.5', 'mean')
        ).reset_index()
        scaler = MinMaxScaler()
        rfm_data[['Recency', 'Frequency', 'Monetary']] = scaler.fit_transform(rfm_data[['Recency', 'Frequency', 'Monetary']])
        rfm_data['RFM_Score'] = rfm_data[['Recency', 'Frequency', 'Monetary']].mean(axis=1)
        plt.figure(figsize=(16, 8))  # Increased figure size
        sns.barplot(data=rfm_data, x='location', y='RFM_Score', palette='Blues_r')
        st.pyplot(plt.gcf())
        plt.clf()

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
