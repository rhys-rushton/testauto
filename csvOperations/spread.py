import pandas as pd
from datetime import datetime

#merge dsp and redrc to get medicare. 
#then straight to web. 


#now we want to read the item number data from zedmed. 
item_number_data = pd.read_csv(r'H:\testauto\csvOperations\item_number\REDRC.csv', header=0, encoding='CP1252')
dsp_data = pd.read_csv(r'H:\testauto\csvOperations\dsp\DSPatients.csv', header=0, encoding='CP1252')


#contains all those who have same file number
#aim here is to get medicare number so we can compare this to rhino
dsp_and_redrc_df = pd.merge(item_number_data, dsp_data, on= 'FILE_NUMBER', how = 'inner')
#change format so that we don't have decimals for medicare
pd.set_option('display.float_format', lambda x: '%.0f' % x)

#get rid of irrelevant columns
dsp_and_redrc_df.drop(['CLINIC_CODE_x', 'TITLE_x','MAILING_ADDRESS_LINE_1_x',
       'MAILING_ADDRESS_LINE_2_x', 'MAILING_SUBURB_TOWN_x',
       'MAILING_POSTCODE_x', 'MOBILE_PHONE', 'patient_name', 'full_name',
       'full_suburb', 'address', 'full_mailing_suburb', 'TITLE_y',
       'FAMILY_NAME_y', 'GIVEN_NAME_y', 'HOME_ADDRESS_LINE_1_y',
       'HOME_ADDRESS_LINE_2_y', 'HOME_SUBURB_TOWN_y', 'HOME_POSTCODE_y',
       'HOME_PHONE_y','AGE_y', 'GENDER_y', 'USUAL_CLINIC',
       'USUAL_DOCTOR', 'TYPE_CODE', 'STATUS_CODE',
       'PRACTICE_DEFINABLE_FIELD1_CODE', 'PRACTICE_DEFINABLE_FIELD2_CODE',
       'PRACTICE_DEFINABLE_FIELD3_CODE', 'PRACTICE_DEFINABLE_FIELD4_CODE',
       'PRACTICE_DEFINABLE_FIELD5_CODE', 'PRACTICE_DEFINABLE_FIELD6',
       'PRACTICE_DEFINABLE_FIELD7', 'PRACTICE_DEFINABLE_FIELD8',
       'PRACTICE_DEFINABLE_FIELD9', 'PRACTICE_DEFINABLE_FIELD10', 'FIRST_IN',
       'LAST_IN_y', 'ALERTS', 'CLINIC_CODE_y', 'MAILING_SUBURB_TOWN_y', 'MAILING_POSTCODE_y', 'FAMILY_ID','VETERAN_AFFAIRS_NUMBER',
       'VETERAN_FILE_NUMBER_EXPIRY_DATE', 'PATIENT_HEALTH_CARE_CARD',
       'PATIENT_HLTH_CARE_CARD_EX_DATE', 'SAFETY_NET_NO'  ], axis = 1, inplace=True)

#the dsp_and_redrc_df contains all patients whether they are new or not
print(dsp_and_redrc_df)
#change to a dictionary. 
dsp_and_redrc_df = (dsp_and_redrc_df.transpose()).to_dict()






















