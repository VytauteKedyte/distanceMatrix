import pandas as pd
import numpy as np

#load a file containing a list of postcodes, latitudes and longitudes - 
#the locations for which the drive time is required
postcodes = pd.read_csv('filename.csv', sep = ',', encoding = "ISO-8859-1", header = 0)
cols_to_use = ['Postcode', 'lat','lon']
postcodes = postcodes[cols_to_use]

#%% loop to create a half a matrix of distances in kilometres

#form an empty matrix
distanceMatrix = np.empty([len(postcodes), len(postcodes)])

#defining the Haversine function that takes 2 sets of coordinates and outputs km
def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians      
        lon1 = np.radians(lon1)
        lat1 = np.radians(lat1)
        lon2 = np.radians(lon2)
        lat2 = np.radians(lat2)
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a)) 
        km = 6367 * c
        return km


for location1 in range(len(postcodes)):
    for location2 in range(location1+1, len(postcodes)):
        
        orig_lat = postcodes.iloc[location1][1]
        orig_lon = postcodes.iloc[location1][2]
        
        dest_lat = postcodes.iloc[location2][1]
        dest_lon = postcodes.iloc[location2][2]
        
        distanceMatrix[location1, location2] = haversine(orig_lon, orig_lat, dest_lon, dest_lat)
        
distanceMatrixDF = pd.DataFrame(distanceMatrix) 

#copy the upper triangle into the lower
num_rows = np.size(distanceMatrix,0)
num_cols = np.size(distanceMatrix,1)
           
for i in range(num_rows):
    for j in range(i, num_cols):
        distanceMatrix[j][i] = distanceMatrix[i][j]


#add a column and a row with original postcodes
postcode = postcodes['Postcode']
distanceMatrixDF_full = pd.DataFrame(distanceMatrix, columns = postcode)

#save to csv
distanceMatrixDF_full.to_csv('distanceMatrixDF_full.csv', index = False, sep=',',header=True)
