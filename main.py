#import the user class object
from classes import userClass, patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as times
import pandas as pd
from csvOperations import spread

###############
###NEED TO CHANGE BELOw[remove 0]
data_to_use = spread.data_done
#print(data_to_use)
print(data_to_use)

#patients who are new
#eventually this will be updated and not relevant. 
new_patients = {}


#create the user class
#import user Class Object 
em = input("enter email please ")
pw = input("enter pword")
user = userClass.User(em, pw)

def navigate_res_app ():
    driver = webdriver.Chrome()
    #driver.get("https://app.respiratoryclinic.com.au/login")
    #userName = driver.find_element_by_id("inputUsername")
    #passWord = driver.find_element_by_id("inputPassword")
    #firstSignIn = driver.find_element_by_xpath("//*[@id=\"regular-login\"]/button")
    #userName.clear()
    #passWord.clear()
    #userName.send_keys(user.email)
    ##passWord.send_keys(user.password)
    #firstSignIn.click()
    #######################################
    try: 
        WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

        exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
        exisiting_patient_button.click()

        times.sleep(5)
        encounter_id_input = driver.find_element_by_xpath('//*[@id="encounterId"]')
        
        encounter_id_input.send_keys("2417940")
        search_button = driver.find_element_by_class_name('btn.btn-dark')
        search_button.click()
        times.sleep(5)

        try:

            new_encounter_button = driver.find_element_by_link_text("New Encounter")
            new_encounter_button.click()
            #checkbox
            no_symptoms_button = driver.find_element_by_xpath('//*[@id="encounter_symptoms_choice"]/div[20]/label')
            #tickbox
            usual_medications = driver.find_element_by_xpath('//*[@id="encounter_usualMedications"]')
            #speciman dropdon
            speciman = driver.find_element_by_xpath('//*[@id="encounter_specimenCollected"]')
            #diagnosis dropdown
            diagnosis = driver.find_element_by_xpath('//*[@id="encounter_diagnosis_choice"]')
            #outocme  dropdown
            outcome = driver.find_element_by_xpath('//*[@id="encounter_outcome_choice"]')

            #certificate dropdown 
            certificate = driver.find_element_by_xpath('//*[@id="encounter_outcome_choice"]')

            #sumbmit 
            submit = driver.find_element_by_xpath('//input[@type="submit"]')
            print("Patient found")
            
        
        except: 
            ##write this patient and their details to file. 
            print("THis is a new patient.")





     


    except:
        #exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
        #exisiting_patient_button.click()
        times.sleep(10)
        print("Couldn't Click Existing Assement Patients Button or Error with Encounter ID")


#navigate_res_app()





    
def automate(patient_dict, patient_class):
    print('''
    Have your auth ready
    Have your auth ready
    Have your auth ready
    Have your auth ready
    ''')
    driver = webdriver.Chrome()
    driver.get("https://app.respiratoryclinic.com.au/login")
    userName = driver.find_element_by_id("inputUsername")
    passWord = driver.find_element_by_id("inputPassword")
    firstSignIn = driver.find_element_by_xpath("//*[@id=\"regular-login\"]/button")
    userName.clear()
    passWord.clear()
    userName.send_keys(user.email)
    passWord.send_keys(user.password)
    firstSignIn.click()
    #enter google auth code part
    #select auth input 
    authInput = driver.find_element_by_xpath("//*[@id=\"two_factor_register_code\"]")
    authLogin = driver.find_element_by_xpath("/html/body/main/div/form/p[1]/button")
    #new patients counter
    #counts number of new patients use this value to index the new ditionary
    #when using in function call this as index after updating value
    new_patients_counter = 0



    ##need to change this so I wait for user to click login. 
    #define a function so the webdrive waits for user 
    try:
        WebDriverWait(driver,timeout=30).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        print("You're through")
    except:
        print("You did not login succesfully")
        return 
    

    times.sleep(10)
    print("yo")

    for key in patient_dict:
        #print(key)
        date = patient_dict[key]['encounter_date']
        time = patient_dict[key]['encounter_time']
        ident = patient_dict[key]['encounter_id']
        first_name = patient_dict[key]['first_name']
        last_name = patient_dict[key]['last_name']
        DOB = patient_dict[key]['date_of_birth']
        age = patient_dict[key]['age_at_presentation']
        gender = patient_dict[key]['gender']
        medicare = patient_dict[key]['medicare_number']
        atsi =  patient_dict[key]['indigenous_status']
        address = patient_dict[key]['address_line1']
        suburb = patient_dict[key]['suburb']
        state = patient_dict[key]['state']
        postcode = patient_dict[key]['postcode']
        emergency = patient_dict[key]['emergency_contact_name']
        birth_country = patient_dict[key]['country_of_birth']
        language = patient_dict[key]['home_language']
        symptoms = patient_dict[key]['patient_symptoms']
        meds = patient_dict[key]['usual_medications']
        specimen = patient_dict[key]['specimen_collected']
        diagnosis = patient_dict[key]['diagnosis']
        outcome = patient_dict[key]['outcome']
        patient = patient_class.Patient(date,time,ident,first_name, last_name, DOB, age, gender, medicare, atsi, address, suburb, state, postcode, emergency, birth_country, language, symptoms, meds,specimen, diagnosis, outcome )
        print(patient.first_name+ " " + patient.last_name + " " + gender + f"{ident}")
    
        try: 
            WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

            exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
            exisiting_patient_button.click()

            times.sleep(5)
            encounter_id_input = driver.find_element_by_xpath('//*[@id="encounterId"]')
            
            encounter_id_input.send_keys(ident)
            search_button = driver.find_element_by_class_name('btn.btn-dark')
            search_button.click()
            times.sleep(5)

            try:

                new_encounter_button = driver.find_element_by_link_text("New Encounter")
                #new_encounter_button.click()
                #checkbox
                #no_symptoms_button = driver.find_element_by_xpath('//*[@id="encounter_symptoms_choice"]/div[20]/label')
                #tickbox
                #usual_medications = driver.find_element_by_xpath('//*[@id="encounter_usualMedications"]')
                #speciman dropdon
                #speciman = driver.find_element_by_xpath('//*[@id="encounter_specimenCollected"]')
                #diagnosis dropdown
                #diagnosis_field = driver.find_element_by_xpath('//*[@id="encounter_diagnosis_choice"]')
                #outocme  dropdown
                #outcome_outcome = driver.find_element_by_xpath('//*[@id="encounter_outcome_choice"]')

                #certificate dropdown 
                #certificate = driver.find_element_by_xpath('//*[@id="encounter_outcome_choice"]')

                #sumbmit 
                #submit = driver.find_element_by_xpath('//input[@type="submit"]')
                print("Patient found" + first_name)
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            
        
            except: 
                ##write this patient and their details to the new patient dict. 
                print("This is a new patient." + first_name)
                new_patients_counter += 1
                new_patients[new_patients_counter] = patient_dict["key"]
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")
                


        except:
            #exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
            #exisiting_patient_button.click()
            times.sleep(10)
            print("Couldn't Click Existing Assement Patients Button or Error with Encounter ID")

        

        
       
    

    
automate(data_to_use, patientClass)






