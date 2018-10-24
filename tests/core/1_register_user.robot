*** Settings ***
Library   OperatingSystem
Test Setup  Clear database
Resource   resources.txt


*** Test Cases ***
First Installation
  [Documentation]   Register an administrator on freshed installation
  Open Browser To Login Page 
  Title Should Be     Installer Libreosteo
  Click RegisterUser
  Input Username    test 
  Input Password1   test
  Input Password2   test
  Submit Credentials
  Login Page Should Be Open
  [Teardown]  Close Browser

*** Keywords ***
Click RegisterUser
  Click Button  register

Input Username
  [Arguments]   ${username}
  Input Text  name:username  ${username}

Input Password1
  [Arguments]   ${password}
  Input Text  password1  ${password}

Input Password2
  [Arguments]   ${password}
  Input Text  password2  ${password}

Submit Credentials
  Click Button  login 

Login Page Should Be Open
  Title Should Be  Identifiez-vous sur Libreosteo 

Clear database
  Remove File   db.sqlite3
  Run   python ./manage.py migrate
