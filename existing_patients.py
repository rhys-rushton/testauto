#in this file the encounters for patients who already exist in the registered patient database are completed. 
#the output files are located in csv/existing_patients_output
#the script will only ad encounters for those who have not had their encounter uploaded. 
#all actions are recorded and logged. 

from classes import userClass, patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time as times
from csvOperations import spread
import csv
from random import randrange
from csvOperations.fields import fields as field_data
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login
from auto_funcs.symptoms import symptoms

fields = field_data

#get the existing patients. 
data_to_use = spread.existing_patients


#result of automation. 
encounter_success = []
encounter_error = []
already_entered = []

def automate():

    driver = login()

    try: 
        for key in data_to_use:

            driver.get("https://app.respiratoryclinic.com.au/dashboard/")

            data_to_use[key]['error_code'] = ''

            #if key > 10: 
                #break

            encounter_id = data_to_use[key]['encounter_id']
            encounter_date = data_to_use[key]['LAST_IN_x'][0:10]
            encounter_date = remove_zeroes(encounter_date)

            existing_assement_button = driver.find_element_by_link_text('Existing Assessment Patients')
            existing_assement_button.click()

            encounter_id_field = driver.find_element_by_id('encounterId')
            encounter_id_field.send_keys(encounter_id)

            search_button = driver.find_element_by_class_name('btn.btn-dark')
            search_button.click()

            try:
                assert encounter_date in driver.page_source
                print('Encounter already entered')
                data_to_use[key]['error_code'] = 'Encounter Already Entered'
                already_entered.append(data_to_use[key])
                continue
            
            except:
                print('Patient encounter has not yet been entered')


            new_encounter_button = driver.find_element_by_link_text("New Encounter")
            new_encounter_button.click()

            fever_box = driver.find_element_by_id('encounter_symptoms_choice_Feverselfreported')
            cough_box = driver.find_element_by_id('encounter_symptoms_choice_Cough')
            sore_throat = driver.find_element_by_id('encounter_symptoms_choice_Sorethroat')
            tiredness = driver.find_element_by_id('encounter_symptoms_choice_Tirednesslethargy')
            runny_nose = driver.find_element_by_id('encounter_symptoms_choice_Headache')
            headache = driver.find_element_by_id('encounter_symptoms_choice_Headache')
            joint_pain = driver.find_element_by_id('encounter_symptoms_choice_Jointpain')

            array_of_symptoms = [fever_box, cough_box, sore_throat, tiredness, runny_nose, headache, joint_pain]
            num_symptoms = symptoms(6)

            counter = 0

            while counter < num_symptoms:
                randome_index = symptoms(6)
                symptom_to_click = array_of_symptoms[randome_index]
                if symptom_to_click.is_selected() == False:
                    
                    symptom_to_click.click()
                counter += 1

            no_usual_meds = driver.find_element_by_id('no_usual_medications')
            no_usual_meds.click()

            diagnosis = Select(driver.find_element_by_id('encounter_diagnosis_choice'))
            diagnosis.select_by_visible_text('Other (specify)')
            driver.find_element_by_id('encounter_diagnosis_other').send_keys('Possible covid')
        
            encounter_date = driver.find_element_by_id('encounter_encounterDate')
            encounter_date.clear()
            encounter_date.send_keys(data_to_use[key]['LAST_IN_x'][0:10])
            
            random_hour = randrange(9, 19)
            random_minute = randrange(59)
            
            encounter_time = driver.find_element_by_name('encounter_time')
            encounter_time.clear()

            if random_hour >= 12:
                encounter_time.send_keys(f'{random_hour}:{random_minute}PM')

            elif random_hour < 12:
                encounter_time.send_keys(f'{random_hour}:{random_minute}AM')

            times.sleep(1)
            save_button = driver.find_element_by_class_name('btn.btn-dark')

            save_button.click()
            times.sleep(1)

            url = driver.current_url

            try:
                assert url == 'https://app.respiratoryclinic.com.au/dashboard/'
                print("patient success")
                encounter_success.append(data_to_use[key])
                continue

            except Exception as e:
                print("patient error")
                data_to_use[key]['error_code'] = e
                encounter_error.append(data_to_use[key])
                continue

    except Exception as e:

        print('Error')
        data_to_use[key]['error_code'] = e
        print(e)
        encounter_error.append(data_to_use[key])
        


automate()
print('Exisitng patients done.')


#write errors to csv
with open(r'H:\testauto\csv\existing_patients_output\existing_encounter_err.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(encounter_error)

#write successes to csv
with open(r'H:\testauto\csv\existing_patients_output\encounter_success.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(encounter_success)

#write patients who have had encounters entered to csv
with open(r'H:\testauto\csv\existing_patients_output\already_done.csv', 'w', newline='') as f: 
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(already_entered)

