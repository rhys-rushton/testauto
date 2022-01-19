import pandas as pd

#we do the following here:
#read the item_number_data from 'REDRC.csv'
#read the data from 'DSPatients'
#we then merge this data together based on the patients filenumber. We do this to get their medicare number which we will need later. 
item_number_data = pd.read_csv(r'H:\testauto\csvOperations\item_number\REDRC.csv', header=0, encoding='CP1252')
dsp_data = pd.read_csv(r'H:\testauto\csvOperations\dsp\DSPatients.csv', header=0, encoding='CP1252')

#contains all those who have same file number
#aim here is to get medicare number so we can compare this to rhino
dsp_and_redrc_df = pd.merge(item_number_data, dsp_data, on= 'FILE_NUMBER', how = 'inner')
#change format so that we don't have decimals for medicare
dsp_and_redrc_df.fillna('', inplace=True)
pd.set_option('display.float_format', lambda x: '%.0f' % x)
dsp_and_redrc_df.MEDICARE_NUMBER = dsp_and_redrc_df.MEDICARE_NUMBER.astype(str)
dsp_and_redrc_df.HOME_POSTCODE_x = dsp_and_redrc_df.HOME_POSTCODE_x.astype(str)
dsp_and_redrc_df = dsp_and_redrc_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


#create a copy of the dspandredrc data to play around with for medicare matching. 
dsp_and_redrc_df_copy = dsp_and_redrc_df

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

#we want to remove this eventually but currently it is being used in the web scraping part. 
dsp_and_redrc_df = (dsp_and_redrc_df.transpose()).to_dict()


#get the rhino data and clean it all. 
#we are comparing the rhino data and dsp_and_redrc_df to check whether patients in dsp_and_red_rc are already registered in the RCapp
#compare rhino data with dsp_and_red_rc data.
#if a patient already exists in rhino => we want to add them to a data structure that we can then convert as a csv
#if a patient doesn't exist we want to add them to a dictionary that we can then pass to the main function.
fields_for_rhino = ['encounter_date', 'encounter_time', 'encounter_id', 'first_name', 'last_name', 'date_of_birth', 'age_at_presentation', 'gender', 'medicare_number', 'indigenous_status', 'address_line1', 'suburb', 'state', 'postcode', 'emergency_contact_name', 'country_of_birth','home_language', 'patient_symptoms', 'usual_medications', 'specimen_collected', 'diagnosis', 'outcome']
rhino_data = pd.read_csv(r'H:\testauto\csvOperations\rhinodata\rhinoapp.csv',dtype={'medicare_number': 'str'}, header=0, usecols= fields_for_rhino)
rhino_data['medicare_number'] = rhino_data['medicare_number'].astype(str)
rhino_data.fillna('', inplace=True)
rhino_data = rhino_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#using a copy below just so nothing gets stuffed up. 
#below we are cleaning data
#first step is comparing the two data frames, we need to convert all the data so that it is a string in similar formats. 
rhino_data['medicare_number'] = rhino_data['medicare_number'].str.replace(' ', '')
dsp_and_redrc_df_copy['MEDICARE_NUMBER'] = dsp_and_redrc_df_copy['MEDICARE_NUMBER'].str.replace('.0', '', regex=False)
dsp_and_redrc_df_copy['MEDICARE_NUMBER'] = dsp_and_redrc_df_copy['MEDICARE_NUMBER'].str.replace('_', '', regex=False)
rhino_data['medicare_number'] = rhino_data['medicare_number'].str.replace('_', '', regex=False)
dsp_and_redrc_df_copy['MEDICARE_NUMBER'] = dsp_and_redrc_df_copy['MEDICARE_NUMBER'].str.strip()
rhino_data['medicare_number'] = rhino_data['medicare_number'].str.strip()

#we meed tp chenge the medicare number is dsp df because it has the reference number and rhino does not. We remove so we can merge on this 
#column. 
dsp_and_redrc_df_copy['MEDIRCARE_NUMBER_WREF'] = ''
dsp_and_redrc_df_copy['MEDIRCARE_NUMBER_WREF'] = dsp_and_redrc_df_copy['MEDICARE_NUMBER']
dsp_and_redrc_df_copy['MEDICARE_NUMBER'] = dsp_and_redrc_df_copy['MEDICARE_NUMBER'].str.slice(start=0, stop=10)



#get all the new patients
#we merge on multiple column values because if we merge solely based on medicare_number we end up overwriting other column values.
#this is becuase we strip out the identification number from the dsp_and_and_redrc_copy dataframe. 
#if we don't merge with an individualising parameter (i.e. DOB) then what happens is that it will overwrite column values for anyone who shares a medicare card (i.e. families)
new_patients = dsp_and_redrc_df_copy.merge(rhino_data, how='outer', left_on = ['MEDICARE_NUMBER', 'DATE_OF_BIRTH'], right_on=['medicare_number', 'date_of_birth'], indicator=True)
new_patients = new_patients[new_patients['_merge'] == 'left_only']
prexisting_df = dsp_and_redrc_df_copy.merge(rhino_data, left_on = ['MEDICARE_NUMBER', 'DATE_OF_BIRTH'], right_on=['medicare_number', 'date_of_birth'])
#print(prexisting_df[['encounter_id', 'GIVEN_NAME_x', 'FAMILY_NAME_x']])


#remove duplicates as we are matching based on medicare so we can drop based on file number
#we want to get the most recent version though so that we can update the encounter. 
prexisting_df.drop_duplicates(subset=['FILE_NUMBER'],keep='last', inplace=True)

#all the patients we couldn't find are in 'new_patients'
#all the patients that were already in the rhino app go into 'prexistng_df'. 
#all the patients in no medicare df are ones who have no medicare number but may not be new.

# get all patients without medicare 
no_medicare_df = new_patients[new_patients['MEDICARE_NUMBER'] == '']

# get all patients without medicare numbers removed from new_patient data. 
new_patients = new_patients[new_patients['MEDICARE_NUMBER']  != '']

#print(no_medicare_df.shape[0])
#print(prexisting_df.shape[0])
#print(new_patients.shape[0])

#write the patients with no medicare to csv file. 
no_medicare_df.to_csv(r'H:\testauto\csv\no_medicare.csv')
#print(prexisting_df['LAST_IN_x'][0:10])

new_patients = (new_patients.transpose()).to_dict()
#print(new_patients[0]['LAST_IN_x'][0:10])
existing_patients = (prexisting_df.transpose()).to_dict()

no_medicare_df = (no_medicare_df.transpose()).to_dict()

rhino_data_dup_check = (rhino_data.transpose()).to_dict()
