# testauto
a python script to automate the uploading of testing results. 


# Libraries being Used 

Beautiful Soup 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

CSV Module Python 
https://docs.python.org/3/library/csv.html

Selenium 
https://selenium-python.readthedocs.io/installation.html


# A rough working outline of how the project will work. 
The script starts. 
The script loads the excel data and gets it ready to go. 
Username information is entered
The script logs me in 
the script waits for me to enter authenticator password. 
The script then logs me in to the main page. 
The script then commences uploading the data. 
It checks whether or not the patient is existing. If the patient exists it executes that work flow. 
If the patient doesn't exist then it executes the other work flow. 

things to match are DOB, GENDER



##check whether the patient is existing or not 
we are crrently only going to check for existing ones. 
we will then write to file the ones who are 

#########################
Need to vectorize the comparison function for the spreadsheets. 
Currently huge performance issues. 
Normal for pandas. 
Steps: 
    Define the comparison function sperately and then call it in the creataion of 
    Individual columns for the usble spreadsheet. 