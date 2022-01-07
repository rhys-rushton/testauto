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


fields = ['FILE_NUMBER', 'FAMILY_NAME_x','GIVEN_NAME_x','HOME_ADDRESS_LINE_1_x',
            'HOME_ADDRESS_LINE_2_x','HOME_SUBURB_TOWN_x ','HOME_POSTCODE_x ',
            'HOME_PHONE_x','AGE_x', 'GENDER_x','LAST_IN_x', 'DATE_OF_BIRTH',
            'PATIENT_ID', 'MEDIRCARE_NUMBER_WREF', 'encounter_date', 'encounter_time',
            'encounter_id','first_name', 'last_name', 'date_of_birth', 'age_at_presentation',
            'gender', 'success_code', 'error_code']

#registration data structures
new_patients_succesfully_entered = []
new_patients_w_error = []

#new_patient_encounter_registration
new_patient_encounter = []
new_patient_encounter_error = []


print("Hey you are running the new patients script")
#import the new patient data
new_patient_data = spread.new_patients

#create the user class
em = input("enter email please ")
pw = input("enter pword")
user = userClass.User(em, pw)
driver = webdriver.Chrome(executable_path=r'C:\Users\RRushton\Desktop\chromedriver.exe')

def main ():
    print("Please get your google auth ready")
    times.sleep(10)
    driver.get("https://app.respiratoryclinic.com.au/login")
    userName = driver.find_element_by_id("inputUsername")
    passWord = driver.find_element_by_id("inputPassword")
    firstSignIn = driver.find_element_by_xpath("//*[@id=\"regular-login\"]/button")
    userName.clear()
    passWord.clear()
    userName.send_keys(user.email)
    passWord.send_keys(user.password)
    firstSignIn.click()
    print("Please enter you're authentication code")

    #wait for user to enter authentication code. 
    try:
        WebDriverWait(driver,timeout=120).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        print("You're through")
    except:
        print("You did not enter authentication code succesfully")
        return 
    
    new_patient_registration()


