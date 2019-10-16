Changelog for Libreosteo
========================


0.6.1 (unreleased)
------------------

- Nothing changed yet.


0.6.0 (2019-10-16)
------------------

- Reorganize the home page to be more smart
- Add support for managing documents on patient folder
- Add support to enable/disable some paiment means
- Add support to cancel invoices
- Add support to display all invoices for accountability purpose
- Add support to delete a patient in accordance with GDPR conformity
- Add support to regularize unpaid examinations
- Add helper to detect network address on which the application is available
- Remove the bower dependency and use yarn
- Add support to continuous integration with travis, and some testing from UI with robot framework
- Add support for python 3.X and python 2.X for the software


0.5.7 (2017-06-04)
------------------

- Add support for email field


0.5.6 (2017-06-03)
------------------

- Fix problem when importing CSV file with complete data. use a buffer of 4Ko instead of 1Ko.
- Fix missing error message when birth date is incorrect in patient file


0.5.5 (2016-12-01)
------------------

- Fix problem when creating settings on the office on a new empty instance.


0.5.4 (2016-10-20)
------------------

- Add possibility to rebuild index at any time from the interface.


0.5.3 (2016-10-19)
----------------

- Add support to archive and restore database (restoring when installing)
- Add support to compression for Css/Js (avoid blank pages when updating script and force refresh when releasing version)


0.5.2 (2016-07-13)
------------------

- Fix editing birthdate on patient file on a negative GMT timezone offset 


0.5.1 (2016-05-04)
------------------

- Fix the command panel to edit patient file/examinations when scrolling page
- autosave and close the edit mode when changing tab on the patient file (not the examination)
- Change filter to manage name with "particule" specifically.


0.5.0 (2016-04-27)
------------------

- Finalize version
- Release Docker file to create a docker container with the release
- Improve export to reorganize fields.


0.4.9.2 (2016-04-23)
--------------------

- Add laterality on patient file
- Add support to import examinations linked to patient
- Add support to export patients and examinations as CSV files.


0.4.9.1 (2016-04-12)
--------------------

- Add support to import patient into the system through CSV file.
- Change the editor for textarea to Hallo.js and allow to edit rich text in the application
- Allow to edit/delete patient
- Allow to edit/delete examination
- Add filter to automatically set uppercase on name for patient
- Improve the print of invoice
- Allow to import patient through csv file.


0.4.3 (2016-02-11)
------------------

- Fix the process management on MacOS X platform.
