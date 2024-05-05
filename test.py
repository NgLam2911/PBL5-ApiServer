import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt

# Assuming `data` is a 2D list with the data from the AMG8833 sensor
raw_data = """
30.25, 30.25, 30.25, 29.75, 29.75, 30.00, 29.50, 29.75, 
30.50, 30.50, 30.50, 30.00, 30.00, 29.75, 30.00, 30.00, 
30.75, 31.75, 30.75, 30.25, 30.50, 30.00, 29.75, 30.00, 
32.50, 37.00, 31.00, 30.75, 30.75, 30.50, 30.50, 29.75, 
30.75, 30.75, 30.50, 31.25, 31.50, 31.50, 30.25, 30.50, 
29.75, 30.00, 30.75, 30.50, 31.25, 31.75, 31.00, 29.75, 
29.50, 29.75, 29.75, 30.75, 30.75, 31.00, 31.00, 30.50, 
29.25, 29.50, 29.50, 29.50, 30.25, 30.25, 29.75, 30.00
"""

rows = raw_data.strip().split('\n')
data = [[float(val.strip()) for val in row.split(',') if val.strip()] for row in rows]

# Convert the data to a NumPy array
data = np.array(data)

# Create a grid of the same size as the data
x = np.linspace(0, 1, data.shape[1])
y = np.linspace(0, 1, data.shape[0])

# Create a function that can interpolate the data
f = RectBivariateSpline(y, x, data)

# Create a grid of the size we want
xnew = np.linspace(0, 1, 800)
ynew = np.linspace(0, 1, 600)

# Interpolate the data
data_interp = f(ynew, xnew)

# Create a figure with 2 subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Display the original data in the first subplot
axs[0].imshow(data, cmap='hot')
axs[0].set_title('Original 8x8 Data')

# Display the interpolated data in the second subplot
axs[1].imshow(data_interp, cmap='hot')
axs[1].set_title('Interpolated 800x600 Data')

# Show the figure
plt.show()
