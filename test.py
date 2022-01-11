from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time as times
from datetime import datetime
from auto_funcs.date_string_zeroes import remove_zeroes
from auto_funcs.login import login




#login. 

def automate():
    driver = login()


 
    encounter_id = 'Rushton'
    encounter_date = '05/03/1961'
    
    encounter_date = remove_zeroes(encounter_date)
    #print(encounter_date)



    existing_assement_button = driver.find_element_by_link_text('Existing Assessment Patients')
    existing_assement_button.click()

    #encounter_id_field = driver.find_element_by_id('encounterId')
    encounter_id_field = driver.find_element_by_id('lastName')
    encounter_id_field.send_keys(encounter_id)

    search_button = driver.find_element_by_class_name('btn.btn-dark')
    search_button.click()



    el = driver.find_element_by_xpath(f"//*[contains(., '{encounter_date}')]")
 
    
    for div in driver.find_elements_by_class_name('card.my-4.patient-card.assessment-reg-patient'):
        try: 
            assert encounter_date in div.get_attribute('innerHTML')
            print(div.text)
            div.find_element_by_link_text('New Encounter').click()
            times.sleep(5)
            

        except:
            print('no')




    times.sleep(3)
    #assert encounter_date in driver.page_source
    
    



#automate()





