# -*- coding: robot -*-
*** Settings ***
Test Setup        Open session 
Test Teardown     Close session
Resource   resources.txt

*** Variables ***
${LAST_NAME}        Picard 
${FIRST_NAME}       Jean-Luc
${PATIENT_URL}      \#/patient/1
&{COOKIE}

*** Test Cases ***
Search For Patient
  Go To             ${ROOT_URL}
  ${COOKIE} =         Get Cookie      sessionid
  Input Text        jquery:div[class~="custom-search-form"]>input      ${LAST_NAME}
  Click Button      jquery:div[class~="custom-search-form"]>span>button
  Wait Until Element Contains           jquery:h3.page-header         ${LAST_NAME}
  Wait Until Page Contains Element      jquery:div[class~="search-entry"]>h4>a     
  Click Link                            jquery:div[class~="search-entry"]>h4>a
  Location Should Be                    ${ROOT_URL}/${PATIENT_URL}
  Wait Until Element Contains           jquery:h1.page-header         ${LAST_NAME} (Dupont) ${FIRST_NAME}
  Delete Patient
  Check That All Is Deleted       ${COOKIE.value}
  
*** Keywords ***  
Open session 
  Open Browser To Login Page 
  Login With      test  test

Close session 
  Close Browser

Delete Patient
  Check That Form Has             Supprimer 
  Click Button                    jquery:button:contains("Supprimer")
  Wait Until Element Contains     jquery:div[class~="modal-content"]>div>h3       Confirmer
  Click Button                    modal-btn-ok
  Wait For Condition              return document.location == "${ROOT_URL}/#/"
 

Check That Form Has
  [Arguments]                     ${action_name}
  Page Should Contain Button      jquery:button:contains(${action_name})

Check That All Is Deleted 
  [Arguments]                     ${session_id}
  ${session_cookie}   Create Dictionary   sessionid=${session_id}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request   restapi     /api/patients/1
  Should Be Equal As Strings     ${resp.status_code}         404
  ${resp} =           Get Request   restapi     /api/examinations
  Should Be Equal As Strings     ${resp.status_code}         200
  Should Be Empty     ${resp.json()} 
  ${resp} =           Get Request   restapi     /api/events 
  Should Be Equal As Strings     ${resp.status_code}         200
  Should Be Empty     ${resp.json()}
  ${resp} =           Get Request   restapi     /api/invoices

 


  
