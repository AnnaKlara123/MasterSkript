import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge/top_100_days_D_Area_precipExcle2.csv'

# Use ';' as the delimiter since your CSV file uses semicolons as separators
df = pd.read_csv(file_path, delimiter=';')

# Sort the DataFrame by "Daily max discharge per day" in descending order
df_sorted = df.sort_values(by='Daily max discharge per day', ascending=False)

# Check the column names in your DataFrame
print(df_sorted.columns)

# Define a color map for the "Category" column
colors = {
    1: 'lightblue',  # blue = Snowmelt
    2: 'darkblue',  # Green = SMPrecipitation
    3: 'red',  # Blue = Icemelt
    4: 'darkred',  # Yellow = IcemeltPrecipitation
    5: 'orange',  # Cyan = SMIM Snow and Icemelt
    6: 'grey',  # Magenta = All together 
}

# Create a bar chart with color-coded bars
plt.figure(figsize=(12, 6))

# Get the colors for each bar based on the numeric "Category" column
bar_colors = [colors[cat] for cat in df_sorted['Category']]

bars = plt.bar(np.arange(len(df_sorted)), df_sorted['Daily max discharge per day'], color=bar_colors)

# Label the x-axis
plt.xlabel('100 top event days')
plt.xticks(np.arange(len(df_sorted)), df_sorted.index)

# Label the y-axis
plt.ylabel('Max discharge value per Day m3/s')

# Set the title
plt.title('Sorted daily max discharge per Day in categories')

# Create a legend
legend_labels = {
    1: 'Snowmelt',
    2: 'SMPrecipitation',
    3: 'Icemelt',
    4: 'IcemeltPrecipitation',
    5: 'Snow and Icemelt',
    6: 'All together',
}
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[cat]) for cat in legend_labels.keys()]
plt.legend(legend_handles, legend_labels.values(), title='Factor')

# Show the plot
plt.tight_layout()
plt.show()

############ PIE Diagramm ##################
# Group the data by "Category" and calculate the percentage of each category

category_counts = df['Category'].value_counts()
total_count = len(df)
category_percentages = (category_counts / total_count) * 100

# Define colors for the pie chart
colors = ['lightblue', 'darkblue', 'red', 'darkred', 'orange', 'grey']

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(category_percentages, labels=None, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title('Factors Contributing to High Flood Events')

# Create a legend
legend_labels = {
    1: 'Snowmelt',
    2: 'SMPrecipitation',
    3: 'Icemelt',
    4: 'IcemeltPrecipitation',
    5: 'Snow and Icemelt',
    6: 'All together',
}

legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[cat - 1]) for cat in legend_labels.keys()]
plt.legend(legend_handles, legend_labels.values(), title='Factor', loc='center left', bbox_to_anchor=(1, 0.5))
# Show the plot
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.show()