'''
#import data, specifying the fields we need
#from rhino we want the daily report
#this is all patients in the rhino data who are in the correct date range
data_done_date = {}
#currently we want to only upload patients who are new patients so this dictionary contains new patients which 
#we get by cross checking with itemcode bcse they are already registered if they are in both
data_to_return = {}


fields = ['encounter_date', 'encounter_time', 'encounter_id', 'first_name', 'last_name', 'date_of_birth', 'age_at_presentation', 'gender', 'medicare_number', 'indigenous_status', 'address_line1', 'suburb', 'state', 'postcode', 'emergency_contact_name', 'country_of_birth','home_language', 'patient_symptoms', 'usual_medications', 'specimen_collected', 'diagnosis', 'outcome']
data = pd.read_csv(r'H:\testauto\csvOperations\rhinodata\rhinoapp.csv', header=0, usecols= fields)
#data.set_index("medicare_number", inplace=True)
data_small = data.head()
#print(data_small[['medicare_number']])

#now we want to read the item number data from zedmed. 
item_number_data = pd.read_csv(r'H:\testauto\csvOperations\item_number\REDRC.csv', header=0, encoding='CP1252')
item_number_data_small = item_number_data.head()
#print(item_number_data_small)


dsp_data = pd.read_csv(r'H:\testauto\csvOperations\dsp\DSPatients.csv', header=0, encoding='CP1252')
dsp_data_small = dsp_data.head()
#print(dsp_data_small)

#contains all those who have same file number
#aim here is to get medicare number so we can compare this to rhino
dsp_and_redrc_df = pd.merge(item_number_data, dsp_data, on= 'FILE_NUMBER', how = 'inner')
#change format so that we don't have decimals for medicare
pd.set_option('display.float_format', lambda x: '%.0f' % x)

#get rid of irrelevant columns
dsp_and_redrc_df.drop(['CLINIC_CODE_x', 'TITLE_x','MAILING_ADDRESS_LINE_1_x',
       'MAILING_ADDRESS_LINE_2_x', 'MAILING_SUBURB_TOWN_x',
       'MAILING_POSTCODE_x', 'MOBILE_PHONE', 'patient_name', 'full_name',
       'full_suburb', 'address', 'full_mailing_suburb', 'TITLE_y',
       'FAMILY_NAME_y', 'GIVEN_NAME_y', 'HOME_ADDRESS_LINE_1_y',
       'HOME_ADDRESS_LINE_2_y', 'HOME_SUBURB_TOWN_y', 'HOME_POSTCODE_y',
       'HOME_PHONE_y','AGE_y', 'GENDER_y', 'USUAL_CLINIC',
       'USUAL_DOCTOR', 'TYPE_CODE', 'STATUS_CODE',
       'PRACTICE_DEFINABLE_FIELD1_CODE', 'PRACTICE_DEFINABLE_FIELD2_CODE',
       'PRACTICE_DEFINABLE_FIELD3_CODE', 'PRACTICE_DEFINABLE_FIELD4_CODE',
       'PRACTICE_DEFINABLE_FIELD5_CODE', 'PRACTICE_DEFINABLE_FIELD6',
       'PRACTICE_DEFINABLE_FIELD7', 'PRACTICE_DEFINABLE_FIELD8',
       'PRACTICE_DEFINABLE_FIELD9', 'PRACTICE_DEFINABLE_FIELD10', 'FIRST_IN',
       'LAST_IN_y', 'ALERTS', 'CLINIC_CODE_y', 'MAILING_SUBURB_TOWN_y', 'MAILING_POSTCODE_y', 'FAMILY_ID','VETERAN_AFFAIRS_NUMBER',
       'VETERAN_FILE_NUMBER_EXPIRY_DATE', 'PATIENT_HEALTH_CARE_CARD',
       'PATIENT_HLTH_CARE_CARD_EX_DATE', 'SAFETY_NET_NO'  ], axis = 1, inplace=True)

#print(dsp_and_redrc_df)
#make everything in this dataframe lowercase so we can match with rhino
dsp_and_redrc_df.columns = dsp_and_redrc_df.columns.str.lower()
#print(dsp_and_redrc_df.columns)
dsp_and_redrc_df['medicare_number'] = dsp_and_redrc_df['medicare_number'].map(str)
#print(dsp_and_redrc_df.dtypes)
#print(data.dtypes)
#remove whitespace from rhino app data 
#data['medicare_number'] = data['medicare_number'].str.strip()
data['medicare_number'] = data['medicare_number'].map(str)
data['medicare_number'] = data['medicare_number'].apply(lambda x:x.strip())
#print(data.dtypes)
pre_existing_inrc = pd.merge(data, dsp_and_redrc_df, on='medicare_number', how = 'inner')
print(pre_existing_inrc.drop_duplicates(subset='medicare_number'))

#print(type(dsp_and_redrc_df))
#print(type(data))
df_new_patients = dsp_and_redrc_df.merge(data.drop_duplicates(), on=['medicare_number'], how='left', indicator = True)

print(df_new_patients.drop_duplicates(subset='medicare_number'))

df_new_patients_return = df_new_patients[df_new_patients['_merge'] == 'left_only']

df_new_patients_return = (df_new_patients_return.transpose()).to_dict()

#specifying the data format
#format = "%d/%m/%Y"
#start_date = input("Please enter the date from which you would like results. Please enter as dd-month-year")
#res = True
#start_date = "04/08/2021"

#checing that the user has inputed a date that we can actualy use
#try:
    #res = bool(datetime.strptime(start_date, format))
    #print("Date Successfully Entered")

#except ValueError:
    #res = False
    #print("Please enter a correct date format")






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
   



#make_dic(data, start_date)
#print(data_done_date)




#refer to link below perform join on the dataframes to remove duplicates and get only patients in itemcode csv. 
#then do another join to get those in both

#https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe

'''