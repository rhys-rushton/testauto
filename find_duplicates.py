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
from csvOperations.fields import fields as field_data
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login
from auto_funcs.symptoms import symptoms

possible_duplicates = []


data_to_use = spread.rhino_data_dup_check

def main ():

    driver = login()

    for key in data_to_use:
        #if key > 10:
            #break
        driver.get("https://app.respiratoryclinic.com.au/dashboard/")
        name = data_to_use[key]['first_name']
        last_name = data_to_use[key]['last_name']

        existing_assement_button = driver.find_element_by_link_text('Existing Assessment Patients')
        existing_assement_button.click()

        given_name_field = driver.find_element_by_id('firstName')
        surname_field = driver.find_element_by_id('lastName')

        given_name_field.send_keys(name)
        surname_field.send_keys(last_name)

        search_button = driver.find_element_by_class_name('btn.btn-dark')
        search_button.click()

        try: 
            assert driver.find_element_by_xpath("//*[contains(text(), 'Potential Duplicate found')]").is_displayed()
            possible_duplicates.append(data_to_use[key])
            print('duplicate')

        except:
            
            print('No duplicate')

main()

#write errors to csv
with open(r'H:\testauto\csv\test_duplicates\test_duplicates.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_data, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(possible_duplicates)



