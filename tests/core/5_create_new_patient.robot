# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt

*** Variables ***
${LAST_NAME}        Tester
${FIRST_NAME}       Robot
${EMAIL}            test@robot.com
${BIRTH_DAY}        12
${BIRTH_MONTH}      12
${BIRTH_YEAR}       1972
&{COOKIE}

*** Test Cases ***
Create New Patient  
  [Documentation]   Create a new patient
  Open Browser To Login Page 
  Title Should Be     Identifiez-vous sur Libreosteo
  Login with      test   test
  Title Should Be     Libreosteo
  ${COOKIE} =         Get Cookie      sessionid
  Element Should Not Be Visible     class:alert-danger
  Create Patient
  Create Patient Duplicate

Edit The New Patient                          
  Go To                           ${ROOT_URL}
  ${COOKIE} =         Get Cookie      sessionid
  Wait That Page Is Ready
  Wait Until Element Contains     jquery:div[class~="chat-body"]>div[class~="header"]            ${LAST_NAME} ${FIRST_NAME}      10
  Click Element                   jquery:div[class~="chat-body"]>div[class~="header"]:contains("${LAST_NAME} ${FIRST_NAME}")
  Wait Until Element Contains     jquery:h1.page-header         ${LAST_NAME}
  Wait That Page Is Ready 
  Check That Url Is               ${ROOT_URL}/#/patient/1
  [Documentation]                 Edit the general information
  Click Button                    jquery:button:contains("Éditer")
  Check That Form Has             Supprimer 
  Check That Form Has             Fin d'édition
  Check That Form Does Not Have   Éditer
  Select From List By Label       sex                     Masculin  
  Input Text                      street                  10 rue du Moulin
  Input Text                      address_complement      Appt A
  Input Text                      zipcode                 32110
  Input Text                      city                    Le Vigen 
  Input Text                      phone                   01 01 01 01 01 
  Input Text                      mobile                  07 07 07 07 07 
  Input Text                      email                   tester@robot.fr 
  Select From List By Label       laterality              Gaucher 
  Select Checkbox                 smoker
  Input Text                      job                     Antiquaire
  Input Text                      hobbies                 Ski, Roller, Musique
  Input Text                      important_info          WARNING
  Input Text                      current_treatment       Traitement H2O
  Click Button                    jquery:button:contains("Fin d'édition")
  Wait That Page Is Ready
  Check That Form Has             Supprimer 
  Check That Form Has             Éditer  
  Check That Form Does Not Have   Fin d'édition
  Click Element                   history 
  Check That Form Has             Éditer
  Check That Form Does Not Have   Fin d'édition
  Check That Form Does Not Have   Supprimer 
  Click Button                    jquery:button:contains("Éditer")
  Check That Form Has             Fin d'édition
  Check That Form Does Not Have   Éditer
  Check That Form Does Not Have   Supprimer
  Input Text                      surgical_history        Surgical history 
  Input Text                      medical_history         Medical History 
  Input Text                      family_history          Family History 
  Input Text                      trauma_history          Trauma history 
  Click Element                   medicalreports 
  Check That Form Has             Éditer
  Check That Form Does Not Have   Fin d'édition
  Check That Form Does Not Have   Supprimer 
  Click Button                    jquery:button:contains("Éditer")
  Input Text                      medical_reports         Medical Reports
  Click Button                    jquery:button:contains("Fin d'édition")
  Choose File                     addDocumentMedicalReport     ${CURDIR}/resources.txt   
  Wait Until Element Is Enabled   jquery:button.btn.label.label-info 
  Wait Until Element Contains     jquery:div.form-group.document_create       resources.txt
  Input Text                      jquery:input[placeholder~="Titre"]          Licence Libreosteo 
  Input Text                      jquery:input[placeholder~="Date"]:visible   10/01/2012
  Input Text                      jquery:p.help-block ~ div                   Licence GNU GPLv3
  Click Element                   jquery:button.btn.label.label-info
  Check Rest Patient              ${COOKIE.value}

