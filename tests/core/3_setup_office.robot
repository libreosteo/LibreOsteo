# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt

*** Variables ***
${OFFICE_ADDRESS_STREET}    27 rue Haute
${OFFICE_ADDRESS_COMPLEMENT} 
${OFFICE_ADDRESS_ZIPCODE}   87110
${OFFICE_ADDRESS_CITY}      Le Vigen
${OFFICE_ADDRESS_PHONE}     05 55 12 13 14

*** Test Cases ***

Open Settings
  [Documentation]   login a user and check that the user is asked to setup the office
  Open Browser To Login Page 
  Title Should Be     Signin on Libreosteo
  Login with      test   test
  Title Should Be     Libreosteo
  Element Should Not Be Visible     class:alert-danger
  Wait Until Element Is Enabled     jquery:div.popover-content
  Element Should Contain            jquery:div.popover-content      ADELI
  Element Should Be Visible         jquery:ul.dropdown-user
  Edit Settings
  [TearDown]    Close Browser


*** Keywords ***
Login With
  [Arguments]   ${login}  ${password}
  Input Text    username  ${login}
  Input Text    password    ${password}
  Click Button  login

Edit Settings
  Click Element                   li.ct-active>a>i:nth-child(2)
  Click Element                   li#office-settings
  Wait Until Element Is Enabled   h1.page-header
  Element Should Contain          h1.page-header      Office settings
  Input Text                      office_address_street   ${OFFICE_ADDRESS_STREET}
  Input Text                      office_address_complement     ${OFFICE_ADDRESS_COMPLEMENT}
  Click Button                    class:btn btn-primary

Logout
  Go To   ${LOGIN_URL}/logout
  Title Should Be     Signin on Libreosteo
