# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt
Resource   keywords/create_patient.robot

*** Variables ***
${LAST_NAME}        Picard 
${FIRST_NAME}       Jean-Luc
${EMAIL}            jean-luc.picard@starfleet.com
${BIRTH_DAY}        13
${BIRTH_MONTH}      07 
${BIRTH_YEAR}       1935 
${ID_PATIENT}       1
${ORIGINAL_NAME}    Dupont
${ORIGINA_NAME_HEADER}    (${ORIGINAL_NAME})
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
  Set Selenium Speed              0
  ${COOKIE} =         Get Cookie      sessionid
  Wait That Page Is Ready
  Wait Until Element Contains     jquery:div[class~="chat-body"]>div[class~="header"]            ${LAST_NAME} ${FIRST_NAME}      10
  Click Element                   jquery:div[class~="chat-body"]>div[class~="header"]:contains("${LAST_NAME} ${FIRST_NAME}")
  Wait Until Element Contains     jquery:h1.page-header         ${LAST_NAME}
  Wait That Page Is Ready 
  Check That Url Is               ${ROOT_URL}/#/patient/${ID_PATIENT}
  [Documentation]                 Edit the general information
  Click Button                    jquery:button:contains("Éditer")
  Check That Form Has             Supprimer 
  Check That Form Has             Fin d'édition
  Check That Form Does Not Have   Éditer
  Input Text                      original_name           dupont
  Select From List By Label       sex                     Masculin  
  Input Text                      street                  4 rue de l'Angle
  Input Text                      address_complement      Appt A
  Input Text                      zipcode                 70190 
  Input Text                      city                    La Barre 
  Input Text                      phone                   01 01 01 01 01 
  Input Text                      mobile                  07 07 07 07 07 
  Input Text                      email                   ${EMAIL} 
  Select From List By Label       laterality              Gaucher 
  Select Checkbox                 smoker
  Input Text                      job                     Navigateur 
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
  Wait Until Element Is Not Visible     jquery:button.btn.label 
  Check Rest Patient              ${COOKIE.value}
  Check Rest Patient Documents    ${COOKIE.value}

*** Keywords ***
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

Check Rest Patient 
  [Arguments]     ${session_token}
  ${session_cookie}   Create Dictionary   sessionid=${session_token}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request   restapi     /api/patients/1
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Numbers      ${resp.json()['id']}                    1
  Should Be Equal As Strings      ${resp.json()['birth_date']}            1935-07-13 
  Should Be Equal As Strings      ${resp.json()['family_name']}           ${LAST_NAME} 
  Should Be Equal As Strings      ${resp.json()['original_name']}         Dupont
  Should Be Equal As Strings      ${resp.json()['first_name']}            ${FIRST_NAME} 
  Should Be Equal As Strings      ${resp.json()['address_street']}        4 rue de l'Angle 
  Should Be Equal As Strings      ${resp.json()['address_complement']}    Appt A 
  Should Be Equal As Strings      ${resp.json()['address_zipcode']}       70190 
  Should Be Equal As Strings      ${resp.json()['address_city']}          La Barre 
  Should Be Equal As Strings      ${resp.json()['email']}                 jean-luc.picard@starfleet.com 
  Should Be Equal As Strings      ${resp.json()['phone']}                 01 01 01 01 01 
  Should Be Equal As Strings      ${resp.json()['mobile_phone']}          07 07 07 07 07 
  Should Be Equal As Strings      ${resp.json()['job']}                   Navigateur 
  Should Be Equal As Strings      ${resp.json()['hobbies']}               Ski, Roller, Musique<br>
  Should Be True                  ${resp.json()['smoker']}
  Should Be Equal As Strings      ${resp.json()['laterality']}            L 

Check Rest Patient Documents 
  [Arguments]     ${session_token}
  ${session_cookie}   Create Dictionary   sessionid=${session_token}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request     restapi     /api/patient-documents/1
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Numbers      ${resp.json()['patient']}               1 
  Should Be Equal As Numbers      ${resp.json()['attachment_type']}       5 
  Should Be Equal As Strings      ${resp.json()['document']['title']}     Licence Libreosteo 
  Should Be Equal As Strings      ${resp.json()['document']['notes']}     Licence GNU GPLv3<br>
  Should Be Equal As Strings      ${resp.json()['document']['document_date']}   2012-01-10 
  Should Contain                  ${resp.json()['document']['document_file']}         http://localhost:8085/files/documents/resources  
