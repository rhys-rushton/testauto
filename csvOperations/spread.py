import pandas as pd
from datetime import datetime

#import data, specifying the fields we need
fields = ['encounter_date', 'encounter_time', 'encounter_id', 'first_name', 'last_name', 'date_of_birth', 'age_at_presentation', 'gender', 'medicare_number', 'indigenous_status', 'address_line1', 'suburb', 'state', 'postcode', 'emergency_contact_name', 'country_of_birth','home_language', 'patient_symptoms', 'usual_medications', 'specimen_collected', 'diagnosis', 'outcome']
data = pd.read_csv(r'C:\Users\RRushton\Desktop\testauto\csvOperations\data.csv', header=0, encoding = 'cp1252', usecols= fields)
data_small = data.head()
data_done = {}

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
            data_done[new_key_value] = transposed_data[key]
            #print(data_done[new_key_value])
            new_key_value += 1
   



make_dic(data, start_date)
#print(data_done)





