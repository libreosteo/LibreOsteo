# -*- coding: robot -*-
*** Settings ***
Test Setup        Open session      test    test
Test Teardown     Close session
Resource          resources.txt

*** Variables ***

*** Test Cases ***
Import Patient From CSV File
  [Documentation]  Import patient from an external system
  Open Import From External System
  Scroll Element Into View        jquery:div.panel-heading:contains("Importer")
  Select Patient File
  Analyze Importation
  Check The Analyze Patient
  Import File Success

Import Examinations From CSV File
  [Documentation]   Import examination from an external system
  Open Import From External System
  Scroll Element Into View        jquery:div.panel-heading:contains("Importer")
  Select Patient File
  Select Examination File
  Analyze Importation
  Check The Analyze Patient
  Check The Analyze Examination
  Import File With Error In Patient

*** Keywords ***
Open Import From External System
  Click Element                   jquery:li.dropdown
  Click Element                   jquery:li#import-file
  Wait Until Element Contains     jquery:h1.page-header        Gestion de l'import/export
  Click Element                   jquery:a:contains("Importer d'un système externe")
  Wait Until Element Contains     jquery:div.well              Note

Select Patient File
  Choose File                     patient-file                 ${CURDIR}/resources/patients_1.csv

Select Examination File
  Choose File                     examination-file             ${CURDIR}/resources/examinations_1.csv

Analyze Importation
  Click Button                    jquery:button:contains("Analyser")
  Wait That Page Is Ready

Check The Analyze Patient
  Wait Until Page Contains Element      patient-file-analyze
  Element Should Be Visible             jquery:#patient-file-analyze>p>span.text-success
  Table Header Should Contain           jquery:#patient-file-analyze>div>table       Nom de famille

Check The Analyze Examination
  Wait Until Page Contains Element      examination-file-analyze
  Element Should Be Visible             jquery:#examination-file-analyze>p>span.text-success
  Table Header Should Contain           jquery:#examination-file-analyze>div>table   Motif

Import File Success
  Click Button                          jquery:button.btn-success:contains("Importer")
  Wait That Import Is Complete
  Wait Until Element Contains           jquery:div.panel-success>div.panel-heading    Importation réussie
  Wait Until Element Contains           jquery:div.panel-success>div.panel-body       100 lignes importées du fichier patient

Import File With Error In Patient
  Click Button                          jquery:button.btn-success:contains("Importer")
  Wait That Import Is Complete
  Wait Until Element Contains           jquery:div.panel-warning>div.panel-heading    Importation réussie avec des erreurs
  Wait Until Element Contains           jquery:div.panel-warning>div.panel-body       0 lignes importées du fichier patient
  Wait Until Element Contains           jquery:div.panel-warning>div.panel-body       50 lignes importées du fichier consultation
Wait That Import Is Complete
  Wait Until Element Is Not Visible     loading-bar         2 min

