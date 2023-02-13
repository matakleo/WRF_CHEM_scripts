from math import sin, cos, sqrt, atan2, radians
import numpy as np
import csv
import os





#######################################################################################
# This function calculates the distance between two geographic points using Haversine #
# formula                                                                             #
#######################################################################################

def Calculate_Distance_Haversine (Lat_1, Long_1, Lat_2, Long_2):
	# approximate radius of earth in km
	R = 6373.0
	Lat_1 = radians(Lat_1)
	Long_1 = radians(Long_1)
	Lat_2 = radians(Lat_2)
	Long_2 = radians(Long_2)

	Dlong = Long_2 - Long_1
	Dlat = Lat_2 - Lat_1

	a = sin(Dlat / 2)**2 + cos(Lat_1) * cos(Lat_2) * sin(Dlong / 2)**2
	c = 2 * np.arcsin(sqrt(a))

	distance = R * c
	return (distance)



def Calculate_Error_Intensity (V_Forecast, Real_Output, Error_List, Average_Error):

    count = len (V_Forecast)
    Error = 0
    for i in range (count):
        Error =(abs (V_Forecast [i] - Real_Output [i]) / Real_Output [i])
        Error_List.append(Error)
    count_1 = len (Error_List)
    for Error in Error_List:	
        Average_Error += Error
    Average_Error /= count_1
    list.sort (Error_List)
    return (Error_List, Average_Error)



def Calculate_Error_Track (Lat_Forecast, Lon_Forecast, Lat_Best, Lon_Best, Error_List, Average_Error):

    count = len (Lat_Forecast)
    Error = 0
    for i in range (count):
        Error = Calculate_Distance_Haversine (Lat_Forecast[i], Lon_Forecast[i], Lat_Best[i], Lon_Best[i])
        Error_List.append(Error)
    count_1 = len (Error_List)
    for Error in Error_List:
        Average_Error += Error
    Average_Error /= count_1
    list.sort (Error_List)
    return (Error_List, Average_Error)


def Calculate_Error_Track_2 (Lat_Forecast, Lon_Forecast, Lat_Best, Lon_Best, Error_List):

    count = len (Lat_Forecast)
    Error = 0
    for i in range (count):
        Error = Calculate_Distance_Haversine (Lat_Forecast[i], Lon_Forecast[i], Lat_Best[i], Lon_Best[i])
        Error_List.append(Error)
    count_1 = len (Error_List)
    for Error in Error_List:
        Average_Error += Error
    Average_Error /= count_1
    list.sort (Error_List)
    return (Error_List, Average_Error)

def Calculate_Error_Intensity_2 (wspd_List, V_Best, Error_List, Average_Error_List):
#print(wspd_List)

    Counter = len (wspd_List)
    Error = 0
    for i in range (Counter):
        
        Error_Per_TS =(abs (wspd_List [i] - V_Best[i]) / V_Best[i])
        # print('moj wind: ',wspd_List[i])
        # print('best wind: ',V_Best[i])
        Error_List.append(Error_Per_TS)
        Error += Error_Per_TS
    Error /= Counter
    Average_Error_List.append(Error)
    list.sort (Error_List)

def Calculate_Error_Track_3 (Lat_Forecast, Lon_Forecast, Lat_Best, Lon_Best, Average_Error_List):
    Average_Error_List=[]
    Counter = len (Lat_Forecast)
    Error = 0
    for i in range (Counter):
        Error_Per_TS = Calculate_Distance_Haversine (Lat_Forecast[i], Lon_Forecast[i], Lat_Best[i], Lon_Best[i])

    Error += Error_Per_TS
    Error /= Counter
    Average_Error_List.append(Error)

def calculate_distance_error (eye_lats,eye_longs,best_lats,best_longs):
    errorz=0
    # print(len(eye_lats),len(eye_longs),len(best_lats),len(best_longs))
    for i in range(len(eye_lats)):
        error=Calculate_Distance_Haversine(eye_lats[i],eye_longs[i],best_lats[i],best_longs[i])
        errorz += error/len(eye_lats)
    return errorz


