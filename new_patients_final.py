from classes import patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time as times
from csvOperations import spread
import csv
from random import randrange
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login
from auto_funcs.symptoms import symptoms
from csvOperations.fields import fields as field_data


fields = field_data

#registration data structures
new_patients_succesfully_entered = []
new_patients_w_error = []

#new_patient_encounter_registration
new_patient_encounter = []
new_patient_encounter_error = []


print("Hey you are running the new patients script")
#import the new patient data
new_patient_data = spread.new_patients


def check_patient_exists(patient_object, driver):
    

    #needs to return true or false if patient exists.
    exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
    exisiting_patient_button.click()
    first_name_input = driver.find_element_by_id('firstName')
    last_name_input = driver.find_element_by_id('lastName')
    first_name_input.send_keys(patient_object.name)
    last_name_input.send_keys(patient_object.surname)
    search_button = driver.find_element_by_class_name('btn.btn-dark')
    search_button.click()

    #we are checking of the easy case where the patient definitely doesn't exist. 
    try: 
        driver.find_element_by_xpath("//*[contains(text(), 'No results.')]").is_displayed()
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        return False
    except:

        #want to check if their DOB is there
        #if it isn't then return false
        # i it is: 
            #if DOB is there then we want to check for their encounter date

        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        return True
        
def register_patient(patient_obj, driver):
    print('hey we are registering a patient')

    #check to click the New Assement Patient
    try:
        new_assesment_patient_button = driver.find_element_by_link_text("New Assessment Patient")
        new_assesment_patient_button.click()

    except Exception as e: 
        print(e)
        patient_obj.error = e
        new_patients_w_error.append(patient_obj)
        return

    #uploaed patient information
    try:
        name_field = driver.find_element_by_id('patient_firstName')
        name_field.send_keys(patient_obj.name)

        surname_field = driver.find_element_by_id('patient_lastName')  
        surname_field.send_keys(patient_obj.surname)

        referral_field = Select(driver.find_element_by_id('patient_referralSource_choice'))
        referral_field.select_by_visible_text('General Practice website')

        dob_field = driver.find_element_by_id('patient_dateOfBirth')
        dob_field.send_keys(patient_obj.DOB)

        gender_field = Select(driver.find_element_by_id('patient_gender'))
        if patient_obj.gender == '':
            gender_field.select_by_visible_text('Not Stated')
        elif patient_obj.gender == 'M':
            gender_field.select_by_visible_text('Male')
        elif patient_obj.gender == 'F':
            gender_field.select_by_visible_text('Female')

        atsi_field = Select(driver.find_element_by_id('patient_indigenousStatus'))
        atsi_field.select_by_visible_text('Not stated')

         #enter medicare number
        medicare_field = Select(driver.find_element_by_id('patient_typeOfIdProvided'))
        if patient_obj.medicare == '':
            medicare_field.select_by_visible_text('No - Other ID sighted')
        elif patient_obj.medicare != '': 
            medicare_field.select_by_visible_text('Yes - Please enter Medicare Card number')
            patient_medicare_num = driver.find_element_by_id('patient_medicareNumber')
            patient_medicare_ref = driver.find_element_by_id('patient_medicareReferenceNumber')
            patient_medicare_num.send_keys(patient_obj.medicare[0:10])
            patient_medicare_ref.send_keys(patient_obj.medicare[10])



    except:
        print('Error with name.')

    
        







def add_encounter(patient_obj, driver):
    print('hey')














def new_patient_main():
    print('We are now uploading new patients')
    driver = login()


    #iterate through data
    for key in new_patient_data:
        if key > 10:
            print('We done')
            break
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

        #get data for patient. 
        given_name = new_patient_data[key]['GIVEN_NAME_x']   
        surname = new_patient_data[key]['FAMILY_NAME_x']
        DOB = new_patient_data[key]['DATE_OF_BIRTH']
        gender = new_patient_data[key]['GENDER_x']
        medicare = new_patient_data[key]['MEDIRCARE_NUMBER_WREF']
        adress_1 = new_patient_data[key]['HOME_ADDRESS_LINE_1_x'] 
        suburb = new_patient_data[key]['HOME_SUBURB_TOWN_x']
        postcode = new_patient_data[key]['HOME_POSTCODE_x']
        encounter_date = new_patient_data[key]['LAST_IN_x'][0:10]

        patient_obj = patientClass.patient(given_name, surname, DOB, gender, medicare, adress_1, suburb, postcode, encounter_date)

        #want to double check patient doesn't exist. 
        patient_exists = check_patient_exists(patient_obj, driver)

        if patient_exists == False:
            #we then want to register and do encounter. 
            print('Patient DNE')
            #register_patient(patient_obj, driver)
            continue
        elif patient_exists == True: 
            print('Patient Exists')
            continue


            

                    

new_patient_main()
            
        
     