*** Keywords ***
Create Patient
  Click Element                   jquery:a:contains("Nouveau patient")
  Check That Url Is               ${ROOT_URL}/#/addPatient
  Wait That Page Is Ready
  Wait Until Element Contains     jquery:h1.page-header         Nouveau patient 
  Input Text                      family_name                   ${LAST_NAME}
  Input Text                      first_name                    ${FIRST_NAME}
  Input Text                      jquery:input.dd               ${BIRTH_DAY}
  Input Text                      jquery:input.mm               ${BIRTH_MONTH}
  Input Text                      jquery:input.yy               ${BIRTH_YEAR}
  Wait Until Element Is Enabled   jquery:button.btn.btn-primary 
  Click Button                    jquery:button.btn.btn-primary 
  Wait Until Element Contains     jquery:h1.page-header         ${LAST_NAME}
  Wait That Page Is Ready 
  Check That Form Has             Éditer
  Check That Form Has             Supprimer
  Check That Form Does Not Have   Fin d'édition
  Check That Url Is               ${ROOT_URL}/#/patient/1

Wait That Page Is Ready
  Wait Until Element Is Not Visible     loading-bar

Create Patient Duplicate
  Click Element                   jquery:a:contains("Nouveau patient")
  Wait Until Element Contains     jquery:h1.page-header         Nouveau patient 
  Input Text                      family_name                   ${LAST_NAME}
  Input Text                      first_name                    ${FIRST_NAME}
  Input Text                      jquery:input.dd               ${BIRTH_DAY}
  Input Text                      jquery:input.mm               ${BIRTH_MONTH}
  Input Text                      jquery:input.yy               ${BIRTH_YEAR}
  Wait Until Element Is Enabled   jquery:button.btn.btn-primary 
  Click Button                    jquery:button.btn.btn-primary 
  Wait Until Element Is Enabled   jquery:div.growl-item
  Element Should Be Visible       jquery:div.growl-item.alert.alert-danger
  ${error}=                       Get Text                      jquery:div.growl-item.alert.alert-danger 
  Should Contain                  ${error}                      Ce patient existe déjà

Check That Url Is 
  [Arguments]                     ${url}
  ${current_url}=                 Get Location
  Should Be Equal                 ${current_url}      ${url}

Check That Form Has
  [Arguments]                     ${action_name}
  Page Should Contain Button      jquery:button:contains(${action_name})

Check That Form Does Not Have
  [Arguments]                     ${action_name}
  Page Should Not Contain        jquery:button:contains(${action_name}) 

Check Rest Patient 
  [Arguments]     ${session_token}
  ${session_cookie}   Create Dictionary   sessionid=${session_token}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request   restapi     /api/patients/1
  Should Be Equal As Numbers      ${resp.json()['id']}                    1
  Should Be Equal As Strings      ${resp.json()['birth_date']}            1972-12-12 
  Should Be Equal As Strings      ${resp.json()['family_name']}           Tester 
  Should Be Equal As Strings      ${resp.json()['original_name']}         ""
  Should Be Equal As Strings      ${resp.json()['first_name']}            Robot 
  Should Be Equal As Strings      ${resp.json()['address_street']}        10 rue du Moulin 
  Should Be Equal As Strings      ${resp.json()['address_complement']}    Appt A 
  Should Be Equal As Strings      ${resp.json()['address_zipcode']}       32110 
  Should Be Equal As Strings      ${resp.json()['address_city']}          Le Vigen 
  Should Be Equal As Strings      ${resp.json()['email']}                 tester@robot.fr 
  Should Be Equal As Strings      ${resp.json()['phone']}                 01 01 01 01 01 
  Should Be Equal As Strings      ${resp.json()['mobile_phone']}          07 07 07 07 07 
  Should Be Equal As Strings      ${resp.json()['job']}                   Antiquaire 
  Should Be Equal As Strings      ${resp.json()['hobbies']}               Ski, Roller, Musique<br>
  Should Be Equal As Boolean      ${resp.json()['smoker']}                True
  Should Be Equal As Boolean      ${resp.json()['laterality']}            L 