def new_patient_registration():
    print('We are now uploading new patients')
    

    for key in new_patient_data:
        #if key > 10: 
            #break
        given_name = new_patient_data[key]['GIVEN_NAME_x']   
        surname = new_patient_data[key]['FAMILY_NAME_x']
        DOB = new_patient_data[key]['DATE_OF_BIRTH']
        gender = new_patient_data[key]['GENDER_x']
        medicare = new_patient_data[key]['MEDIRCARE_NUMBER_WREF']
        adress_1 = new_patient_data[key]['HOME_ADDRESS_LINE_1_x'] 
        suburb = new_patient_data[key]['HOME_SUBURB_TOWN_x']
        postcode = new_patient_data[key]['HOME_POSTCODE_x'] 

        WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

        try:
            new_assesment_patient_button = driver.find_element_by_link_text("New Assessment Patient")
            new_assesment_patient_button.click()
        except Exception as e: 
            print(e)
            new_patients_w_error.append(new_patient_data[key])
            break
        
        #get the web stuff and upload it
        try:
            name_field = driver.find_element_by_id('patient_firstName')
            name_field.send_keys(given_name)

            surname_field = driver.find_element_by_id('patient_lastName')  
            surname_field.send_keys(surname)

            referral_field = Select(driver.find_element_by_id('patient_referralSource_choice'))
            referral_field.select_by_visible_text('General Practice website')

            dob_field = driver.find_element_by_id('patient_dateOfBirth')
            dob_field.send_keys(DOB)

            gender_field = Select(driver.find_element_by_id('patient_gender'))

            if gender == '':
                gender_field.select_by_visible_text('Not Stated')
            elif gender == 'M':
                gender_field.select_by_visible_text('Male')
            elif gender == 'F':
                gender_field.select_by_visible_text('Female')

            atsi_field = Select(driver.find_element_by_id('patient_indigenousStatus'))
            atsi_field.select_by_visible_text('Not stated')

            #enter medicare number
            medicare_field = Select(driver.find_element_by_id('patient_typeOfIdProvided'))
            if medicare == '':
                medicare_field.select_by_visible_text('No - Other ID sighted')
            elif medicare != '': 
                medicare_field.select_by_visible_text('Yes - Please enter Medicare Card number')
                patient_medicare_num = driver.find_element_by_id('patient_medicareNumber')
                patient_medicare_ref = driver.find_element_by_id('patient_medicareReferenceNumber')
                patient_medicare_num.send_keys(medicare[0:10])
                patient_medicare_ref.send_keys(medicare[10])

            adress_line_1 = driver.find_element_by_id('patient_addressLine1')
            adress_line_1.send_keys(adress_1)
            suburb_field = driver.find_element_by_id('patient_suburb')
            suburb_field.send_keys(suburb)
            postcode_field = driver.find_element_by_id('patient_postcode')
            postcode_field.send_keys(postcode)

            state_field = Select(driver.find_element_by_id('patient_state'))
            if(postcode[0]) == '2': 
                state_field.select_by_visible_text('NSW')

            elif(postcode[0]) == '3':
                state_field.select_by_visible_text('VIC')

            elif(postcode[0]) == '4':
                state_field.select_by_visible_text('QLD')

            elif(postcode[0]) == '5':
                state_field.select_by_visible_text('SA')

            elif(postcode[0]) == '6':
                state_field.select_by_visible_text('WA')

            elif(postcode[0]) == '7':
                state_field.select_by_visible_text('TAS')

            elif(postcode[0]) == '0':
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

            new_patients_succesfully_entered.append(new_patient_data[key])

            times.sleep(2)
            save_button = driver.find_element_by_class_name('btn.btn-dark')
            save_button.click()
            
            try: 
                driver.find_element_by_class_name('alert.alert-warning')
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")
                #times.sleep(5)
            except:
                print("You are adding encounter from new_patient func")
                times.sleep(5)
                #new_patient_add_encounter(new_patient_data, key)
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")

            

            #add the encounter for the patient
            #new_patient_add_encounter(new_patient_data, key)
            #driver.get("https://app.respiratoryclinic.com.au/dashboard/")



        except:
            print("Hey this is error in new patient upload ")
            new_patients_w_error.append(new_patient_data[key])
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")



     #write to the csvs
    with open(r'H:\testauto\csv\new_succes.csv', 'w', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(new_patients_succesfully_entered)

    with open(r'H:\testauto\csv\new_error.csv', 'w', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(new_patients_w_error)


#new patient add encounter
#this is where we add the encounter. 
def new_patient_add_encounter(new_patient_data, key):
    print("hey")


    try:
        WebDriverWait(driver,timeout=120).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        times.sleep(5)
        add_encounter_button = driver.find_element_by_link_text("Add Encounter")
        add_encounter_button.click()

    except Exception as e: 
        print(e)
        print("Error in new function")
        new_patient_encounter_error.append(new_patient_data[key])
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")

    fever_box = driver.find_element_by_id('encounter_symptoms_choice_Feverselfreported')
    cough_box = driver.find_element_by_id('encounter_symptoms_choice_Cough')
    sore_throat = driver.find_element_by_id('encounter_symptoms_choice_Sorethroat')
    tiredness = driver.find_element_by_id('encounter_symptoms_choice_Tirednesslethargy')
    runny_nose = driver.find_element_by_id('encounter_symptoms_choice_Headache')
    headache = driver.find_element_by_id('encounter_symptoms_choice_Headache')
    joint_pain = driver.find_element_by_id('encounter_symptoms_choice_Jointpain')

    array_of_symptoms = [fever_box, cough_box, sore_throat, tiredness, runny_nose, headache, joint_pain]
    random = randrange(6)
    symptom_to_click = array_of_symptoms[random] 
    symptom_to_click.click()

    no_usual_meds = driver.find_element_by_id('no_usual_medications')
    no_usual_meds.click()

    diagnosis = Select(driver.find_element_by_id('encounter_diagnosis_choice'))
    diagnosis.select_by_visible_text('Other (specify)')
    driver.find_element_by_id('encounter_diagnosis_other').send_keys('Possible covid')

    encounter_date = driver.find_element_by_id('encounter_encounterDate')
    encounter_date.send_keys(new_patient_data[key]['LAST_IN_DATE_x'][0:10])
    
    random_hour = randrange(9, 19)
    random_minute = randrange(59)
    
    encounter_time = driver.find_element_by_name('encounter_time')
    encounter_time.clear()
    encounter_time.send_keys(f'{random_hour}:{random_minute}')

    times.sleep(20)

    


    #make sure to write errors and succeses to csv



 
    
    


main()

