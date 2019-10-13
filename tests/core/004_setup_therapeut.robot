# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt

*** Variables ***
${LAST_NAME}        Tester
${FIRST_NAME}       Robot
${EMAIL}            test@robot.com
${ADELI}            67654684
${QUALITY}          Ostéopathe DO
&{COOKIE}

*** Test Cases ***

Open Therapeut Settings
  [Documentation]   login a user and check that the user is asked to setup this therapeut settings
  Open Browser To Login Page 
  Title Should Be     Identifiez-vous sur Libreosteo
  Login with      test   test
  Title Should Be     Libreosteo
  ${COOKIE} =         Get Cookie      sessionid
  Element Should Not Be Visible     class:alert-danger
  Wait Until Element Is Enabled     jquery:div.popover-content
  Element Should Contain            jquery:div.popover-content      ADELI
  Element Should Be Visible         jquery:ul.dropdown-user
  Edit Therapeut Settings
  Check Rest User                   ${COOKIE.value} 
  Check Rest User Profile           ${COOKIE.value}
  [TearDown]    Close Browser


*** Keywords ***
Login With
  [Arguments]   ${login}  ${password}
  Input Text    username  ${login}
  Input Text    password    ${password}
  Set Selenium Speed      0.1 second
  Click Button  login

Edit Therapeut Settings
  Click Element                   jquery:li.open
  Click Element                   jquery:li#user-profile
  Wait Until Element Contains     jquery:h1.page-header             Profil utilisateur  
  Input Text                      jquery:input[name="last_name"]    ${LAST_NAME}
  Input Text                      first_name                        ${FIRST_NAME}
  Input Text                      email                             ${EMAIL}
  Input Text                      inputAdeli                        ${ADELI}
  Input Text                      inputQuality                      ${QUALITY}
  Click Button                    jquery:button.btn.btn-primary
  Wait Until Element Is Enabled   jquery:div.growl-item
  Element Should Be Visible       jquery:div.growl-item.alert.alert-success

Check Rest User
  [Arguments]     ${session_token}
  ${session_cookie}   Create Dictionary   sessionid=${session_token}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request   restapi     /api/users/1
  RequestsLogger.Write log       ${resp}
  Should Be Equal As Strings     ${resp.json()['username']}      test 
  Should Be Equal As Strings     ${resp.json()['first_name']}    ${FIRST_NAME}
  Should Be Equal As Strings     ${resp.json()['last_name']}     ${LAST_NAME}
  Should Be Equal As Strings     ${resp.json()['email']}         ${EMAIL}

Check Rest User Profile
  [Arguments]     ${session_token}
  ${session_cookie}   Create Dictionary   sessionid=${session_token}
  Login REST with     test        ${session_cookie}
  ${resp} =           Get Request   restapi     /api/profiles/get_by_user
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Numbers      ${resp.json()['id']}            1
  Should Be Equal As Strings      ${resp.json()['adeli']}         ${ADELI}
  Should Be Equal As Strings      ${resp.json()['quality']}       ${QUALITY}

Logout
  Go To   ${ROOT_URL}/logout
 
