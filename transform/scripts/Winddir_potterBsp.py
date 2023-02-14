import matplotlib.pyplot as plt
import numpy as np

# Example wind direction data
wind_directions = [100, 150, 200, 250, 300, 330, 20, 60, 90]

# Plot the wind directions in a polar plot
ax = plt.subplot(111, polar=True)
theta = np.deg2rad(wind_directions)
ax.scatter(theta, np.ones_like(theta))
ax.set_yticklabels([])
plt.show()