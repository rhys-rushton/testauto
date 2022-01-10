from classes import userClass
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


def new_patient_registration():
    print('We are now uploading new patients')
    driver = login()


    #iterate through data
    for key in new_patient_data:

        if key > 10:
            break
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        
        try:
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

             #want to double check patient doesn't exist. 
            try:
                exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
                exisiting_patient_button.click()
                first_name_input = driver.find_element_by_id('firstName')
                last_name_input = driver.find_element_by_id('lastName')
                first_name_input.send_keys(given_name)
                last_name_input.send_keys(surname)
                search_button = driver.find_element_by_class_name('btn.btn-dark')
                search_button.click()
                new_patient_text = driver.find_element_by_xpath("//*[contains(text(), 'No results.')]").is_displayed()
                print('this is a new patient.')
                #register and do encounter

            except:
                print('This is not a new patient new patient. ')
                #check if the encounter date is there
                #get the right patient div. 
                #if not then add the encounter. 








        except:
            print('patient not loaded succesfully. ')
       
        