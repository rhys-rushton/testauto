#want to be able to select patients within a specific date range. 
#then i want to search patient, verify i have correct one by looking at date of birth
#then I want to loop through the encounters they have and if they have encounters then I want to add a follow up.
#then I want to write this patient file to a csv file. 
# don't neccesarily want to drop duplicates. 

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


no_follow_up_no_speciman = []
follow_up_done = []
error = []





def add_follow_up(driver, patient_object):
    try: 
        date = datetime.strptime(patient_object.encounter_date, '%d/%m/%Y') + timedelta(days= randint(1,3))
        date = datetime.strftime(date,'%d/%m/%Y')
        test_result_input = Select(driver.find_element_by_id('followup_testResults'))
        test_result_input.select_by_visible_text('Negative')

        test_result_received_date = driver.find_element_by_id('followup_dateResultsReceived')
        test_result_received_date.clear()
        test_result_received_date.send_keys(date)

        #test_result_communicated_date = driver.find_element_by_id('followup_patientContactedDate')
        #test_result_communicated_date.clear()
        #test_result_communicated_date.send_keys(date)

        results_communicated_y_n = Select(driver.find_element_by_id('followup_patientContacted'))
        results_communicated_y_n.select_by_visible_text('Yes')

        sms_check = driver.find_element_by_id('followup_patientContactMethods_choice_SMS')
        sms_check.click()

        #save_button = driver.find_element_by_class_name('btn.btn-dark')
        #save_button.click()

        time.sleep(1)
    except Exception as e: 
        #print(e)
        #print(traceback.format_exc())
        print('error in add follow up')



def check_follow_up(driver, patient_object):
    print('checking for follow up.')
    if 'Follow-ups' in driver.page_source: 
        print('follow_up_done')
        
        #GET RID OF THIS
        #driver.find_element_by_link_text('Add follow-up').click()
        #add_follow_up(driver, patient_object)


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
        
       
   



def find_encounter(driver, encounter_date, patient_object):

    print('Hey you are finding the encounter')
    for encounter in driver.find_elements_by_class_name('list-group'):
        try:
            assert encounter_date in encounter.get_attribute('innerHTML')
            driver.find_element_by_link_text('Edit encounter').click()
            #print(encounter_date)
            time.sleep(1)

            #check if follow up is there. 
            check_follow_up(driver, patient_object)


        except Exception as e:
            print('error')
            print(e)
            



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

fields = ['name', 'surname', 'DOB', 'encounter_id', 'encounter_date', 'outcome']


with open(r'H:\testauto\follow_up_output\no_follow_no_spec', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in no_follow_up_no_speciman:
        writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])

with open(r'H:\testauto\follow_up_output\follow_done', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in follow_up_done:
         writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])

with open(r'H:\testauto\follow_up_output\error', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in error:
        writer.writerow([patient.name, patient.surname, patient.DOB, patient.encounter_id, patient.encounter_date, patient.outcome])