def create_file (Output_Dir, File_name):

    os.chdir(Output_Dir)
    files = []
    files = list_files_8 (Output_Dir)
    test = False
    for file in files:
        if file == File_name:
            test = True
            break
    if test == False:
        os.mkdir (File_name)
    os.chdir (Output_Dir + File_name)


def calculate_intensity_error (simulated_vars,real_vars):
    error=0
    # print(len(simulated_vars),len(real_vars))
    for i in range(len(simulated_vars)):
        error += (abs(simulated_vars[i]-real_vars[i])/real_vars[i])/len(simulated_vars)
    # print('error:',error)

    return error*100


def calculate_intensity_error_slp (simulated_vars,real_vars):
    error=0
    # print(len(simulated_vars),len(real_vars))
    for i in range(len(simulated_vars)):
        error += (abs(simulated_vars[i]-real_vars[i])/real_vars[i])
    # print('error:',error)

    return error*100


#make a std dev calc func:
def variance(data):
	n=len(data)
	mean=sum(data)/n
	deviations	= 	[(x - mean) ** 2 for x in data]
	variance = sum(deviations) / n
	return variance


# This function extracts the real track data.

def Extract_Track_Data (Real_Data_Dir, List, Variable_Name,HN):
	os.chdir(Real_Data_Dir)
	with open('Real_Data_'+HN+'.csv') as f:
		reader = csv.reader(f)
	#	next (reader)
		row_header = next(reader)
		#print (row_header)
		for row in reader:
			if row[row_header.index(Variable_Name)] == '': continue
			List.append(float(row[row_header.index(Variable_Name)]) )
	return (List)

	
def Extract_by_name (Output_File, list_name, variable_name):
	
	with open(Output_File) as f:
		reader = csv.reader(f)
		if (Output_File.find('Real_Data') == -1):
			next (reader)
		row_header = next(reader)


		for row in reader:
			# print(row) 

			try:
				if (row[row_header.index(variable_name)]) == '' :
					
					continue

				if variable_name== 'Wind Speed(kt)':
					list_name.append(0.51444 * float(row[row_header.index(variable_name)]))
				
				else:
					# print(row[row_header.index(variable_name)])
					list_name.append(float(row[row_header.index(variable_name)]) )
			except: continue
	return (list_name)


def Extract_the_shit2 (Output_File, list_name, variable_name):
	with open(Output_File) as f:
		reader = csv.reader(f)
		row_header = next(reader)

		for row in reader:
			try:
				if (row[row_header.index(variable_name)]) == '' : continue
				if variable_name== 'Wind Speed(kt)':
					list_name.append(0.51444 * float(row[row_header.index(variable_name)]))
				
				else:
					list_name.append(float(row[row_header.index(variable_name)]) )
			except: continue
	return (list_name)




def Extract_Coordinates_2 (Dir, Forecast_Outputs, Lat_Header, Lon_Header):
	os.chdir(Dir)
	Lat_Forecast = []
	Lon_Forecast = []
	with open(Forecast_Outputs) as f:
		reader = csv.reader(f)
		next (reader)
		row_header = next(reader)
		#print (row_header)
		for row in reader:
			try:
				if row[row_header.index(Lat_Header)] == '': continue
				if row[row_header.index(Lon_Header)] == '': continue
				Lat_Forecast.append(float(row[row_header.index(Lat_Header)]))
				Lon_Forecast.append(float(row[row_header.index(Lon_Header)]))
			except:continue
	return (Lat_Forecast, Lon_Forecast)


from wrf import getvar




# This function returns the hurricane's eye SLP, XLAT, XLONG and WSPD using a dictionnary data.
def hurricane_eye(Data, ncfile, Time_idx):

	# Get the index of the minimum value of pressure.
	idx = np.where(Data[ncfile][Time_idx]['slp'] == np.amin(Data[ncfile][Time_idx]['slp']))
	Eye_Slp = np.amin(Data[ncfile][Time_idx]['slp'])
	Eye_Xlat = float (Data[ncfile][Time_idx]['XLAT'][idx])
	Eye_Xlong = float (Data[ncfile][Time_idx]['XLONG'][idx])
	return (Eye_Slp, Eye_Xlat, Eye_Xlong)

