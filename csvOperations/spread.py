import pandas as pd
from datetime import datetime

fields = ['encounter_date', 'encounter_time', 'encounter_id', 'first_name', 'last_name', 'date_of_birth', 'age_at_presentation', 'gender', 'medicare_number', 'indigenous_status', 'address_line1', 'suburb', 'state', 'postcode', 'emergency_contact_name', 'country_of_birth','home_language', 'patient_symptoms', 'usual_medications', 'specimen_collected', 'diagnosis', 'outcome']
data = pd.read_csv('./data.csv', header=0, encoding = 'cp1252', usecols= fields)
data_small = data.head()
data_done = {}

format = "%d/%m/%Y"
start_date = input("Please enter the date from which you would like results. Please enter as dd-month-year")
res = True
#start_date = "04/08/2021"

try:
    res = bool(datetime.strptime(start_date, format))
    print("Date Successfully Entered")

except ValueError:
    res = False
    print("Please enter a correct date format")

#new = data[["encounter_date"] == start_date,["encounter_id"]]

#print(((data.head()).transpose()).to_dict())
## we want to specify a date range. 
##we only want dates that are greater than the last range that we did. 
##record last range done. 
##filter through given dataframe
##add rows that are in specified date range to a different dataframe. 

def make_dic(inputData, dateCompare):
    transposed_data = (inputData.transpose()).to_dict()
    #print(transposed_data)
    new_key_value = 0

    for key in transposed_data: 
        if transposed_data[key]['encounter_date'] == dateCompare:
            
           
            data_done[new_key_value] = transposed_data[key]
            print(data_done[new_key_value])
            new_key_value += 1


#create a dictionary that uses the encounter number as key and date as value 
##then iterate over all values in dictionary. 
#all values that are in date range append encounter number to a list. 
#then use this list as a way to filter through the large dataframe. 

make_dic(data, start_date)
#print(data_done)









#dfRC = pd.read_csv('./REDRC.csv', header=0)
#dfDPS = pd.read_csv('./DSPatients.csv', header =0, encoding = 'cp1252')
#finalData = pd.DataFrame(columns=["FILE_NUMBER","GIVEN_NAME","FAMILY_NAME","HOME_ADDRESS_LINE_1","HOME_ADDRESS_LINE_2","HOME_SUBURB_TOWN","HOME_POSTCODE","DOB","GENDER","TITLE"])


#final =pd.DataFrame()

#dfRCTest = dfRC.head()
#dfDPSTest = dfDPS.head()

#A function to compare file numbers that are both in the rc and the dps information
#def compareRcDPS (rcNum, dpsNum, rcFull, DPSFull):
    #finalDataFileNumbs = []
   # rcClinic = rcNum.tolist()
   # dpsInfo = dpsNum.tolist()

    #for n in rcClinic: 
        #if n in dpsInfo:
            #print("Match")
         #   finalDataFileNumbs.append(n)
      #  else: 
            #print("No")
        #    continue
    
   # fd = pd.DataFrame(finalDataFileNumbs, columns=["FILE_NUMBER"])

    #this is the data we are going to upload
    #we are checking that the list of file numbers in the final data column
    #is inside the rc clinic data. 
   # upload = rcFull[rcFull["FILE_NUMBER"].isin(finalDataFileNumbs)] 
   # supload = DPSFull[DPSFull["FILE_NUMBER"].isin(finalDataFileNumbs)]
   # print(upload)
    #print(supload)
    

    
  
 
        
#compareRcDPS (dfRC["FILE_NUMBER"], dfDPS["FILE_NUMBER"],dfRC, dfDPS[['FILE_NUMBER' , 'GENDER', 'DATE_OF_BIRTH']])

#now we need a function to write the file numbers to the pandas final data data frame. 

##want to create a data frame with the final data file numbers as an index

    


#for ind, row in dfRC.iterrows(): 
    #for dpsInd, dpsRow in dfDPS.iterrows():
        #if (row[1] == dpsRow[33]):
            #fileNumber = row[1]
            #print(ind,row)
            #finalData.loc[ind,"FILE_NUMBER"] = row["FILE_NUMBER"]
            #finalData.loc[ind,"GIVEN_NAME"] = row["GIVEN_NAME"]
            #finalData.loc[ind,"FAMILY_NAME"] = row["FAMILY_NAME"]
            #finalData.loc[ind,"HOME_ADDRESS_LINE_1"] = row["HOME_ADDRESS_LINE_1"]
            #finalData.loc[ind,"HOME_ADDRESS_LINE_2"] = row["HOME_ADDRESS_LINE_2"]
            #finalData.loc[ind,"HOME_SUBURB_TOWN"] = row["HOME_SUBURB_TOWN"]
            #finalData.loc[ind,"HOME_POSTCODE"] = row["HOME_POSTCODE"]
            #finalData.loc[ind, "DOB"] = dpsRow["DATE_OF_BIRTH"]
            #finalData.loc[ind,"GENDER"] = dpsRow["GENDER"]
            #finalData.loc[ind,"TITLE"] = row["TITLE"]
        #else:
            #unMatched.loc[ind, "FILE_NUMBER"] = row["FILE_NUMBER"]
           
            #pass 
            
            
#print(finalDataFileNumbs)

            


#print(finalData.head())
#finalData.to_csv('finalData.csv')
#print(unMatched)