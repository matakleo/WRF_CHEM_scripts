import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the CSV files into Pandas dataframes
df1 = pd.read_csv('/Users/lmatak/Downloads/Earl_temp_m2.csv')
df2 = pd.read_csv('/Users/lmatak/Downloads/Earl_temp_p2.csv')
df3 = pd.read_csv('/Users/lmatak/Downloads/Earl_temp_0.csv')

df4 = pd.read_csv('/Users/lmatak/Downloads/Oussama_Earl_temp_m2.csv')
df5 = pd.read_csv('/Users/lmatak/Downloads/Oussama_Earl_temp_p2.csv')
df6 = pd.read_csv('/Users/lmatak/Downloads/Oussama_Earl_temp_0.csv')

# Create a Cartopy projection object
crs = ccrs.PlateCarree()

# Create a figure and axes object
fig, ax = plt.subplots(figsize=(10, 10), )

# Add a background map
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.COASTLINE)

# # Plot the longitude and latitude coordinates
# ax.plot(df1['min_long'][1:], df1['min_lat'][1:], transform=crs, color='red', label='minus 2')
# ax.plot(df2['min_long'][1:], df2['min_lat'][1:], transform=crs, color='blue', label='plus 2')
# ax.plot(df3['min_long'][1:], df3['min_lat'][1:], transform=crs, color='green', label='zero')

# ax.scatter(df4['min_long'][1:], df1['min_lat'][1:], transform=crs, color='red', marker="o" ,label='Oussama minus 2')
# ax.plot(df5['min_long'][1:], df2['min_lat'][1:], transform=crs, color='blue', marker="o" ,label='Oussama plus 2')
# ax.plot(df6['min_long'][1:], df3['min_lat'][1:], transform=crs, color='green', marker="o" ,label='Oussama zero')

# Plot the wind intensity 
ax.plot(np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8),df1['All_Max_WND_SPD_10'][1:],  color='red', label='minus 2')
ax.plot( np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8),df2['All_Max_WND_SPD_10'][1:], color='blue', label='plus 2')
ax.plot( np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8),df3['All_Max_WND_SPD_10'][1:],  color='green', label='zero')

ax.scatter(np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8), df1['All_Max_WND_SPD_10'][1:],  color='red', marker="o" ,label='Oussama minus 2')
ax.scatter(np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8),df2['All_Max_WND_SPD_10'][1:],  color='blue', marker="o" ,label='Oussama plus 2')
ax.scatter(np.arange(0,8*len(df1['All_Max_WND_SPD_10'][1:]),8), df3['All_Max_WND_SPD_10'][1:],  color='green', marker="o" ,label='Oussama zero')
ax.set_title('Earl')
# Add a legend
ax.legend()

# Show the plot
plt.show()
