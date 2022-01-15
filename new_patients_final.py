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
from auto_funcs.look_for_date import look_for_date


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


def add_encounter(patient_obj, driver):
    try:
        WebDriverWait(driver,timeout=120).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        times.sleep(5)
        add_encounter_button = driver.find_element_by_link_text("Add Encounter")
        add_encounter_button.click()

    except Exception as e: 
        print(e)
        print("Error in new function")
        #add patient to error list
        return 

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
        encounter_date.send_keys(patient_obj.date[0:10])
        
        random_hour = randrange(9, 19)
        random_minute = randrange(59)
        
        encounter_time = driver.find_element_by_name('encounter_time')
        encounter_time.clear()

        if random_hour >= 12:
            encounter_time.send_keys(f'{random_hour}:{random_minute}PM')

        elif random_hour < 12:
            encounter_time.send_keys(f'{random_hour}:{random_minute}AM')

        times.sleep(5)
        save_button = driver.find_element_by_class_name('btn.btn-dark')

        try:
            save_button.click()
            WebDriverWait(driver,timeout=2).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
            print("patient success")
            #add patient to success
         

        except Exception as e:
            print("patient error")
            #add patient to error
            




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
                return True
            else:
                #need to add encounter
                new_encounter_button = driver.find_element_by_link_text("New Encounter")
                new_encounter_button.click()
                add_encounter(patient_object, driver)
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
        print(e)
        patient_obj.error = e
        new_patients_w_error.append(patient_obj)
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
        save_button.click()

        url = driver.current_url()

        if url == 'https://app.respiratoryclinic.com.au/dashboard/':
            #new patient succesfully registered
            add_encounter(patient_obj, driver)
        else: 
            try: 
                potential_dup = driver.find_element_by_class_name('alert.alert-warning')
                print('Potential Duplicate')
                times.sleep(2)
                save_button.click()
                #new patient succesfully registered
                add_encounter(patient_obj, driver)

                

            except:
                #unable to register patient, encounter outstanding. 
                print('hello')


    except Exception as e:
        #unable to register patient, encounter outstanding. 
        print('Error uploading data')



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
            #we then want to register and do encounter. We will call the encounter function from register patient function.  
            print('Patient DNE')
            register_patient(patient_obj, driver)
            continue
        elif patient_exists == True: 
            print('Patient Exists')
            continue

new_patient_main()
            
        
     