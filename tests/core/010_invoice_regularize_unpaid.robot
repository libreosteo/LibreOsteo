# -*- coding: robot -*-
*** Settings ***
Test Setup        Open session      test    test
Test Teardown     Close session
Resource          resources.txt
Resource          keywords/create_patient.robot
Resource          keywords/create_examination.robot

*** Variables ***
${LAST_NAME}        Picard
${FIRST_NAME}       Jean-Luc
${EMAIL}            jean-luc.picard@starfleet.com
${BIRTH_DAY}        13
${BIRTH_MONTH}      07
${BIRTH_YEAR}       1935
${ID_PATIENT}       2
${ORIGINAL_NAME_HEADER}
${INVOICE_ID}       5
${PATIENT_URL}      \#/patient/2
${INVOICE_NUMBER}   25003
${EXAMINATION_ID}   54

*** Test Cases ***
Invoice A Non Paid Examination
  ${COOKIE} =         Get Cookie      sessionid
  Search For Patient
  Write New Examination Invoiced Non Paid
  Go To                                 ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible          finishPaimentBtn
  Regularize Invoice          ${EXAMINATION_ID}     "check"
  Ensure Examination Is Paid    ${COOKIE.value}       ${EXAMINATION_ID}   ${INVOICE_ID}


*** Keywords ***
Regularize Invoice
  [Arguments]       ${examination_id}     ${paiment_mean}
  Click Button      finishPaimentBtn
  Wait Until Element Is Visible         jquery:input[value=${paiment_mean}]
  Click Element                         jquery:input[value=${paiment_mean}]
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider')
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')
  Wait Until Element Is Not Visible     finishPaimentBtn
  Go To                                 ${ROOT_URL}/invoice/${INVOICE_ID}
  Element Should Contain                patient                 ${FIRST_NAME} ${LAST_NAME}
  Element Should Contain                main                    Template with 55 EUR
  Element Should Contain                invoice-number          ${INVOICE_NUMBER}
  Element Should Contain                paiments                Réglé(s) le

Ensure Examination Is Paid
  [Arguments]                     ${session_id}       ${exmination_id}      ${invoice_id}
  ${session_cookie}               Create Dictionary   sessionid=${session_id}
  Login REST with                 test        ${session_cookie}
  ${resp} =                       Get Request   restapi     /api/examinations/${exmination_id}
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Strings      ${resp.status_code}         200
  ${examination}=                  Set Variable  ${resp.json()}
  Should Be Equal As Strings      ${examination['status']}    2
  ${resp} =                       Get Request   restapi     /api/invoices/${invoice_id}
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Strings      ${resp.status_code}         200
  ${invoice}=                     Set Variable  ${resp.json()}
  Should Be Equal As Strings      ${invoice['status']}        2
  Should Not Be Empty             ${invoice['paiments_list']}
  ${length}=                      Get Length                  ${invoice['paiments_list']}
  Should Be Equal As Strings      ${length}                   1
  Should Be Equal As Strings      ${invoice['paiments_list'][0]['paiment_mode']}     check
  Should Be Equal As Strings      ${invoice['paiments_list'][0]['currency']}         EUR
  Should Be Equal As Strings      ${invoice['paiments_list'][0]['amount']}        55.0

