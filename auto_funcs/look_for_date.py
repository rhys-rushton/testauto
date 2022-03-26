# this function looks for either the encounter date or the patient's date of birth 
# so that we can avoid duplicate encounters. 
import time
def look_for_date (date_string, driver):
    print('looking for date')
    date_present = False
    for div in driver.find_elements_by_class_name('card.my-4.patient-card.assessment-reg-patient'):
        
        if date_string in div.get_attribute('innerHTML'):
            print('date here')
            date_present = True
            #print(div.get_attribute('innerHTML'))
            break

    return date_present


#this will select element in div with relement div. 
def find_date_click (date_string, driver):

    print('getting div to add encounter to.')
    
    for div in driver.find_elements_by_class_name('card.my-4.patient-card.assessment-reg-patient'):
       
        if date_string in div.get_attribute('innerHTML'):
        #print("We here" )
        #print(div.get_attribute('innerHTML'))
        #time.sleep(20)
            new_encounter_button = div.find_element_by_class_name('btn.btn-primary.mr-4')
            new_encounter_button.click()
            #break
            return 
        print('hey')
            
            
       
 


