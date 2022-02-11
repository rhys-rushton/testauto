# Automation Tool for Uploading Vaccination Data for COVID-19 (AUSTRALIA)
This is a python cli application that enables users to automate the uploading of data to the Australian Government's Respiratory Clinic app. 
In order to use this app. you will need to be a registered user on the government respiratory clinic app. and you will also need access to the relevant patient
management system for sourcing data. The two data sources I have been using is Aspen Medical's Rhino app and Zedmed. 
This script can automate the registering of patients who have been tested, the uploading of their pcr test encounter and also the follow up for those patients who received
a negative result. This script will also pick up on any patients who may be duplicates. 

## Table of Contents 
- How to run and install
- How to use
- Dependencies
- Checkinf for duplicates

## How to Run and Install
This autmation tool requires you to have [Python](https://www.python.org/) installed. You will also need a wedriver for whatever browser it is that you are using. 
You will also need to install some dependenices. 

```sh
pip install pandas
pip install selenium
```
The inputs and outputs are configured to be specific to a certain computer, these will need to be changed if you move location. 

The data inputs for uploading patient tests encounters and registering goes in the 'csvOperations' folder. The data outputs  go in the 'csv' folder.
Further, the data outputs for the follow up process go in the 'follow_up_output' folder. 

All csv files are never uploaded to github because of data sensitivity. 

#### Checking for Duplicates 

Make sure that you have the correct data source available for the script. The script you will need is the aspen medical record of all of the tests. 

![Checking for Duplicates](.\gifs\duplicates.gif)

## Dependencies
- Python
- Selenium
- Pandas
- Driver for whatever browser you're using



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

https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
https://stackoverflow.com/questions/24870953/does-pandas-iterrows-have-performance-issues
https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#essential-basic-functionality
https://stackoverflow.com/questions/37113173/compare-2-excel-files-using-python

https://datascience.stackexchange.com/questions/58546/valueerror-the-truth-value-of-a-dataframe-is-ambiguous-use-a-empty-a-bool


