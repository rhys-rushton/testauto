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
- Checking for duplicates

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

```sh
python find_duplicates.py
```
Enter your emaila nd 2FA code and then the script will run. 

![Checking for Duplicates](duplicates.gif)

The above gif is instructive for all other proccesses that need to be run, so I will only give the relevant commands for further processes. The password and email will not be shown on the CLI and I couldn't demo uploading data as this is 
sensitive. But once you have put in your 2FA code the script will run. 

#### Follow-ups

```sh
python follow_up.py
```
Then enter your email and password. 
On completion the results of the script will be outputed in the 'follow_up_output' folder.  

#### Registering patients and adding encounters. 
It is important to note that there are two scripts here. One script is for patients who have been tests before, whereas the other script is for new patients. 
To run the script for new patients:

```sh
python new_patients_final.py
```
For existing patients: 

```sh
python existing_patients.py
```

The process for username and password is the same as the gif above. Output of this process can be found in the 'csv' folder. 

## Dependencies
- Python
- Selenium
- Pandas
- Driver for whatever browser you're using



