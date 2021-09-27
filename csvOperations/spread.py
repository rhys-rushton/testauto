import pandas as pd

dfRC = pd.read_csv(r'./REDRC.csv', header=0)
dfDPS = pd.read_csv(r'./DSPatients.csv', header =0, encoding = 'cp1252')
finalData = pd.DataFrame(columns=["FILE_NUMBER","GIVEN_NAME","FAMILY_NAME","HOME_ADDRESS_LINE_1","HOME_ADDRESS_LINE_2","HOME_SUBURB_TOWN","HOME_POSTCODE","DOB","GENDER"])
finalData.to_csv('finalData.csv')


dfRCTest = dfRC.head()
dfDPSTest = dfDPS.head()

#print(dfRCTest)

#with open("./REDRC.csv") as f: 
    #print(f)
#for ind, row in dfDPSTest.iterrows():
    #print(type(row[33]))

#for ind, row in dfRCTest.iterrows():
    #print(type(row[1]))

for ind, row in dfRCTest.iterrows(): 
    for dpsInd, dpsRow in dfDPS.iterrows():

        if (row[1] == dpsRow[33]):
            fileNumber = row[1]
            
            #print(row[1])
            #print(dpsRow[33])
                
                #print(row[1])  
                #print(dpsRow[33])
        
       
   

    

        #print(10000 + ind,row)
        #print(2000 + dpsInd, dpsRow)
