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

    
def openBrowser():
    driver = webdriver.Chrome()
    driver.get("https://app.respiratoryclinic.com.au/login")
    # username id="inputUsername"
    userName = driver.find_element_by_id("inputUsername")
    userName.clear()
    userName.send_keys(user.email)
    time.sleep(5)
    
    

openBrowser()



