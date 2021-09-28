import pandas as pd

dfRC = pd.read_csv('./REDRC.csv', header=0)
dfDPS = pd.read_csv('./DSPatients.csv', header =0, encoding = 'cp1252')
finalData = pd.DataFrame(columns=["FILE_NUMBER","GIVEN_NAME","FAMILY_NAME","HOME_ADDRESS_LINE_1","HOME_ADDRESS_LINE_2","HOME_SUBURB_TOWN","HOME_POSTCODE","DOB","GENDER","TITLE"])
unMatched = pd.DataFrame(columns=["FILE_NUMBER"])


dfRCTest = dfRC.head()
dfDPSTest = dfDPS.head()

def compareSheets (rc, dps):
    if (rc == dps):
        print("Match")
    else: 
        print("No Match")
        
compareSheets(dfRCTest["FILE_NUMBER"], dfDPSTest["FILE_NUMBER"])

#for ind, row in dfRC.iterrows(): 
    #for dpsInd, dpsRow in dfDPS.iterrows():
        #if (row[1] == dpsRow[33]):
            #fileNumber = row[1]
            #print(ind,row)
            #finalData.loc[ind,"FILE_NUMBER"] = row["FILE_NUMBER"]
            #finalData.loc[ind,"GIVEN_NAME"] = row["GIVEN_NAME"]
            #finalData.loc[ind,"FAMILY_NAME"] = row["FAMILY_NAME"]
            #finalData.loc[ind,"HOME_ADDRESS_LINE_1"] = row["HOME_ADDRESS_LINE_1"]
            #finalData.loc[ind,"HOME_ADDRESS_LINE_2"] = row["HOME_ADDRESS_LINE_2"]
            #finalData.loc[ind,"HOME_SUBURB_TOWN"] = row["HOME_SUBURB_TOWN"]
            #finalData.loc[ind,"HOME_POSTCODE"] = row["HOME_POSTCODE"]
            #finalData.loc[ind, "DOB"] = dpsRow["DATE_OF_BIRTH"]
            #finalData.loc[ind,"GENDER"] = dpsRow["GENDER"]
            #finalData.loc[ind,"TITLE"] = row["TITLE"]
        #else:
            #unMatched.loc[ind, "FILE_NUMBER"] = row["FILE_NUMBER"]
           
            #pass 
            
            
#print(finalData)
            


#print(finalData.head())
#finalData.to_csv('finalData.csv')
#print(unMatched)