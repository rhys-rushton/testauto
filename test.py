from classes import userClass, patientClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time as times
#from csvOperations import spread
import csv
from random import randrange
from csvOperations.fields import fields as field_data
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login
from auto_funcs.symptoms import symptoms


driver = login()
surname = 'Doe'
(driver.find_element_by_link_text('Existing Assessment Patients')).click()
(driver.find_element_by_id('lastName').send_keys(surname))
search_button = driver.find_element_by_class_name('btn.btn-dark')
search_button.click()
assert driver.find_element_by_xpath("//*[contains(text(), 'Potential Duplicate found')]").is_displayed()

