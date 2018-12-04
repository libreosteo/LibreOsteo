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
  Wait Until Element Contains           jquery:h1.page-header         ${LAST_NAME} (Dupont) ${FIRST_NAME}
  Click Element                         examinations
  Click Button                          new-examination-btn
  Wait Until Element Is Visible         current-examination

Write New Examination Not Invoiced
  Input Text                            jquery:input[placeholder~="Motif"]      Motif de consultation
  Input Text                            jquery:div[class~="inPlaceholderMode"]:contains(Examen)         Examen normal
  Click Button                          close-examination
  Click Element                         jquery:input[value="notinvoiced"]
  Input Text                            reason                                  Test
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider') 
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')

Write New Examination Invoiced 
  Go To                                 ${ROOT_URL}
  Go To                                 ${ROOT_URL}/${PATIENT_URL}/examinations
  Click Button                          new-examination-btn
  Wait Until Element Is Visible         current-examination 
  Input Text                            jquery:input[placeholder~="Motif"]      Motif de consultation
  Input Text                            jquery:div[class~="inPlaceholderMode"]:contains(Examen)         Examen normal
  Click Button                          close-examination
  Click Element                         jquery:input[value="invoiced"]
  Wait Until Element Is Visible         jquery:input[value="check"] 
  Click Element                         jquery:input[value="check"]
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider')
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')
  Go To                                 ${ROOT_URL}/invoice/1
  Element Should Contain                patient                 ${FIRST_NAME} ${LAST_NAME}
  Element Should Contain                main                    Template with 55 EUR
