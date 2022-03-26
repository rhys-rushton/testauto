from msilib.schema import Error
from classes import patientClass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time as times
from csvOperations import csv_test
import csv
from random import randrange
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login
from auto_funcs.symptoms import symptoms
from csvOperations.fields import fields as field_data
from auto_funcs.look_for_date import look_for_date, find_date_click
import traceback


fields = field_data

#registration data structures
patient_registered = []
patient_encounter_success = []
patient_registration_error = []
patient_encounter_error = []
prexisting = []


print("Hey you are running the new patients script")
#import the new patient data
#############################
### below is where we     ###
### interact with diff    ###
### data sources. Needs   ###
### to be fixed           ###
#############################
print("HEY YOU NEED TO DO BOTH NEW PATIENTS AND PATIENTS W/OUT MEDICARE")
new_patient_data = csv_test.merged_data_pcr
#new_patient_data = spread.no_medicare_df


def add_encounter(patient_obj, driver):
    try:
        WebDriverWait(driver,timeout=4).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        
        add_encounter_button = driver.find_element_by_link_text("Add Encounter")
        add_encounter_button.click()

    except Exception as e: 
        print(e)

        times.sleep(2)
    
    try:


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
            else:
                continue

            counter += 1
        print('symps done')

        #times.sleep(30)

        no_usual_meds = driver.find_element_by_id('no_usual_medications')
        no_usual_meds.click()
        print('Usual meds done')
        print(patient_obj)

        WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.ID,'encounter_diagnosis_choice' )))
        try:
            diagnosis = Select(driver.find_element(By.ID, 'encounter_diagnosis_choice'))
            diagnosis.select_by_visible_text('Other (specify)')
            WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.ID,'encounter_diagnosis_other' )))
            driver.find_element_by_id('encounter_diagnosis_other').send_keys('Possible covid')
        except Exception as e: 
            print(e)
    
        encounter_date = driver.find_element_by_id('encounter_encounterDate')
        encounter_date.clear()
        encounter_date.send_keys(patient_obj.date[0:10])
        
        random_hour = randrange(9, 19)
        random_minute = randrange(59)
        
        encounter_time = driver.find_element_by_name('encounter_time')
        encounter_time.clear()

        if random_hour >= 12:
            encounter_time.send_keys(f'{random_hour}:{random_minute}PM')

        elif random_hour < 12:
            encounter_time.send_keys(f'{random_hour}:{random_minute}AM')

        #times.sleep(30)
        save_button = driver.find_element_by_class_name('btn.btn-dark')
        save_button.click()
        #times.sleep(30)

        try:
            url = driver.current_url
            assert url == 'https://app.respiratoryclinic.com.au/dashboard/'
            print('encounter success')
            patient_encounter_success.append(patient_obj)
            return

        except Exception as e:
            print('encounter not added')
            patient_encounter_error.append(patient_obj)
            return

    except Exception as e: 
        print("Encounter not added")
        print(e)
        times.sleep(2)
        return 


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
        date_of_birth = remove_zeroes(patient_object.DOB)
        date_of_birth_present = look_for_date(date_of_birth, driver)

        if date_of_birth_present == True:
            encounter_date = remove_zeroes(patient_object.date)
            encounter_date_present = look_for_date(encounter_date, driver)

            if encounter_date_present == True:
                prexisting.append(patient_object)
                print('encounter already there')
                return True
            else:
                #need to add encounter
                #get to the right div if there are multiple, using patient DOB
                try:
                    find_date_click(date_of_birth,driver)
                except Exception as e:
                    patient_object.error = e
                    patient_encounter_error.append(patient_object)
                    return False

                #add the encounter. 
                try:
                    add_encounter(patient_object, driver)
                   
                    #patient_encounter_success.append(patient_object)
                    return True

                except Exception as e:
                    patient_object.error = e 
                    #patient_encounter_error.append(patient_object)
                    return True
        else:
            #patient doesn't exist. 
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            return False




