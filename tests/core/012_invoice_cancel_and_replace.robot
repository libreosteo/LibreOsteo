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
${ID_PATIENT}       2
${ORIGINAL_NAME_HEADER}
${INVOICE_ID}       6
${REPLACEMENT_INVOICE_ID}   7
${PATIENT_URL}      \#/patient/2
${INVOICE_NUMBER}   25004
${REPLACEMENT_INVOICE_NUMBER}   25005
${EXAMINATION_ID}    55

*** Test Cases ***
Corrective Invoice On Already Invoiced Examination
  Change Setting For Corrective Invoice
  Search For Patient
  Write New Examination Invoiced
  Go To                                 ${ROOT_URL}/${PATIENT_URL}/examination/${EXAMINATION_ID}
  Cancel And Replace Invoice

*** Keywords ***
Change Setting For Corrective Invoice
  Edit Settings
  Click Element                  jquery:input[value="false"]
  Apply Settings

Cancel And Replace Invoice
  Click Button                          cancelInvoiceBtn
  Wait Until Element Is Visible         jquery:h3.modal-title
  Click Button                          modal-btn-ok
  Wait Until Element Is Visible         jquery:input[value="cash"]
  Click Element                         jquery:input[value="cash"]
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider')
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')
  Go To                                 ${ROOT_URL}/invoice/${REPLACEMENT_INVOICE_ID}
  Element Should Contain                patient                 ${FIRST_NAME} ${LAST_NAME}
  Element Should Contain                main                    Template with 55 EUR
  Element Should Contain                invoice-number          ${INVOICE_NUMBER}
  Element Should Contain                invoice-number          ${REPLACEMENT_INVOICE_NUMBER}




Edit Settings
  Click Element                   jquery:li.dropdown
  Click Element                   jquery:li#office-settings
  Wait Until Element Contains     jquery:h1.page-header         Paramètres du cabinet

Apply Settings
  Click Button                    jquery:button.btn.btn-primary
  Wait Until Element Is Enabled   jquery:div.growl-item


