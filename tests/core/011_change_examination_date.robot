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
Change Examination Date
  ${COOKIE} =         Get Cookie      sessionid
  Go To                               ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible       jquery:button[class~="btn-default"]:contains('Éditer')
  Click Element                       jquery:button[class~="btn-default"]:contains('Éditer')
  Wait Until Element Is Visible       jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDateValue}             Get Value         jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDate}=                 Convert Date      ${examinationDateValue}       date_format=%d/%m/%Y
  ${examinationDate}                  Subtract Time From Date    ${examinationDate}   3 days      result_format=%d/%m/%Y
  Input Text                          jquery:input[class~="ws-date"][class~="examinationdate"]    ${examinationDate}
  Click Element                       jquery:button[class~="btn-default"]:contains("Fin d'édition")
  Wait Until Element Is Visible       jquery:span[id="examinationDate"]
  ${dateValue}                        Get Text          jquery:span[id="examinationDate"]
  ${examinationDate}=                 Convert Date         ${examinationDate}   datetime    date_format=%d/%m/%Y
  ${longExpectedExaminationDate}      Format Longdate      ${examinationDate}
  Should Be Equal                     ${longExpectedExaminationDate}      ${dateValue}
  Sleep                               2s            Wait to be sure that REST request is not cached
  Ensure That Examination Has Date    ${COOKIE.value}     ${EXAMINATION_ID}     ${examinationDate}

Change Examination Date In Future
  ${COOKIE} =         Get Cookie      sessionid
  Go To                               ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible       jquery:button[class~="btn-default"]:contains('Éditer')
  Click Element                       jquery:button[class~="btn-default"]:contains('Éditer')
  Wait Until Element Is Visible       jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDateValue}             Get Value         jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDate}=                 Convert Date      ${examinationDateValue}       date_format=%d/%m/%Y
  ${futurExaminationDate}             Add Time To Date    ${examinationDate}   13 days      result_format=%d/%m/%Y
  Input Text                          jquery:input[class~="ws-date"][class~="examinationdate"]    ${futurExaminationDate}
  Click Element                       jquery:button[class~="btn-default"]:contains("Fin d'édition")
  Wait Until Element Is Visible       jquery:div[class~="editable-error"]:contains("La date est invalide")
  Element Should Be Visible           jquery:button[class~="btn-default"]:contains("Fin d'édition")
  ${examinationDate}=                 Convert Date         ${examinationDate}   datetime
  Sleep                               2s            Wait to be sure that REST request is not cached
  Ensure That Examination Has Date    ${COOKIE.value}     ${EXAMINATION_ID}     ${examinationDate}

Change Date On Invoiced Examination Future
  ${COOKIE} =         Get Cookie      sessionid
  Sleep                               2s
  ${invoiceDate}                      Get Date Invoice                    ${INVOICE_NUMBER}
  ${newDate}                          Subtract Time From Date   ${invoiceDate}    15 days     result_format=datetime    date_format=datetime
  Sleep                               2s
  Change Date Invoice                 ${INVOICE_NUMBER}  ${newDate}
  Sleep                               2s
  Change Date Examination             ${EXAMINATION_ID}  ${newDate}
  Go To                               ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible       jquery:button[class~="btn-default"]:contains('Éditer')
  Click Element                       jquery:button[class~="btn-default"]:contains('Éditer')
  Wait Until Element Is Visible       jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDateValue}             Get Value         jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDate}=                 Convert Date      ${examinationDateValue}       date_format=%d/%m/%Y
  ${examinationDate}                  Add Time To Date    ${examinationDate}   20 days      result_format=%d/%m/%Y
  Input Text                          jquery:input[class~="ws-date"][class~="examinationdate"]    ${examinationDate}
  Click Element                       jquery:button[class~="btn-default"]:contains("Fin d'édition")
  Wait Until Element Is Visible       jquery:div[class~="editable-error"]:contains("La date est invalide")
  Element Should Be Visible           jquery:button[class~="btn-default"]:contains("Fin d'édition")
  ${examinationDate}=                 Convert Date         ${examinationDateValue}         date_format=%d/%m/%Y  result_format=datetime
  Sleep                               2s            Wait to be sure that REST request is not cached
  Ensure That Examination Has Date    ${COOKIE.value}     ${EXAMINATION_ID}     ${examinationDate}


Change Date On Invoiced Examination
  ${COOKIE} =         Get Cookie      sessionid
  Sleep                               2s
  ${invoiceDate}                      Get Date Invoice                    ${INVOICE_NUMBER}
  ${newDate}                          Subtract Time From Date   ${invoiceDate}    5 days     result_format=datetime    date_format=datetime
  Sleep                               2s
  Change Date Invoice                 ${INVOICE_NUMBER}  ${newDate}
  Sleep                               2s
  Change Date Examination             ${EXAMINATION_ID}  ${newDate}
  Go To                               ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible       jquery:button[class~="btn-default"]:contains('Éditer')
  Click Element                       jquery:button[class~="btn-default"]:contains('Éditer')
  Wait Until Element Is Visible       jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDateValue}             Get Value         jquery:input[class~="ws-date"][class~="examinationdate"]
  ${examinationDate}=                 Convert Date      ${examinationDateValue}       date_format=%d/%m/%Y
  ${examinationDate}                  Subtract Time From Date    ${examinationDate}   2 days      result_format=%d/%m/%Y
  Input Text                          jquery:input[class~="ws-date"][class~="examinationdate"]    ${examinationDate}
  Click Element                       jquery:button[class~="btn-default"]:contains("Fin d'édition")
  Wait Until Element Is Visible       jquery:span[id="examinationDate"]
  ${dateValue}                        Get Text          jquery:span[id="examinationDate"]
  ${examinationDate}=                 Convert Date         ${examinationDate}   datetime    date_format=%d/%m/%Y
  ${longExpectedExaminationDate}      Format Longdate      ${examinationDate}
  Should Be Equal                     ${longExpectedExaminationDate}      ${dateValue}
  ${examinationDate}=                 Convert Date         ${examinationDate}         date_format=%d/%m/%Y  result_format=datetime
  Sleep                               2s            Wait to be sure that REST request is not cached
  Ensure That Examination Has Date    ${COOKIE.value}     ${EXAMINATION_ID}     ${examinationDate}


*** Keywords ***
Ensure That Examination Has Date
  [Arguments]                     ${session_id}       ${examination_id}      ${examinationDate}
  ${session_cookie}               Create Dictionary   sessionid=${session_id}
  Login REST with                 test        ${session_cookie}
  ${resp} =                       GET On Session   restapi     /api/examinations/${examination_id}
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Strings      ${resp.status_code}         200
  ${examination}=                  Set Variable  ${resp.json()}
  ${readExaminationDate}          Convert Django Timezone Date    ${examination['date']}
  Should Be Equal As Date Only    ${readExaminationDate}   ${examinationDate}