def register_patient(patient_obj, driver):
    print('hey we are registering a patient')

    #check to click the New Assement Patient
    try:
        new_assesment_patient_button = driver.find_element_by_link_text("New Assessment Patient")
        new_assesment_patient_button.click()

    except Exception as e: 
        patient_obj.error = e
        patient_registration_error.append(patient_obj)
        print(e)
        times.sleep(2)
        return

    #upload patient information
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

        
        adress_line_1 = driver.find_element_by_id('patient_addressLine1')
        adress_line_1.send_keys(patient_obj.address)
        suburb_field = driver.find_element_by_id('patient_suburb')
        suburb_field.send_keys(patient_obj.suburb)
        postcode_field = driver.find_element_by_id('patient_postcode')
        postcode_field.send_keys(patient_obj.post_code)



        state_field = Select(driver.find_element_by_id('patient_state'))
        if(patient_obj.post_code[0]) == '2': 
            state_field.select_by_visible_text('NSW')

        elif(patient_obj.post_code[0]) == '3':
            state_field.select_by_visible_text('VIC')

        elif(patient_obj.post_code[0]) == '4':
            state_field.select_by_visible_text('QLD')

        elif(patient_obj.post_code[0]) == '5':
            state_field.select_by_visible_text('SA')

        elif(patient_obj.post_code[0]) == '6':
            state_field.select_by_visible_text('WA')

        elif(patient_obj.post_code[0]) == '7':
            state_field.select_by_visible_text('TAS')

        elif(patient_obj.post_code[0]) == '0':
            state_field.select_by_visible_text('NT')

        
        emergency_field = driver.find_element_by_id('patient_emergencyContactName')
        emergency_field.send_keys('Nil Provided')


        country_of_birth = Select(driver.find_element_by_id('patient_countryOfBirth_choice'))
        country_of_birth.select_by_visible_text('Not stated')

        home_language = Select(driver.find_element_by_id('patient_homeLanguage_choice'))
        home_language.select_by_visible_text('Not stated')

        patient_symptoms_other = driver.find_element_by_id('patient_symptoms_choice__other')
        patient_symptoms_other.click()

        driver.find_element_by_id('patient_symptoms_other').send_keys('See encounter')
        driver.find_element_by_id('patient_reportConsent_yes').click()

        save_button = driver.find_element_by_class_name('btn.btn-dark')
        #times.sleep(30)
        save_button.click()

        #times.sleep(2)

        url = driver.current_url

        if url == 'https://app.respiratoryclinic.com.au/dashboard/':
            
            add_encounter(patient_obj, driver)
        else: 
            try: 
                times.sleep(2)
                potential_dup = driver.find_element_by_class_name('alert.alert-warning')
                
                print('Potential Duplicate')
                times.sleep(2)
                save_button = driver.find_element_by_class_name('btn.btn-dark')
                save_button.click()
                #new patient succesfully registered
                patient_registered.append(patient_obj)
                add_encounter(patient_obj, driver)

            except Exception as e:
                #unable to register patient, encounter outstanding. 
                print(e)
                times.sleep(2)
                patient_registration_error.append(patient_obj)
                

    except Exception as e:
        #unable to register patient, encounter outstanding. 
        print(e)
        print(traceback.format_exc())
        times.sleep(2)
        patient_registration_error.append(patient_obj)
        print('Error uploading data')



def new_patient_main():
    print('We are now uploading new patients')
    driver = login()


    #iterate through data
    for key in new_patient_data:
        #if key > 100:
            #print('We done')
            #break
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

        #get data for patient. 
        given_name = new_patient_data[key]['GIVEN_NAME']   
        surname = new_patient_data[key]['FAMILY_NAME']
        DOB = new_patient_data[key]['DATE_OF_BIRTH']
        gender = new_patient_data[key]['GENDER']
        medicare = new_patient_data[key]['MEDICARE_NUMBER']
        adress_1 = new_patient_data[key]['HOME_ADDRESS_LINE_1'] 
        suburb = new_patient_data[key]['HOME_SUBURB_TOWN']
        postcode = new_patient_data[key]['HOME_POSTCODE']
        encounter_date = new_patient_data[key]['ServDate'][0:10]

        patient_obj = patientClass.patient(given_name, surname, DOB, gender, medicare, adress_1, suburb, postcode, encounter_date)

        #want to double check patient doesn't exist. 
        patient_exists = check_patient_exists(patient_obj, driver)

        if patient_exists == False:
            #we then want to register and do encounter. We will call the encounter function from register patient function.  
            print('Patient DNE')
            register_patient(patient_obj, driver)
            continue
        elif patient_exists == True: 
            print('Patient Exists')
            #times.sleep(5)
            continue

new_patient_main()

#patient registration success
with open(r'H:\testauto\csv\new_patient_rego_opt\patient_rego_succ.csv', 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in patient_registered:
        writer.writerow([patient.name,patient.surname, patient.DOB, patient.gender, patient.medicare, patient.address,patient.suburb, patient.post_code, patient.date, patient.error ])

#patient registration error
with open(r'H:\testauto\csv\new_patient_rego_opt\patient_rego_err.csv', 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in patient_registration_error:
        writer.writerow([patient.name,patient.surname, patient.DOB, patient.gender, patient.medicare, patient.address,patient.suburb, patient.post_code, patient.date, patient.error ])

#patient encounter success
with open(r'H:\testauto\csv\new_patient_rego_opt\encounter_succ.csv', 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in patient_encounter_success:
        writer.writerow([patient.name,patient.surname, patient.DOB, patient.gender, patient.medicare, patient.address,patient.suburb, patient.post_code, patient.date, patient.error ])

#patient encounter error
with open(r'H:\testauto\csv\new_patient_rego_opt\encounter_err.csv', 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in patient_encounter_error:
        writer.writerow([patient.name,patient.surname, patient.DOB, patient.gender, patient.medicare, patient.address,patient.suburb, patient.post_code, patient.date, patient.error ])


#prexisting patient
with open(r'H:\testauto\csv\new_patient_rego_opt\prexisting.csv', 'w', newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([fields])
    for patient in prexisting:
        writer.writerow([patient.name,patient.surname, patient.DOB, patient.gender, patient.medicare, patient.address,patient.suburb, patient.post_code, patient.date, patient.error ])

print('Execution finished')