# This function returns the hurricane's eye SLP, XLAT, XLONG and WSPD using SLP, LAT and LONG.
def hurricane_eye_2(SLP, LAT, LONG):
	idx = np.where(np.array(SLP) == np.amin(np.array(SLP)))
	Eye_Slp = np.amin(np.array(SLP))
	Eye_Xlat = float (np.array(LAT)[idx])
	Eye_Xlong = float (np.array(LONG)[idx])
	return (Eye_Slp, Eye_Xlat, Eye_Xlong)


# This function returns the hurricane's eye SLP, XLAT, XLONG and WSPD using the original data.
def hurricane_eye_3(Data, Time_idx):

		# The Data here is the ncfile.
		SLP = np.array(getvar(Data, 'slp', Time_idx))
		Eye_Slp = np.amin(SLP) 
		Eye_Idx = np.where(SLP == np.amin(SLP))
		Eye_Xlat = float (np.array(getvar (Data, 'XLAT', Time_idx))[Eye_Idx])
		Eye_Xlong = float (np.array(getvar (Data, 'XLONG', Time_idx))[Eye_Idx])
		return (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlong)

# This function returns a list of all wrf ouput files in the directory.
def list_ncfiles(Dir, ncfiles):
	for f in os.listdir(Dir):
		if f.startswith('wrfout'):
			ncfiles.append(f)
	ncfiles.sort()
	return (ncfiles)

def list_csv_files_0(Dir,list_with_csv_targets):
	os.chdir(Dir)
	csv_files=[]
	for csv_file in list_with_csv_targets:
		for f in os.listdir(Dir):
			if (f.find(csv_file) != -1):
				csv_files.append(f)
	return(csv_files)

def list_csv_files (Dir, csv_files):
	for f in os.listdir(Dir):
		if (f == "Real_Output.csv"):
			csv_files.append(f)
		#if (f == "Dropsonde.csv"):
		#	csv_files.append(f)
		elif (f.find('Smag2D') != -1) and (f.find('cLh1p0') != -1):
			csv_files.append(f)
		elif (f.find('NoTurb') != -1) and (f.find('cLh1p0') != -1):
			csv_files.append(f)
		elif (f.find('TKE2D') != -1) and (f.find('cLh1p0') != -1):
			csv_files.append(f)
	return (csv_files)

def list_csv_files_1 (Dir, Forecast_Outputs_pfac_1p5,Forecast_Outputs_pfac_2p0, Forecast_Outputs_pfac_3p0,Real_Output):

	for f in os.listdir(Dir):
		if (f == "Real_Output.csv"):
			Real_Output = f


		elif (f.find('_pfac_1.5.') != -1):
			Forecast_Outputs_pfac_1p5 = f
		elif (f.find('_pfac_2.0.') != -1):
			Forecast_Outputs_pfac_2p0 = f
		elif (f.find('_pfac_3.0.') != -1):
			Forecast_Outputs_pfac_3p0 = f


	
	
	return (  Forecast_Outputs_pfac_1p5,Forecast_Outputs_pfac_2p0, Forecast_Outputs_pfac_3p0,
			 Real_Output)

def list_csv_files_2 (Dir, csv_files, TM):
	for f in os.listdir(Dir):
		if (f == "Real_Output.csv"):
			csv_files.append(f)
		if (f == "Dropsonde.csv"):
			csv_files.append(f)
		elif (f.find(TM) != -1):
			csv_files.append(f)
	return (csv_files)

def list_csv_files_3 (Dir, csv_files):
	for f in os.listdir(Dir):
		if f=='.DS_Store':
			pass
		else:
			csv_files.append(f)
	csv_files.sort()
	return (csv_files)

