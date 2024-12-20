# Air Quality Analysis Dashboard 🌍✨

An interactive dashboard and analysis project to explore air quality data across various locations. This project uses **Python** and **Streamlit** to provide visualizations and actionable insights into air quality trends, pollution hotspots, and environmental correlations.

## Live Streamlit Dashboard
https://kevinaryaswardhana-air-quality-analysis-dashboard.streamlit.app/

## Preview Dashboard
![alt text](https://github.com/kevinaryaswardhana/Air-Quality-Analysis-Project/blob/main/dashboard/Home%20Dashboard.jpg?raw=true)
![alt text](https://github.com/kevinaryaswardhana/Air-Quality-Analysis-Project/blob/main/dashboard/Exploratory%20Data%20Analysis%20Dashboard.jpg?raw=true)
![alt text](https://github.com/kevinaryaswardhana/Air-Quality-Analysis-Project/blob/main/dashboard/Visualization%20Explanatory%20Analysis%20Dashboard.jpg?raw=true)
![alt text](https://github.com/kevinaryaswardhana/Air-Quality-Analysis-Project/blob/main/dashboard/Advanced%20Analysis%20Dashboard.jpg?raw=true)

---

## **Features**
1. **Data Wrangling**: 
   - Gathering, assessing, and cleaning air quality data.
2. **Exploratory Data Analysis (EDA)**:
   - Visualizations for trends, correlations, and distributions in the data.
3. **Visualization & Explanatory Analysis**:
   - PM2.5 trends over time.
   - Days with poor air quality by location.
   - Location with the highest average PM2.5.
   - Correlation between DEWP and PM2.5.
   - Monthly and seasonal air quality trends.
4. **Advanced Analysis**:
   - **RFM Analysis**: Identifies patterns in air quality data.
   - **Geospatial Analysis**: Maps pollution hotspots using Folium.
   - **Clustering**: Manual clustering for additional insights.
5. **Interactive Dashboard**:
   - Built using Streamlit for real-time interaction and visualizations.

---

## **Getting Started**

### **Environment Setup - Anaconda**
1. Create a new environment:
   ```bash
   conda create --name air-quality python=3.9

2. Activate the environment:
   ```bash
   conda activate air-quality

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

### **Environment Setup - Shell/Terminal**
1. Create a project directory:
   ```bash
   mkdir proyek_analisis_data_air_quality_dataset
   cd proyek_analisis_data_air_quality_dataset

2. Initialize a virtual environment:
   ```bash
   pipenv install
   pipenv shell

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

### **Run the Streamlit App**
To launch the interactive dashboard, use the following command:
```
streamlit run dashboard/Dashboard.py
```
---

### **Dependencies**
The following Python libraries are required to run the project:
- pandas
- numpy
- matplotlib
- seaborn
- folium
- streamlit
- streamlit-folium
- scikit-learn

Install all dependencies using:
```
pip install -r requirements.txt
```
---

### **Key Insights**
From the Notebook:
1. **Trend Analysis**:
   - PM2.5 levels at Aotizhongxin show significant seasonal variations, with peaks in winter months due to industrial activities.
2. **Poor Air Quality**:
   - Guanyuan and Gucheng have the highest number of days exceeding PM2.5 thresholds (>150), indicating potential areas for intervention.
3. **Pollution Hotspots**:
   - Guanyuan is identified as the location with the highest average PM2.5 level (178.45 µg/m³), highlighting it as a consistent pollution hotspot.
4. **Correlation**:
   - A strong positive correlation (approximately 0.78) exists between DEWP (Dew Point) and PM2.5, suggesting that humidity contributes to increased particulate matter concentration.
5. **Seasonal Changes**:
   - Monthly air quality trends in Dongsi reveal elevated PM2.5 levels during winter, with significant improvements in summer months.

### **Conclusion**
The analysis and dashboard provide actionable insights to guide air quality management:
- Pollution Hotspots: Guanyuan requires immediate intervention due to consistently high PM2.5 levels.
- Seasonal Strategies: Focus on implementing pollution control measures during winter months when air quality is poorest.
- Correlation Awareness: Use DEWP levels as an early indicator of potential PM2.5 spikes, especially during humid periods.

---

### **About the Author**
- **Name**: Kevin Arya Swardhana
- **Email**: kevinaryastarigan@gmail.com
- **Dicoding Profile**: [kevinaryastarigan](https://www.dicoding.com/users/kevinaryastarigan)

**Feel free to reach out for any questions or feedback!**
