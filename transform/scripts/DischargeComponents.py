import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'C:/Users/annak/OneDrive/Documents/Master/Masterarbeit/Meteo_Discharge/AnalyseTest_0610/Discharge/top_100_days_D_Area_precipExcle2.csv'

# Use ';' as the delimiter since your CSV file uses semicolons as separators
df = pd.read_csv(file_path, delimiter=';')

# Sort the DataFrame by "Daily max discharge per day" in descending order
df_sorted = df.sort_values(by='Daily max discharge per day', ascending=False)

# Define a color map for the "Category" column
colors = {
    1: 'r',  # Red
    2: 'g',  # Green
    3: 'b',  # Blue
    4: 'y',  # Yellow
    5: 'c',  # Cyan
    6: 'm',  # Magenta
}

# # Create a list of colors based on the "Category" column
# bar_colors = [colors.get(cat, 'k') for cat in df_sorted['Category']]

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(np.arange(len(df_sorted)), df_sorted['Daily max discharge per day'])

# Label the x-axis
plt.xlabel('Sorted Days')
plt.xticks(np.arange(len(df_sorted)), df_sorted.index)

# Label the y-axis
plt.ylabel('Daily Max Discharge per Day')

# # Add a legend for the categories
# legend_labels = {1: 'Category 1', 2: 'Category 2', 3: 'Category 3', 4: 'Category 4', 5: 'Category 5', 6: 'Category 6'}
# legend_handles = [plt.Line2D([0], [0], color=color, lw=4, label=legend_labels[cat]) for cat, color in colors.items()]
# plt.legend(handles=legend_handles, title='Categories')

# Set the title
plt.title('Daily Max Discharge per Day Sorted by Category')

# Show the plot
plt.tight_layout()
plt.show()


print("done")

# Now, you can access and work with your data using the 'df' DataFrame