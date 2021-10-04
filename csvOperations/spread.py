import pandas as pd

dfRC = pd.read_csv('./REDRC.csv', header=0)
dfDPS = pd.read_csv('./DSPatients.csv', header =0, encoding = 'cp1252')
finalData = pd.DataFrame(columns=["FILE_NUMBER","GIVEN_NAME","FAMILY_NAME","HOME_ADDRESS_LINE_1","HOME_ADDRESS_LINE_2","HOME_SUBURB_TOWN","HOME_POSTCODE","DOB","GENDER","TITLE"])
#unMatched = pd.DataFrame(columns=["FILE_NUMBER"])
final =pd.DataFrame()

dfRCTest = dfRC.head()
dfDPSTest = dfDPS.head()

#A function to compare file numbers that are both in the rc and the dps information
def compareRcDPS (rcNum, dpsNum, rcFull, DPSFull):
    finalDataFileNumbs = []
    rcClinic = rcNum.tolist()
    dpsInfo = dpsNum.tolist()

    for n in rcClinic: 
        if n in dpsInfo:
            #print("Match")
            finalDataFileNumbs.append(n)
        else: 
            #print("No")
            continue
    
    fd = pd.DataFrame(finalDataFileNumbs, columns=["FILE_NUMBER"])

    #this is the data we are going to upload
    #we are checking that the list of file numbers in the final data column
    #is inside the rc clinic data. 
    upload = rcFull[rcFull["FILE_NUMBER"].isin(finalDataFileNumbs)] 
    supload = DPSFull[DPSFull["FILE_NUMBER"].isin(finalDataFileNumbs)]
    print(upload)
    print(supload)
    

    
  
 
        
compareRcDPS (dfRC["FILE_NUMBER"], dfDPS["FILE_NUMBER"],dfRC, dfDPS[['FILE_NUMBER' , 'GENDER', 'DATE_OF_BIRTH']])

#now we need a function to write the file numbers to the pandas final data data frame. 

##want to create a data frame with the final data file numbers as an index

    


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
            
            
#print(finalDataFileNumbs)

            


#print(finalData.head())
#finalData.to_csv('finalData.csv')
#print(unMatched)