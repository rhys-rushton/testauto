from numpy import int64
import pandas as pd

#change this to matts report
red_rc = pd.read_csv(r'H:\testauto\csvOperations\item_number\REDRC.csv', header=0, encoding='CP1252')
red_rc = red_rc.drop(columns=['Patient','Patient Type','Payer','Account Payer Type', 'Date','Brn','Doc','Stf','Inv #','Item','Transaction Type','Transaction Status','GST','Amount','Fee Type','Analysis Group'])
red_rc = red_rc.rename(columns={'File #': 'FILE_NUMBER'})
dsp_patients = pd.read_csv(r'H:\testauto\csvOperations\dsp\DSPatients.csv', header=0, encoding='CP1252')
dsp_patients = dsp_patients.drop(columns=['patient_name','full_name', 'full_suburb', 'address', 'full_mailing_suburb', 'TITLE', 'HOME_ADDRESS_LINE_2', 'USUAL_CLINIC', 'USUAL_DOCTOR', 'TYPE_CODE',	'STATUS_CODE', 'PRACTICE_DEFINABLE_FIELD1_CODE', 'PRACTICE_DEFINABLE_FIELD2_CODE','PRACTICE_DEFINABLE_FIELD3_CODE',	'PRACTICE_DEFINABLE_FIELD4_CODE','PRACTICE_DEFINABLE_FIELD5_CODE','PRACTICE_DEFINABLE_FIELD6','PRACTICE_DEFINABLE_FIELD7',	'PRACTICE_DEFINABLE_FIELD8', 'PRACTICE_DEFINABLE_FIELD9', 'PRACTICE_DEFINABLE_FIELD10', 'FIRST_IN', 'LAST_IN', 'ALERTS', 'CLINIC_CODE', 'PATIENT_ID', 'MAILING_ADDRESS_LINE_1', 'MAILING_ADDRESS_LINE_2', 'MAILING_SUBURB_TOWN', 'MAILING_POSTCODE','FAMILY_ID' , 'email_ADDRESS', 'VETERAN_AFFAIRS_NUMBER','VETERAN_FILE_NUMBER_EXPIRY_DATE',	'PATIENT_HEALTH_CARE_CARD', 'PATIENT_HLTH_CARE_CARD_EX_DATE', 'SAFETY_NET_NO'])
dsp_patients.FILE_NUMBER = dsp_patients.FILE_NUMBER.astype(int)


merged_data_pcr = pd.merge(red_rc, dsp_patients, on='FILE_NUMBER', how ='inner')
merged_data_pcr.to_csv('test.csv', header=True)

#drop any duplicates made in the merge based off FILE_NUMBER and ENCOUNTER_DATE



#use matt report:
    #get file number
    #get encounter date

#from dsp get:
    #first name 
    #last name 
    #etc

#merge these two on file number. 

#given_name, surname, DOB, gender, medicare, adress_1, suburb, postcode, encounter_date