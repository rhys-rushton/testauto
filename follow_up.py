#Automation of follow-ups for patients who have had COVID-19 PCR Tests
#This script automates the uploading of the patients data. 
#all data needs to be extracted from the aspen medical rhino app, the data is cleaned in 'csvOperations\spread.py'
from datetime import datetime, timedelta
from auto_funcs.login import login
from csvOperations.spread import rhino_follow_up_dict as data_to_use
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from classes import patientClass
import time
from random import randint
from auto_funcs.date_string_zeroes import remove_zeroes
import traceback
import csv

#these lists are where we will hold the output from the script. 
#these lists are used to generate the csvs, see bottom of file. 

#patients who have not had a follow up and not had a speciman collected. 
no_follow_up_no_speciman = []
#patients for whom the script succesfully completes the follow up. 
follow_up_done = []
#patient who has an error thrown, error code is appended to the patient object so we can troubleshoot if neccessary. 
error = []


#This functions adds the follow up. 
def add_follow_up(driver, patient_object):
    try: 
        #create the date for contacting the patient. 
        date = datetime.strptime(patient_object.encounter_date, '%d/%m/%Y') + timedelta(days= randint(1,3))
        date = datetime.strftime(date,'%d/%m/%Y')

        #upload the covid-19 test result. 
        #we assume all patients are negative because all positives are entered manually. 
        test_result_input = Select(driver.find_element_by_id('followup_testResults'))
        test_result_input.select_by_visible_text('Negative')

        #send the date varaible to the date input on the webpage. 
        test_result_received_date = driver.find_element_by_id('followup_dateResultsReceived')
        test_result_received_date.clear()
        test_result_received_date.send_keys(date)

        #select the results communicated option. 
        results_communicated_y_n = Select(driver.find_element_by_id('followup_patientContacted'))
        results_communicated_y_n.select_by_visible_text('Yes')

        #all negative patients are contacted via SMS
        sms_check = driver.find_element_by_id('followup_patientContactMethods_choice_SMS')
        sms_check.click()

        #Save the follow up encounter. 
        #save_button = driver.find_element_by_class_name('btn.btn-dark')
        #save_button.click()

        time.sleep(1)
    except Exception as e: 
        #print(e)
        #print(traceback.format_exc())
        print('error in add follow up')


#Check whether or not the patient has had a follow up. 
def check_follow_up(driver, patient_object):
    print('checking for follow up.')

    #If a follow up has been done then the word 'Follow-ups' will be in the page source. 
    if 'Follow-ups' in driver.page_source: 
        print('follow_up_done')

    #check that the patient has had a speciman collected and then add the follow up. 
    #otherwise just add the patient to the relevant CSV. 
    else:
        field = 'Yes, specimen collected'
        speciman_dropdown = Select(driver.find_element_by_id('encounter_specimenCollected'))
        if field == speciman_dropdown.first_selected_option.text:
            print('match')
            driver.find_element_by_link_text('Add follow-up').click()
            add_follow_up(driver, patient_object)
        else:
            print('no speciman collected but followup not done.')
            no_follow_up_no_speciman.append(patient_object)
        

#Find the patients encounter. 
def find_encounter(driver, encounter_date, patient_object):

    print('Hey you are finding the encounter')
    #there could be mutliple encounters so we loop through the encounters and look for each one. 
    #we select the relevant encounter by matching by date. 
    for encounter in driver.find_elements_by_class_name('list-group'):
        try:
            assert encounter_date in encounter.get_attribute('innerHTML')
            driver.find_element_by_link_text('Edit encounter').click()
            time.sleep(1)

            #check if follow up is there. 
            check_follow_up(driver, patient_object)


        except Exception as e:
            print('error')
            print(e)
            
#look the patient up. 
def look_up_patient(driver, patient_object):

    existing_patients = driver.find_element_by_link_text('Existing Assessment Patients')
    existing_patients.click()

    encounter_id_input = driver.find_element_by_id('encounterId')
    encounter_id_input.send_keys(patient_object.encounter_id)

    search_button = driver.find_element_by_class_name('btn.btn-dark')
    search_button.click()

    time.sleep(1)
    encounter_date = remove_zeroes(patient_object.encounter_date)
    find_encounter(driver, encounter_date, patient_object)

#create each patient object and loop through dictionary. 
def main ():
    print('We are now doing the follow ups')
    driver = login()

    for key in data_to_use:
        if key > 10:
            break
        try: 
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
            encounter_date = data_to_use[key]['encounter_date']
            encounter_id = data_to_use[key]['encounter_id']
            name = data_to_use[key]['first_name']
            surname = data_to_use[key]['last_name']
            DOB = data_to_use[key]['date_of_birth']
            

            patient_obj = patientClass.patient_follow_up(name, surname, DOB, encounter_id, encounter_date)
            look_up_patient(driver, patient_obj)

            patient_obj.outcome = 'success'
            follow_up_done.append(patient_obj)

        except Exception as e:
            patient_obj.outcome = e
            error.append(patient_obj)



main()
print('Follow ups done.')

#fields for the csv
fields = ['name', 'surname', 'DOB', 'encounter_id', 'encounter_date', 'outcome']
with open(r'H:\testauto\follow_up_output\no_follow_no_spec.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in no_follow_up_no_speciman:
        writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])

with open(r'H:\testauto\follow_up_output\follow_done.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in follow_up_done:
         writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])

with open(r'H:\testauto\follow_up_output\error.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in error:
        writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])
