#initialize the patient classs object
class Patient(): 
    def __init__(self, encounter_date, encounter_time, encounter_id, first_name, last_name, DOB, age_at_presentation, gender, medicare, atsi, address, suburb, state, postcode, emergency, birth_country, language, symptoms, meds, specimen, diagnosis, outcome): 
        self.date = encounter_date
        self.time = encounter_time
        self.id = encounter_id
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.age_at_presentation = age_at_presentation
        self.gender = gender
        self.medicare = medicare
        self.atsi = atsi
        self.address = address
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.emergency = emergency
        self.birth_country = birth_country
        self.language = language
        self.symptoms = symptoms
        self.meds = meds
        self.specimen = specimen
        self.diagnosis = diagnosis
        self.outcome = outcome

#basic testing class
class patient():
    def __init__(self, name, surname, DOB, gender,medicare, address, suburb, post_code, date, error=''):
        self.name = name
        self.surname = surname
        self.DOB = DOB
        self.gender = gender
        self.medicare = medicare
        self.address = address
        self.suburb = suburb
        self.post_code = post_code
        self.date = date
        self.error = error


#follow up class
class patient_follow_up():
    def __init__(self, name, surname, DOB, encounter_id, encounter_date, outcome = ''):
        self.name = name 
        self.surname = surname
        self.DOB = DOB
        self.encounter_id = encounter_id
        self.encounter_date = encounter_date
        self.outcome = outcome 
        
