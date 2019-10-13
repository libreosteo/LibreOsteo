*** Keywords ***
Search For Patient
  Go To             ${ROOT_URL}
  Input Text        jquery:div[class~="custom-search-form"]>input      ${LAST_NAME}
  Click Button      jquery:div[class~="custom-search-form"]>span>button
  Wait Until Element Contains           jquery:h3.page-header         ${LAST_NAME}
  Wait Until Page Contains Element      jquery:div[class~="search-entry"]>h4>a
  Click Link                            jquery:div[class~="search-entry"]>h4>a
  Location Should Be                    ${ROOT_URL}/${PATIENT_URL}
  ${expected_header}=                   Evaluate                     ' '.join([z for z in ('%s %s %s' % ($LAST_NAME, $ORIGINAL_NAME_HEADER, $FIRST_NAME)).split(' ') if len(z) > 0 ])
  Wait Until Element Contains           jquery:h1.page-header         ${expected_header}
  Click Element                         examinations
  Click Button                          new-examination-btn
  Wait Until Element Is Visible         current-examination

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
  Go To                                 ${ROOT_URL}/invoice/${INVOICE_ID}
  Element Should Contain                patient                 ${FIRST_NAME} ${LAST_NAME}
  Element Should Contain                main                    Template with 55 EUR
  Element Should Contain                invoice-number          ${INVOICE_NUMBER}

Invoice Again Examination
  Click Button                          invoiceExaminationBtn
  Click Element                         jquery:input[value="invoiced"]
  Wait Until Element Is Visible         jquery:input[value="check"]
  Click Element                         jquery:input[value="check"]
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider')
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')

Write New Examination Invoiced Non Paid
  Go To                                 ${ROOT_URL}
  Go To                                 ${ROOT_URL}/${PATIENT_URL}/examinations
  Click Button                          new-examination-btn
  Wait Until Element Is Visible         current-examination
  Input Text                            jquery:input[placeholder~="Motif"]      Motif de consultation
  Input Text                            jquery:div[class~="inPlaceholderMode"]:contains(Examen)         Examen normal
  Click Button                          close-examination
  Click Element                         jquery:input[value="invoiced"]
  Wait Until Element Is Visible         jquery:input[value="notpaid"]
  Click Element                         jquery:input[value="notpaid"]
  Element Should Be Enabled             jquery:button[class~="btn-primary"]:contains('Valider')
  Click Button                          jquery:button[class~="btn-primary"]:contains('Valider')
  Go To                                 ${ROOT_URL}/invoice/${INVOICE_ID}
  Element Should Contain                patient                 ${FIRST_NAME} ${LAST_NAME}
  Element Should Contain                main                    Template with 55 EUR
  Element Should Contain                invoice-number          ${INVOICE_NUMBER}
  Element Should Contain                main                    Non réglée en date de facture