def list_hurricane_settings(Dir, Hurricane_Simulations):
	for f in os.listdir(Dir):
		if f=='.DS_Store':
			pass
		else:
			Hurricane_Simulations.append(f)
	Hurricane_Simulations.sort()
	return (Hurricane_Simulations)

def list_files_4 (Dir_2, TM, Forecast_Outputs_0p2, Forecast_Outputs_0p5, Forecast_Outputs_1p0, Forecast_Outputs_1p5, Real_Output):
	for f in os.listdir(Dir_2):
		if (f == "Real_Output.csv"):
			Real_Output = f
		elif (f.find('0p2') != -1) and (f.find(TM) != -1):
			Forecast_Outputs_0p2 = f
		elif (f.find('0p5') != -1) and (f.find(TM) != -1):
			Forecast_Outputs_0p5 = f
		elif (f.find('1p0') != -1) and (f.find(TM) != -1):
			Forecast_Outputs_1p0 = f
		elif (f.find('1p5') != -1) and (f.find(TM) != -1):
			Forecast_Outputs_1p5 = f
	return (Forecast_Outputs_0p2, Forecast_Outputs_0p5, Forecast_Outputs_1p0, Forecast_Outputs_1p5, Real_Output)

def list_files_5 (Dir, Hurricane, NDay, TM, CLH):
	Dir_1 = Dir + Hurricane + '/32km_REF_' + NDay + '/'
	Forecast_Outputs = ''
	for f in os.listdir(Dir_1):
		#print (f)
		#print (CLH)
		if (f.find(CLH)!= -1) and (f.find(TM) != -1):
			Forecast_Outputs = f
			#print (Forecast_Outputs)
	return (Forecast_Outputs, Dir_1)

def list_files_6 (Dir, Hurricane, NDay, TM, CLH):
	Dir_1 = Dir + Hurricane + '/'
	Forecast_Outputs = ''
	for f in os.listdir(Dir_1):
		#print (f)
		#print (CLH)
		if (f.find(CLH)!= -1) and (f.find(TM) != -1) and (f.find(NDay) != -1):
			Forecast_Outputs = f
			#print (Forecast_Outputs)
	return (Forecast_Outputs, Dir_1)

def list_files_7 (Dir, TM, Forecast_Outputs_0p1, Forecast_Outputs_0p2, Forecast_Outputs_0p5, Forecast_Outputs_1p0, Forecast_Outputs_1p5, Real_Output):
        for f in os.listdir(Dir):
          if (f == "Real_Output.csv"):
            Real_Output = f
          elif (f.find('0p1') != -1) and (f.find(TM) != -1):
            Forecast_Outputs_0p1 = f
          elif (f.find('0p2') != -1) and (f.find(TM) != -1):
            Forecast_Outputs_0p2 = f
          elif (f.find('0p5') != -1) and (f.find(TM) != -1):
            Forecast_Outputs_0p5 = f
          elif (f.find('1p0') != -1) and (f.find(TM) != -1):
            Forecast_Outputs_1p0 = f
          elif (f.find('1p5') != -1) and (f.find(TM) != -1):
            Forecast_Outputs_1p5 = f
        return (Forecast_Outputs_0p1, Forecast_Outputs_0p2, Forecast_Outputs_0p5, Forecast_Outputs_1p0, Forecast_Outputs_1p5, Real_Output)

# Identify all possible settings.
def list_hurricane_settings_2 (HNS, GSS, TMS, CLHS):
	Hurricane_Settings = []
	for HN in HNS:
		for GS in GSS:
			for TM in TMS:
				for CLH in CLHS:
					Hurricane_Setting = HN + '_1Nest_2days_MainGrid' + GS + '_' + TM + '_vert42_' + CLH + '_cfl2p0'
					#print (Hurricane_Setting)
					Hurricane_Settings.append(Hurricane_Setting)
	return (Hurricane_Settings)
	#print (Hurricane_Settings)

def list_files_8(Dir):
	Post_Processed_Data = []
	for f in os.listdir(Dir):
		Post_Processed_Data.append(f)
	return (Post_Processed_Data)