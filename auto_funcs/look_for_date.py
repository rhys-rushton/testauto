# this function looks for either the encounter date or the patient's date of birth 
# so that we can avoid duplicate encounters. 
def look_for_date (date_string, driver):
    print('looking for date')
    date_present = False
    for div in driver.find_elements_by_class_name('card.my-4.patient-card.assessment-reg-patient'):
        try: 
            assert date_string in div.get_attribute('innerHTML')
            date_present = True
            break
            
        except:
            continue
    
    return date_present
