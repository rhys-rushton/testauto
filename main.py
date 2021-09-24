#import the user class object
from classes import userClass, patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from csvOperations import csv






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


#PANDAS READING CSV STUFF
#<----------------------------------------->
#READ CSV + SKIP HEADER
df = pd.read_csv(r'./csvOperations/REDRC.csv', header=0)
#print(df.GIVEN_NAME)
#SELECT RELEVANT COLOUMNS
df_data =df[["FILE_NUMBER","GIVEN_NAME","FAMILY_NAME","HOME_ADDRESS_LINE_1","HOME_ADDRESS_LINE_2","HOME_SUBURB_TOWN","HOME_POSTCODE"]]
#JUST FOR TESTING PURPOSES (ONLY USE THE FIRST FIVE)
df_test = df_data.head()

##Iterate through the csv object
##then return values. We will save these in the
##patient object

for ind,row in df_test.iterrows():
    #patient = ind, row[0],row[1]
    #print(patient)
    file = [ind, row [0]]
    givenName = [ind, row[1]]
    familyName = [ind, row[2]]
    homeOne = [ind, row[3]]
    homeTwo = [ind, row[4]]
    suburb = [ind, row[5]]
    postCode = [ind, row[6]]
    patient = patientClass.Patient(file,givenName,familyName,homeOne,homeTwo,suburb,postCode)
    print(patient.giveName)



    #print(ind,row[0] + row[1])
    #print(ind,row[1])
    #print(ind,row[2])
    #print(ind,row[3])
    #print(ind,row[4])
    #print(ind,row[5])


