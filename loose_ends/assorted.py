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

###############
###NEED TO CHANGE BELOw[remove 0]
#data_to_use = spread.data_done_date

#data_to_use = spread.dsp_and_redrc_df

data_to_use = spread.new_patients


#patients who are new
#eventually this will be updated and not relevant. 
new_patients = []
pre_existing_patients = []
patient_new_error = []
patient_new_success = []

#create the user class
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
        #if key > 10: 
            #break
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
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
                continue
            
            except Exception as e:
                print('Potentially prexisting')

            try: 
                if DOB[0] == '0' and DOB[3] == '0':
                    DOB = DOB[1:3] + DOB[4:]

                elif DOB[0] == '0':
                    DOB = DOB[1:]

                elif DOB[0] != '0' and DOB[3] == '0':
                    DOB = DOB[0:3] + DOB[4:]

                assert DOB in driver.page_source
                pre_existing_patients.append(data_to_use[key])
                continue

            except:
                print('Patient doesnt exist')
                new_patients.append(data_to_use[key])

        except Exception as e:
            print(e)
            print("an error has occured in load this patient")
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")

    #once i've done this I need to take the list of dictionaries and go through
    #and register them. 
    fields = ['FILE_NUMBER', 'HOME_ADDRESS_LINE_2_x', 'HOME_PHONE_x', 'MEDICARE_NUMBER', 'MAILING_ADDRESS_LINE_2_y', 'GENDER_x', 'email_ADDRESS', 'HOME_ADDRESS_LINE_1_x', 'MAILING_ADDRESS_LINE_1_y', 'DATE_OF_BIRTH', 'FAMILY_NAME_x', 'PATIENT_ID', 'HOME_SUBURB_TOWN_x', 'MEDICARE_NUMBER_EXPIRY', 'GIVEN_NAME_x', 'MEDICARE_BASE_NUMBER', 'LAST_IN_x', 'HOME_POSTCODE_x', 'AGE_x']

    with open(r'H:\testauto\csv\pre_existing_patients.csv','w', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(pre_existing_patients)

    #new_assesment_patient(fields)
      



#this is the function where we register the new patient. 
def new_assesment_patient(fields):

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
            print("Error in creating patient obj")
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

            surname_field = driver.find_element_by_id('patient_lastName')  
            surname_field.send_keys(patient.surname)

            referral_field = Select(driver.find_element_by_id('patient_referralSource_choice'))
            referral_field.select_by_visible_text('General Practice website')

            dob_field = driver.find_element_by_id('patient_dateOfBirth')
            dob_field.send_keys(patient.DOB)

            gender_field = Select(driver.find_element_by_id('patient_gender'))
            
            if new_patients[el]['GENDER_x'] == '':
                 gender_field.select_by_visible_text('Not Stated')
            elif new_patients[el]['GENDER_x'] == 'M':
                gender_field.select_by_visible_text('Male')
            elif new_patients[el]['GENDER_x'] == 'F':
                gender_field.select_by_visible_text('Female')

            atsi_field = Select(driver.find_element_by_id('patient_indigenousStatus'))
            atsi_field.select_by_visible_text('Not stated')

            #enter medicare number
            medicare_field = Select(driver.find_element_by_id('patient_typeOfIdProvided'))
            if new_patients[el]['MEDICARE_NUMBER'] == '':
                medicare_field.select_by_visible_text('No - Other ID sighted')
            elif new_patients[el]['MEDICARE_NUMBER'] != '': 
                medicare_field.select_by_visible_text('Yes - Please enter Medicare Card number')
                patient_medicare_num = driver.find_element_by_id('patient_medicareNumber')
                patient_medicare_ref = driver.find_element_by_id('patient_medicareReferenceNumber')
                patient_medicare_num.send_keys(patient.medicare[0:10])
                patient_medicare_ref.send_keys(patient.medicare[10])
            
            adress_line_1 = driver.find_element_by_id('patient_addressLine1')
            adress_line_1.send_keys(patient.address)

            suburb_field = driver.find_element_by_id('patient_suburb')
            suburb_field.send_keys(patient.suburb)

            postcode_field = driver.find_element_by_id('patient_postcode')
            postcode_field.send_keys(patient.post_code)

            state_field = Select(driver.find_element_by_id('patient_state'))
            if(patient.post_code[0]) == '2': 
                state_field.select_by_visible_text('NSW')

            elif(patient.post_code[0]) == '3':
                state_field.select_by_visible_text('VIC')

            elif(patient.post_code[0]) == '4':
                state_field.select_by_visible_text('QLD')

            elif(patient.post_code[0]) == '5':
                state_field.select_by_visible_text('SA')

            elif(patient.post_code[0]) == '6':
                state_field.select_by_visible_text('WA')

            elif(patient.post_code[0]) == '7':
                state_field.select_by_visible_text('TAS')

            elif(patient.post_code[0]) == '0':
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

            #click the save button for potential duplicates, as they are registered
            #for vax. 
            try: 
                potential_dup = driver.find_element_by_class_name('alert.alert-warning')
                
                save_button.click()
                patient_new_success.append(new_patients[el])  
                times.sleep(1)
                #new_patient_add_encounter(new_patient_data, key)
              

            except:
                if new_assesment_patient_button.is_displayed():
                    patient_new_success.append(new_patients[el])
                    #new_patient_add_encounter(new_patient_data, key)
                   
                else:
                    patient_new_error.append(new_patients[el])
                    times.sleep(1)

            #add the encounter for the patient
            #new_patient_add_encounter(new_patient_data, key)


            #patient_new_success.append(new_patients[el])
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")

            #times.sleep(1)

        except Exception as e: 
            print("Error in loading patient data")
            times.sleep(1)
            print(e)
            patient_new_error.append(new_patients[el])
            driver.get("https://app.respiratoryclinic.com.au/dashboard/")

    #write to the csvs
    with open(r'H:\testauto\csv\new_patient_rego_opt\new_succes.csv', 'w', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(patient_new_success)

    with open(r'H:\testauto\csv\new_patient_rego_opt\new_error.csv', 'w', newline='') as f: 
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(patient_new_error)
          



automate()

print("All finished")



#when adding a new patient what you want to do is after you register them click add encounter which is what should pop up after they've been registered. 




































