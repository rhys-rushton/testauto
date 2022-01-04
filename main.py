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
#data_to_use = spread.data_done_date
#print(data_to_use)
data_to_use = spread.dsp_and_redrc_df
print(data_to_use[1])

#patients who are new
#eventually this will be updated and not relevant. 
new_patients = []
pre_existing_patients = []

#create the user class
#import user Class Object 
em = input("enter email please ")
pw = input("enter pword")
user = userClass.User(em, pw)
driver = webdriver.Chrome(executable_path=r'C:\Users\RRushton\Desktop\chromedriver.exe')

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

    for key in data_to_use: 
        #just for testing purposes
        if key > 10: 
            break


        given_name = data_to_use[key]['GIVEN_NAME_x']   
        surname = data_to_use[key]['FAMILY_NAME_x']
        DOB = data_to_use[key]['DATE_OF_BIRTH']
        gender = data_to_use[key]['GENDER_x']
        medicare = data_to_use[key]['MEDICARE_NUMBER']
        adress_1 = data_to_use[key]['HOME_ADDRESS_LINE_1_x'] 
        suburb = data_to_use[key]['HOME_SUBURB_TOWN_x']
        postcode = data_to_use[key]['HOME_POSTCODE_x']
        patient = patientClass.p_basic(given_name, surname, DOB, gender, medicare, adress_1,suburb, postcode)

        #now iterate through the dictionary
        #if the patient is now then register patient. 
        #if the patient exists already then add tp patient exists_dict
        try:
            WebDriverWait(driver,timeout=5).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))

            exisiting_patient_button = driver.find_element_by_link_text("Existing Assessment Patients")
            exisiting_patient_button.click()

            first_name_input = driver.find_element_by_id('firstName')
            last_name_input = driver.find_element_by_id('lastName')
            first_name_input.send_keys(given_name)
            last_name_input.send_keys(surname)
            search_button = driver.find_element_by_class_name('btn.btn-dark')
            search_button.click()



            try:
                #check if no results pop up. 
                new_patient_text = driver.find_element_by_xpath("//*[contains(text(), 'No results.')]").is_displayed()
                print("new patient")
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")
                #add to new patient key. 
                new_patients.append(data_to_use[key])
                print(new_patients)
            
            except Exception as e:
                #print(e)
                print("Prexisting")
                driver.get("https://app.respiratoryclinic.com.au/dashboard/")
                pre_existing_patients.append(data_to_use[key])
                
        except Exception as e:
            print(e)
            print("an error has occured in load this patient")
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")


    #once i've done this I need to take the list of dictionaries and go through
    #and register them. 
    #for el in range(len(new_patients)): 
        #print(new_patients[el]['GIVEN_NAME_x'])
    new_assesment_patient()
      




def new_assesment_patient():

    for el in range(len(new_patients)):
        try:
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")
            given_name = new_patients[el]['GIVEN_NAME_x'] 
            surname = new_patients[el]['FAMILY_NAME_x']
            date_of_birth = new_patients[el]['DATE_OF_BIRTH']
            gender = new_patients[el]['GENDER_x']
            medicare = new_patients[el]['MEDICARE_NUMBER']
            address1 = new_patients[el]['HOME_ADDRESS_LINE_1_x'] 
            suburb = new_patients[el]['HOME_SUBURB_TOWN_x']
            postcode = new_patients[el]['HOME_POSTCODE_x']
            patient = patientClass.p_basic(given_name, surname, date_of_birth, gender, medicare, address1,suburb, postcode)
        except Exception as e: 
            print(e)
            
        
        try:
            new_assesment_patient_button = driver.find_element_by_link_text("New Assessment Patient")
            new_assesment_patient_button.click()
        except Exception as e: 
            print(e)

        #get web stuff and upload it 
        try:
            name_field = driver.find_element_by_id('patient_firstName')
            name_field.send_keys(patient.name)


            #surname_field = 
            #referral_field = 
            #dob_field = 
            #gender_field = 
            #atsi_field = 
            #medicare_field = 
            #adress_1_field = 
            #suburb_field
            #state_field 
            #postcode_field 
            #emergency_field 
            #country_birth_field = 
            #at_home_language_field = 
            #symptoms_field = 


        except Exception as e: 
            print(e)
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")








    



automate()










































'''
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
    print(\'''
    Have your auth ready
    Have your auth ready
    Have your auth ready
    Have your auth ready
    \''')
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

        

        
       
    

    
automate(data_to_use,  ss)

'''




