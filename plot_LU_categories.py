import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(15, 5))
# Read the wrfout file using xarray
data_no_urb = xr.open_dataset('/Users/lmatak/Downloads/chem_outputs_test_contor/no_urb_march/wrfout_d01_2019-03-01_05')
data_urb=xr.open_dataset('/Users/lmatak/Downloads/chem_outputs_test_contor/BEM_march/wrfout_d01_2019-03-01_05')

# Extract the land use variable (assuming it's named 'LU_INDEX')
land_use_no_urb = data_no_urb['LU_INDEX']
land_use_BEM = data_urb['LU_INDEX']

# Plot the land use categories
land_use_slice_no_urb = land_use_no_urb.isel(Time=0)
land_use_slice_BEM = land_use_BEM.isel(Time=0)
# Create a mask where LU_INDEX is not equal to 13
mask_no_urb = np.where(land_use_slice_no_urb == 13, np.nan, land_use_slice_no_urb)
mask_BEM = np.where(land_use_slice_BEM != 13, np.nan, land_use_slice_BEM)
# Plot the land use categories
plt.subplot(1, 3, 1)
plt.imshow(mask_no_urb, cmap='viridis')
plt.ylim(0,100)

plt.subplot(1, 3, 2)
plt.imshow(mask_BEM, cmap='viridis')
plt.ylim(0,100)

plt.subplot(1, 3, 3)
plt.imshow(land_use_slice_BEM-land_use_slice_no_urb, cmap='viridis')
plt.ylim(0,100)
# Set plot title and labels
# plt.title('Land Use Categories (LU_INDEX = 13)')
plt.xlabel('X')
plt.ylabel('Y')

# Display the plot
plt.colorbar()
plt.show()