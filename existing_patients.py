#import the user class object
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

#get the existing patients. 
data_to_use = spread.existing_patients

#login. 
em = input("enter email please ")
pw = input("enter pword")
user = userClass.User(em, pw)
driver = webdriver.Chrome(executable_path=r'C:\Users\RRushton\Desktop\chromedriver.exe')

encounter_success = []

encounter_error = []



def rand_symp_array (range):

    number = randrange(range)
    return number

def rand_symp_num (range):

    number =  randrange(range)
    return number

def automate():
    print("Have your authentication ready please")
    #driver = webdriver.Chrome(executable_path=r'C:\Users\RRushton\Desktop\chromedriver.exe')
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
    

    try: 
        for key in data_to_use:

            data_to_use[key]['error_code'] = ''

            if key > 10: 
                break
            driver.get("https://app.respiratoryclinic.com.au/login")
            encounter_id = data_to_use[key]['encounter_id']
            encounter_date = data_to_use[key]['LAST_IN_x'][0:10]

            existing_assement_button = driver.find_element_by_link_text('Existing Assessment Patients')
            existing_assement_button.click()

            encounter_id_field = driver.find_element_by_id('encounterId')
            encounter_id_field.send_keys(encounter_id)

            search_button = driver.find_element_by_class_name('btn.btn-dark')
            search_button.click()

            new_encounter_button = driver.find_element_by_link_text("New Encounter")
            new_encounter_button .click()

            fever_box = driver.find_element_by_id('encounter_symptoms_choice_Feverselfreported')
            cough_box = driver.find_element_by_id('encounter_symptoms_choice_Cough')
            sore_throat = driver.find_element_by_id('encounter_symptoms_choice_Sorethroat')
            tiredness = driver.find_element_by_id('encounter_symptoms_choice_Tirednesslethargy')
            runny_nose = driver.find_element_by_id('encounter_symptoms_choice_Headache')
            headache = driver.find_element_by_id('encounter_symptoms_choice_Headache')
            joint_pain = driver.find_element_by_id('encounter_symptoms_choice_Jointpain')

            array_of_symptoms = [fever_box, cough_box, sore_throat, tiredness, runny_nose, headache, joint_pain]
            num_symptoms = rand_symp_num(6)

            counter = 0

            while counter < num_symptoms:
                randome_index = rand_symp_array(6)
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

            times.sleep(20)
            save_button = driver.find_element_by_css_selector('btn.btn-dark')
            save_button.click()

            try:
                WebDriverWait(driver,timeout=2).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
                print("patient success")
                encounter_success.append(data_to_use[key])
            except Exception as e:
                print("patient error")
                data_to_use[key]['error_code'] = e
                encounter_error.append(data_to_use[key])
       

    except Exception as e:
        print('Error')
        data_to_use[key]['error_code'] = e
        encounter_error.append(data_to_use[key])
        


automate()

#Gnomescript