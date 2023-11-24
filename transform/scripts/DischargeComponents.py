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
    2: 'darkblue',  # darkblue = SMPrecipitation
    3: 'red',  # Blue = Icemelt
    4: 'darkred',  # lightred = IcemeltPrecipitation
    5: 'orange',  # orange = SMIM Snow and Icemelt
    6: 'purple',  # l = All together 
}

# Create a bar chart with color-coded bars
plt.figure(figsize=(12, 6))

# Get the colors for each bar based on the numeric "Category" column
bar_colors = [colors[cat] for cat in df_sorted['Category']]

bars = plt.bar(np.arange(len(df_sorted)), df_sorted['Daily max discharge per day'], color=bar_colors)


# Label the x-axis with numbers from 1 to 100
plt.xlabel('Top 100 Event Days')
plt.xticks(np.arange(len(df_sorted)), np.arange(1, 101), rotation=45, ha='right', fontsize=7)

# Label the y-axis
plt.ylabel('Max discharge value per Day m3/s')

# Set the title
plt.title('Top 100 High Discharge Days and Contributing Factors')

# Create a legend
legend_labels = {
    1: 'Snowmelt',
    2: 'Snowmelt and Precipitation',
    3: 'Icemelt',
    4: 'Icemelt and Precipitation',
    5: 'Snow and Icemelt',
    6: 'All together',
}
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[cat]) for cat in legend_labels.keys()]
plt.legend(legend_handles, legend_labels.values(), title='Factor')

# Remove extra empty space before the first bar and after the last bar
plt.xlim(-0.5, len(df_sorted) - 0.5)

# Show the plot
plt.tight_layout()
plt.show()

########### PIE Diagramm ##################
# Group the data by "Category" and calculate the percentage of each category
category_counts = df['Category'].value_counts()
total_count = len(df)
category_percentages = (category_counts / total_count) * 100

# Use the same colors dictionary for the pie chart
colors = {
    1: 'lightblue',
    2: 'darkblue',
    3: 'red',
    4: 'darkred',
    5: 'orange',
    6: 'purple',
}

# Create a pie chart
plt.figure(figsize=(10, 6))
plt.pie(category_percentages, labels=None, autopct='%1.1f%%', colors=[colors[cat] for cat in category_percentages.index], startangle=90, pctdistance=0.85)
plt.title('Factors Contributing to High Flood Events', fontsize=16, y=1.08)

# Create a legend
legend_labels = {
    1: 'Snowmelt',
    2: 'Snowmelt and Precipitation',
    3: 'Icemelt',
    4: 'Icemelt and Precipitation',
    5: 'Snow and Icemelt',
    6: 'All together',
}

plt.legend(legend_handles, legend_labels.values(), title='Factor', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)  # Adjust legend font size


# Show the plot
plt.tight_layout()
plt.show()
################## Balkendiagramm 3 ##############

# # Create a bar chart to show the relationship between "Q mm Area" and "mm Precipitation"
# fig, ax1 = plt.subplots(figsize=(12, 6))

# ## Label the x-axis with smaller and slanted numbers counting down from 100 to 1
# ax1.set_xlabel('Top 100 Event Days', fontsize=10)
# ax1.set_xticks(np.arange(len(df_sorted)))
# ax1.set_xticklabels(np.arange(1, 101), rotation=45, ha='right', fontsize=8)

# # Set the y-axis limits for both variables
# ax1.set_ylim(0, 80)

# # Label the y-axis for "Q mm Area"
# ax1.set_ylabel('Q-Area (mm)', color='darkgray', fontsize=12)
# ax1.bar(np.arange(len(df_sorted)), df_sorted['Q mm Area'], color='darkgray', label='Discharge in mm, calculated for the Area')
# ax1.tick_params(axis='y', labelcolor='black')

# # Create a second y-axis for "mm Precipitation"
# ax2 = ax1.twinx()
# ax2.set_ylim(0, 80)
# ax2.set_ylabel('P (mm)', color='darkblue', fontsize=12)
# ax2.bar(np.arange(len(df_sorted)), df_sorted['mm Precipitation'], color='darkblue', alpha=0.5, label='Precipitation in mm')
# ax2.tick_params(axis='y', labelcolor='black')

# # Set the title
# plt.title('Area Discharge and Precipitation in High Discharge Events')

# # Create a legend
# lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# lines = lines1 + lines2
# labels = labels1 + labels2
# plt.legend(lines, labels, loc='upper right')

# # # Remove extra empty space before the first bar and after the last bar
# plt.xlim(-0.5, len(df_sorted) - 0.5)

# # Show the plot
# plt.tight_layout()
# plt.show()

# Define a color map for the "Category" column
colors = {
    1: 'lightblue',  # blue = Snowmelt
    2: 'darkblue',  # Green = SMPrecipitation
    3: 'red',  # Blue = Icemelt
    4: 'darkred',  # Yellow = IcemeltPrecipitation
    5: 'orange',  # Cyan = SMIM Snow and Icemelt
    6: 'purple',  # Magenta = All together 
     'gray': 'gray',  # Gray for Precipitation
}

# Create a bar chart to show the relationship between "Q mm Area" and "mm Precipitation"
fig, ax1 = plt.subplots(figsize=(12, 6))

# Label the x-axis with smaller and slanted numbers counting down from 100 to 1
ax1.set_xlabel('Top 100 Event Days', fontsize=10)
ax1.set_xticks(np.arange(len(df_sorted)))
ax1.set_xticklabels(np.arange(1, 101), rotation=45, ha='right', fontsize=7)

# Set the y-axis limits for "Q mm Area"
ax1.set_ylim(0, 80)

# Label the y-axis for "Q mm Area"
ax1.set_ylabel('Q-Area (mm)', color='black', fontsize=12)

# Create a bar chart for "Q mm Area" with Category colors
category_colors = [colors[cat] for cat in df_sorted['Category']]
ax1.bar(np.arange(len(df_sorted)), df_sorted['Q mm Area'], color=category_colors, label='Q mm Area')

# Create a second y-axis for "mm Precipitation"
ax2 = ax1.twinx()
ax2.set_ylim(0, 80)
ax2.set_ylabel('P (mm)', color='gray', fontsize=12)
ax2.bar(np.arange(len(df_sorted)), df_sorted['mm Precipitation'], color='gray', alpha=0.5, label='P mm Precipitation')
ax2.tick_params(axis='y', labelcolor='gray')

# Set the title
plt.title('Area Discharge and Precipitation in High Discharge Events')

# Create a legend
legend_labels = {
    1: 'Snowmelt',
    2: 'Snowmelt and Precipitation',
    3: 'Icemelt',
    4: 'Icemelt and Precipitation',
    5: 'Snow and Icemelt',
    6: 'All together',
    'gray': 'Precipitation',  # Include 'gray' for Precipitation
}

legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[cat]) for cat in legend_labels.keys()]
plt.legend(legend_handles, legend_labels.values(), title='Legend')


# Remove extra empty space before the first bar and after the last bar
plt.xlim(-0.5, len(df_sorted) - 0.5)

# Show the plot
plt.tight_layout()
plt.show()