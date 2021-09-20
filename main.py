#import the user class object
from classes import userClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time




#create the user class
#import user Class Object 

em = input("enter email please ")
pw = input("enter pword")
user = userClass.User(em, pw)

    
def login():
    driver = webdriver.Chrome()
    driver.get("https://app.respiratoryclinic.com.au/login")
    # username id="inputUsername"
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
    #authInput.send_keys("hey")
    print(bool(authInput.get_attribute("value")))
    




    time.sleep(5)
    
    

login()



