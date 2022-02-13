import pandas as pd
from csvOperations import spread

#here we are checking for patients who have been in more than once to the clinic
#for a covid 19 test
# what we will keep all patients in the billing item data who appear more than once
# then we will compare this with the rhino app data
# the patients who have an encounter will be dropped. 
# the patients who do not have an encounter are once that we want to keep. 
# 

data = spread.prexisting_df_copy
data[data.duplicated(keep = False)]

print(data)