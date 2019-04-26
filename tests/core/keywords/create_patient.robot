*** Keywords ***
Create Patient
  Click Element                   jquery:a:contains("Nouveau patient")
  Check That Url Is               ${ROOT_URL}/#/addPatient
  Wait That Page Is Ready
  Wait Until Element Contains     jquery:h1.page-header         Nouveau patient
  Input Text                      family_name                   ${LAST_NAME}
  Input Text                      first_name                    ${FIRST_NAME}
  Input Text                      jquery:input.dd               ${BIRTH_DAY}
  Input Text                      jquery:input.mm               ${BIRTH_MONTH}
  Input Text                      jquery:input.yy               ${BIRTH_YEAR}
  Wait Until Element Is Enabled   jquery:button.btn.btn-primary
  Click Button                    jquery:button.btn.btn-primary
  Wait Until Element Contains     jquery:h1.page-header         ${LAST_NAME}
  Wait That Page Is Ready
  Check That Form Has             Éditer
  Check That Form Has             Supprimer
  Check That Form Does Not Have   Fin d'édition
  Check That Url Is               ${ROOT_URL}/#/patient/${ID_PATIENT}


