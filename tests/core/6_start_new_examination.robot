# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt

*** Variables ***
${LAST_NAME}        Picard 
${FIRST_NAME}       Jean-Luc
${PATIENT_URL}      \#/patient/1
&{COOKIE}

*** Test Cases ***
Search For Patient
  Go To             ${ROOT_URL}
  Input Text        jquery:div[class~="custom-search-form"]>input      ${LAST_NAME}
  Click Button      jquery:div[class~="custom-search-form"]>span>button
  Wait Until Element Contains           jquery:h3.page-header         ${LAST_NAME}
  Wait Until Page Contains Element      jquery:div[class~="search-entry"]>h4>a     
  Click Link                            jquery:div[class~="search-entry"]>h4>a
  Location Should Be                    ${ROOT_URL}/${PATIENT_URL}
  Wait Until Element Contains           jquery:h1.page-header         ${LAST_NAME} ${FIRST_NAME}
  Click Element                         examinations
  Click Button                          new-examination-btn
  Wait Until Element Is Visible         current-examination

Write New Examination
  Input Text                            jquery:input[placeholder~="Motif"]      Motif de consultation
  Input Text                            jquery:div[class~="inPlaceholderMode"]:contains(Examen)         Examen normal
  Click Button                          jquery:button[class~="btn-success"]
  Click Element                         jquery:input[value="notinvoiced"]
  Input Text                            reason                                  Test
  Element Should Be Enabled             jquery:button[class~="btn-primary"]        
  Click Button                          jquery:button[class~="btn-primary"]
