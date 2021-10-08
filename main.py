#import the user class object
from classes import userClass, patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from csvOperations import spread


data_to_use = spread.data_done

print(data_to_use[0])


#create the user class
#import user Class Object 
#em = input("enter email please ")
#pw = input("enter pword")
#user = userClass.User(em, pw)

    
def login():
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

    ##need to change this so I wait for user to click login. 
    #define a function so the webdrive waits for user 
    try:
        WebDriverWait(driver,timeout=30).until(EC.url_contains("https://app.respiratoryclinic.com.au/dashboard/"))
        print("You're through")
    except:
        print("You did not login succesfully")
        return 
    

    time.sleep(10)
    

    
#LOGIN FUNCTION CURRENTLY CHILLING
#login()


def make_patient (patient_dict, patient_class):
    
    for key in patient_dict:
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
        print(patient.first_name + patient.last_name + gender)

    


##we want to inititialise each value in the spreadsheet in the patient class
#then do a series of steps where we go through the website -> patient is either existing or not. 
##then we want to record the outcome of these steps 

make_patient(data_to_use, patientClass)
