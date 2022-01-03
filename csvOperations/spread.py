import pandas as pd
from datetime import datetime

#import data, specifying the fields we need
#from rhino we want the daily report
fields = ['encounter_date', 'encounter_time', 'encounter_id', 'first_name', 'last_name', 'date_of_birth', 'age_at_presentation', 'gender', 'medicare_number', 'indigenous_status', 'address_line1', 'suburb', 'state', 'postcode', 'emergency_contact_name', 'country_of_birth','home_language', 'patient_symptoms', 'usual_medications', 'specimen_collected', 'diagnosis', 'outcome']
data = pd.read_csv(r'H:\testauto\csvOperations\rhinodata\rhinoapp.csv', header=0, usecols= fields)
#data.set_index("medicare_number", inplace=True)
data_small = data.head()
print(data_small)
#this is all patients in the rhino data who are in the correct date range
data_done_date = {}
#currently we want to only upload patients who are new patients so this dictionary contains new patients which 
#we get by cross checking with itemcode bcse they are already registered if they are in both
data_to_return = {}

#specifying the data format
format = "%d/%m/%Y"
start_date = input("Please enter the date from which you would like results. Please enter as dd-month-year")
res = True
#start_date = "04/08/2021"

#checing that the user has inputed a date that we can actualy use
try:
    res = bool(datetime.strptime(start_date, format))
    print("Date Successfully Entered")

except ValueError:
    res = False
    print("Please enter a correct date format")


#now we want to read the item number data from zedmed. 
#item_number_data = pd.read_csv(r'H:\testauto\csvOperations\dspdata\item_number.csv')



## we want to specify a date range. 
##we only want dates that are greater than the last range that we did. 
##record last range done. 
##filter through given dataframe
##add rows that are in specified date range to a different dataframe. 
#create a dictionary that uses the encounter number as key and date as value 
##then iterate over all values in dictionary. 
#all values that are in date range append encounter number to a list. 
#then use this list as a way to filter through the large dataframe.

#this functions transposes the data so we can uses
#indexes as keys for the dictionary we then make
#then we take all the patients who are in the date range we want. 
#create a new dictinary from this. 
#we use and integer that we change to add the new keys to the new dictionary
#For the dataframe we are turning it into a dictionary so that we can iterate through it quicker

def make_dic(inputData, dateCompare):
    transposed_data = (inputData.transpose()).to_dict()
    
    new_key_value = 0

    for key in transposed_data: 
        if transposed_data[key]['encounter_date'] >= dateCompare:
            data_done_date[new_key_value] = transposed_data[key]
            #print(data_done[new_key_value])
            new_key_value += 1
   



make_dic(data, start_date)
#print(data_done_date)




#refer to link below perform join on the dataframes to remove duplicates and get only patients in itemcode csv. 
#then do another join to get those in both

#https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe