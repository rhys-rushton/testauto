#want to be able to select patients within a specific date range. 
#then i want to search patient, verify i have correct one by looking at date of birth
#then I want to loop through the encounters they have and if they have encounters then I want to add a follow up.
#then I want to write this patient file to a csv file. 
# don't neccesarily want to drop duplicates. 

from auto_funcs.login import login

login()