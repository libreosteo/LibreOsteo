# -*- coding: robot -*-
*** Settings ***
Resource   resources.txt
Resource    keywords/create_examination.robot

*** Variables ***
${LAST_NAME}        Picard 
${FIRST_NAME}       Jean-Luc
${PATIENT_URL}      \#/patient/1
${ORIGINAL_NAME_HEADER}     (Dupont)
${INVOICE_ID}       1
${INVOICE_NUMBER}   10000
&{COOKIE}

*** Test Cases ***
Search For Patient
  Search For Patient

Write New Examination Not Invoiced
  Input Text                            jquery:input[placeholder~="Motif"]      Motif de consultation
  Input Text                            jquery:div[class~="inPlaceholderMode"]:contains(Examen)         Examen normal
  Click Button                          close-examination
  Click Element                         jquery:input[value="notinvoiced"]
  Input Text                            reason                                  Test
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider') 
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')

Write New Examination Invoiced 
  Write New Examination Invoiced
