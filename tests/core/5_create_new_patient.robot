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

*** Keywords ***
Create Patient
  Click Element                   jquery:a:contains("Nouveau patient")
  Wait Until Element Contains     jquery:h1.page-header         Nouveau patient 
  Input Text                      family_name                   ${LAST_NAME}
  Input Text                      first_name                    ${FIRST_NAME}
  Input Text                      jquery:input.dd               ${BIRTH_DAY}
  Input Text                      jquery:input.mm               ${BIRTH_MONTH}
  Input Text                      jquery:input.yy               ${BIRTH_YEAR}
  Wait Until Element Is Enabled   jquery:button.btn.btn-primary 
  Click Button                    jquery:button.btn.btn-primary 
  Wait Until Element Contains     jquery:h1.page-header         ${LAST_NAME} 
  -- Check that Editer/Supprimer is available
  -- Check each tab for editing.
  -- Check that when reloading, information are there

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
