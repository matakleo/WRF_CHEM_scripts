import xarray as xr
import matplotlib.pyplot as plt
import wrf
from netCDF4 import Dataset
# Open the first wrfout file using xarray
data1 = ('/Users/lmatak/Downloads/chem_outputs_test_contor/No_Urban/wrfout_d01_2019-08-02_16')
data1=Dataset(data1)

# Open the second wrfout file using xarray
data2 = ('/Users/lmatak/Downloads/chem_outputs_test_contor/BEM/wrfout_d01_2019-08-02_16')
data2=Dataset(data2)
# Extract the land use variable (LU_INDEX) from both files
land_use1 = wrf.getvar(data1, 'LU_INDEX')
land_use2 = wrf.getvar(data2, 'LU_INDEX')

# Select a specific time or vertical level (adjust the index as needed)
land_use1_slice = land_use1
land_use2_slice = land_use2

# Calculate the difference between the land use categories
land_use_diff = land_use2_slice - land_use1_slice

# Plot the land use categories
plt.figure(figsize=(15, 5))

# Plot the land use from the first wrfout file
plt.subplot(1, 3, 1)
plt.imshow(land_use1_slice)
plt.ylim(0,140)
plt.title('Land Use Categories - File 1')

# Plot the land use from the second wrfout file
plt.subplot(1, 3, 2)
plt.imshow(land_use2_slice)
plt.ylim(0,140)
plt.title('Land Use Categories - File 2')

# Plot the difference in land use categories
plt.subplot(1, 3, 3)
plt.ylim(0,140)
plt.imshow(land_use_diff, cmap='bwr')
plt.title('Land Use Difference')

# Add colorbars to the plots
# cbar1 = plt.colorbar(orientation='horizontal', ax=plt.gca(), fraction=0.05)
# cbar2 = plt.colorbar(orientation='horizontal', ax=plt.gcf().get_axes()[1], fraction=0.05)
# cbar3 = plt.colorbar(orientation='horizontal', ax=plt.gcf().get_axes()[2], fraction=0.05)

# # Set colorbar labels
# cbar1.set_label('Land Use Categories')
# cbar2.set_label('Land Use Categories')
# cbar3.set_label('Land Use Difference')

# Adjust the layout
plt.tight_layout()

# Display the plot
plt.show()