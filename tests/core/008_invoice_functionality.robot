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
${INVOICE_ID}       2
${PATIENT_URL}      \#/patient/2
${INVOICE_NUMBER}   25000
${EXAMINATION_ID}   3

*** Test Cases ***
Change Invoice Start Number
  [Documentation]   Edit the office settings to change the invoice start number
  ${COOKIE} =         Get Cookie      sessionid
  Edit Settings
  Clear Element Text              invoice_start_sequence
  Should Be Invalid               invoice_start_sequence
  Input Text                      invoice_start_sequence         25000
  Should Be Valid                 invoice_start_sequence
  Apply Settings
  Element Should Be Visible       jquery:div.growl-item.alert.alert-success
  Ensure That Event Is Created    ${COOKIE.value}                  25000

Invoice With The New Sequence
  Create Patient
  Search For Patient
  Write New Examination Invoiced

Change Invoice Start Number Before
  [Documentation]   Edit the office settings to change the invoice start number on a number before an existing invoice
  ${COOKIE} =         Get Cookie      sessionid
  Edit Settings
  Clear Element Text              invoice_start_sequence
  Should Be Invalid               invoice_start_sequence
  Input Text                      invoice_start_sequence         15000
  Should Be Invalid               invoice_start_sequence
  Input Text                      invoice_start_sequence         25500
  Should Be Valid                 invoice_start_sequence
  Apply Settings
  Element Should Be Visible       jquery:div.growl-item.alert.alert-success
  Ensure That Event Is Created    ${COOKIE.value}                25500
  Input Text                      invoice_start_sequence         25000
  Should Be Invalid               invoice_start_sequence
  Input Text                      invoice_start_sequence         25001
  Should Be Valid                 invoice_start_sequence
  Apply Settings
  Element Should Be Visible       jquery:div.growl-item.alert.alert-success
  Ensure That Event Is Created    ${COOKIE.value}                25001


Change Invoice Start Number With Text
  [Documentation]   Edit the office settings to change the invoice start number on a number before an existing invoice
  Edit Settings
  Clear Element Text              invoice_start_sequence
  Should Be Invalid               invoice_start_sequence
  Input Text                      invoice_start_sequence        FACT00001
  Should Be Invalid               invoice_start_sequence
  Apply Settings
  Element Should Be Visible       jquery:div.growl-item.alert.alert-danger


Cancel Invoice
  [Documentation]                 Open already invoiced examination and cancel an invoice
  Go To                           ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Wait Until Element Is Visible   cancelInvoiceBtn
  Click Button                    cancelInvoiceBtn
  Wait Until Element Is Visible   modal-btn-ok
  Click Button                    modal-btn-ok
  Wait Until Element Is Visible   invoiceExaminationBtn
  Wait Until Element Is Visible   unfold_invoices
  Click Button                    unfold_invoices
  Wait Until Element Is Visible   jquery:span[class~="label-warning"]:contains('Annulée')
  Wait Until Element Is Visible   jquery:a[href="invoice/2"]:contains('25000')
  Wait Until Element Is Visible   jquery:a[href="invoice/3"]:contains('25001')
  Invoice Again Examination
  Wait Until Element Is Visible   jquery:a[href="invoice/4"]:contains('25002')
  Go To                           ${ROOT_URL}/#/invoices
  Wait Until Element Is Visible   jquery:tbody>tr:eq(3)


*** Keywords ***
Edit Settings
  Click Element                   jquery:li.dropdown
  Click Element                   jquery:li#office-settings
  Wait Until Element Contains     jquery:h1.page-header         Paramètres du cabinet

Should Be Invalid
  [Arguments]                     ${element_locator}
  Should Have Class               ${element_locator}    ng-invalid

Should Be Valid
  [Arguments]                     ${element_locator}
  Should Have Class               ${element_locator}    ng-valid

Should Have Class
  [Arguments]                     ${element_locator}    ${class_on_element}
  Wait For Condition              return $(${element_locator}).attr('class').split(' ').indexOf('ng-animate') == -1
  ${class_on_input}=              Get Element Attribute       ${element_locator}      class
  ${class_list_on_input}=         Evaluate                    $class_on_input.split(' ')
  Should Contain                  ${class_list_on_input}           ${class_on_element}

Apply Settings
  Click Button                    jquery:button.btn.btn-primary
  Wait Until Element Is Enabled   jquery:div.growl-item

Ensure That Event Is Created
   [Arguments]                     ${session_id}    ${value}
  ${session_cookie}               Create Dictionary   sessionid=${session_id}
  Login REST with                 test        ${session_cookie}
  ${resp} =                       Get Request   restapi     /api/events
  RequestsLogger.Write log        ${resp}
  Should Be Equal As Strings      ${resp.status_code}         200
  ${last_event}=                  Set Variable  ${resp.json()[0]}
  Should Be Equal As Strings      ${last_event['therapeut_name']['username']}    test
  Should Contain                  ${last_event['translated_comment']}            ${value}
  Should Be Equal As Strings      ${last_event['clazz']}     OfficeSettings

