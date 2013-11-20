# -*- coding: utf-8 -*-

"""
    LibreOsteo - a tool to manage osteopathy consultation
    Copyright (C) 2011  garth <garth@tuxfamily.org>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
import gtk
import views
from views.contentview import ContentBuilder
from business.helperservice import get_services
from business import patientservice
import datetime
import time
from business.helperservice import get_date_text
from business.examinationmodel import Examination

class ExaminationContent(object):

    _gladefile = "views/gtkbuilder/libreosteo-examination.glade"
    _maincontent_name = "maincontent"
    _maincontent = None
    
    def __init__(self, parent=None):
        content_builder = ContentBuilder()
        content_builder.gladefile = self._gladefile
        self._maincontent = content_builder.view
        self._maincontent.connect_signals(self)
        self._maincontent.get_object("label_patient_name").set_text('')
        if parent is not None:
            content_builder.attach(parent, self._maincontent_name)
        self._examination = None
    
    def get_examination_name(self):
        patient = get_services().examination_service.get_current_patient()
        if not patient is None:
            return "%s %s - %s" % (patient.family_name.upper(), patient.firstname, get_date_text(
            datetime.date.fromtimestamp(time.time()), "%d/%m/%Y"))
        return ""
    
    def update(self):
        self._maincontent.get_object("label_patient_name").set_text(self.get_examination_name())
        self._examination = Examination()
        self._examination.patients_id = get_services().examination_service.get_current_patient().id
        self._examination.date = datetime.date.fromtimestamp(time.time())
        exam = get_services().examination_service.request_for_examination(self._examination.patients_id, self._examination.date)
        if exam is None:
            get_services().examination_service.save(self._examination)
        else :
            self._examination = exam
        self._fill()
        
    def _fill(self):
        if self._examination.reason:
            self._maincontent.get_object("textbuffer_examination_reason").set_text(self._examination.reason)
        else:
            self._maincontent.get_object("textbuffer_examination_reason").set_text('')
        if self._examination.orl:
            self._maincontent.get_object("textbuffer_orl").set_text(self._examination.orl)
        else :
            self._maincontent.get_object("textbuffer_orl").set_text('')
            
        if self._examination.visceral:
            self._maincontent.get_object("textbuffer_visceral").set_text(self._examination.visceral)
        else:
            self._maincontent.get_object("textbuffer_visceral").set_text('')
            
        if self._examination.pulmo:
            self._maincontent.get_object("textbuffer_pulmo").set_text(self._examination.pulmo)
        else:
            self._maincontent.get_object("textbuffer_pulmo").set_text('')
        
        if self._examination.uro_gyneco:
            self._maincontent.get_object("textbuffer_uro_gyneco").set_text(self._examination.uro_gyneco)
        else:
            self._maincontent.get_object("textbuffer_uro_gyneco").set_text('')
        
        if self._examination.periphery:
            self._maincontent.get_object("textbuffer_peripherie").set_text(self._examination.periphery)
        else:
            self._maincontent.get_object("textbuffer_peripherie").set_text('')
        
        if self._examination.general_state:
            self._maincontent.get_object("textbuffer_general_state").set_text(self._examination.general_state)
        else:
            self._maincontent.get_object("textbuffer_general_state").set_text('')
        
        if self._examination.medical_examination:
            self._maincontent.get_object("textbuffer_medical_examination").set_text(self._examination.medical_examination)
        else:
            self._maincontent.get_object("textbuffer_medical_examination").set_text('')
        
        if self._examination.tests:
            self._maincontent.get_object("textbuffer_tests").set_text(self._examination.tests)
        else:
            self._maincontent.get_object("textbuffer_tests").set_text('')
            
        if self._examination.diagnosis:
            self._maincontent.get_object("textbuffer_diagnostic").set_text(self._examination.diagnosis)
        else:
            self._maincontent.get_object("textbuffer_diagnostic").set_text('')
        
        if self._examination.treatments:
            self._maincontent.get_object("textbuffer_treatment").set_text(self._examination.treatments)
        else:
            self._maincontent.get_object("textbuffer_treatment").set_text('')
        
        if self._examination.conclusion:
            self._maincontent.get_object("textbuffer_conclusion").set_text(self._examination.conclusion)
        else:
            self._maincontent.get_object("textbuffer_conclusion").set_text('')
    
    def get_maincontent(self):
        return self._maincontent.get_object(self._maincontent_name)
    
    def on_textview_conclusion_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_conclusion").get_bounds()
        conclusion = self._maincontent.get_object("textbuffer_conclusion").get_slice(start, end, False)
        if conclusion != self._examination.conclusion:
            self._examination.conclusion = conclusion
            get_services().examination_service.save(self._examination)
    
    def on_textview_treatment_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_treatment").get_bounds()
        treatments = self._maincontent.get_object("textbuffer_treatment").get_slice(start, end, False)
        if treatments != self._examination.treatments:
            self._examination.treatments = treatments
            get_services().examination_service.save(self._examination)
    
    def on_textview_diagnostic_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_diagnostic").get_bounds()
        diagnosis = self._maincontent.get_object("textbuffer_diagnostic").get_slice(start, end, False)
        if diagnosis != self._examination.diagnosis:
            self._examination.diagnosis = diagnosis
            get_services().examination_service.save(self._examination)
        
    def on_textview_test_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_tests").get_bounds()
        tests = self._maincontent.get_object("textbuffer_tests").get_slice(start, end, False)
        if tests != self._examination.tests:
            self._examination.tests = tests
            get_services().examination_service.save(self._examination)
    
    def on_textview_medical_examination_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_medical_examination").get_bounds()
        medical_examination = self._maincontent.get_object("textbuffer_medical_examination").get_slice(start, end, False)
        if medical_examination != self._examination.medical_examination:
            self._examination.medical_examination = medical_examination
            get_services().examination_service.save(self._examination)
    
    def on_textview_general_state_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_general_state").get_bounds()
        general_state = self._maincontent.get_object("textbuffer_general_state").get_slice(start, end, False)
        if general_state != self._examination.general_state:
            self._examination.general_state = general_state
            get_services().examination_service.save(self._examination)
    
    def on_textview_peripherie_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_peripherie").get_bounds()
        periphery = self._maincontent.get_object("textbuffer_peripherie").get_slice(start, end, False)
        if periphery != self._examination.periphery:
            self._examination.periphery = periphery
            get_services().examination_service.save(self._examination)
    
    def on_textview_uro_gyneco_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_uro_gyneco").get_bounds()
        uro_gyneco = self._maincontent.get_object("textbuffer_uro_gyneco").get_slice(start, end, False)
        if uro_gyneco != self._examination.uro_gyneco:
            self._examination.uro_gyneco = uro_gyneco
            get_services().examination_service.save(self._examination)
    
    def on_textview_pulmo_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_pulmo").get_bounds()
        pulmo = self._maincontent.get_object("textbuffer_pulmo").get_slice(start, end, False)
        if pulmo != self._examination.pulmo:
            self._examination.pulmo = pulmo
            get_services().examination_service.save(self._examination)
    
    def on_textview_visceral_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_visceral").get_bounds()
        visceral = self._maincontent.get_object("textbuffer_visceral").get_slice(start, end, False)
        if visceral != self._examination.visceral:
            self._examination.visceral = visceral
            get_services().examination_service.save(self._examination)
    
    def on_textview_orl_focus_out_event(self, sender, event):
        start, end = self._maincontent.get_object("textbuffer_orl").get_bounds()
        orl = self._maincontent.get_object("textbuffer_orl").get_slice(start, end, False)
        if orl != self._examination.orl:
            self._examination.orl = orl
            get_services().examination_service.save(self._examination)
            
            
            
class ExaminationReader(ExaminationContent):
    
    def __init__(self, examination, parent=None):
        ExaminationContent.__init__(self)
        self._examination = examination

    def get_examination_name(self):
        patient = self._examination.patient
        if not patient is None:
            return "%s %s - %s" % (patient.family_name.upper(), patient.firstname, get_date_text(self._examination.date, "%d/%m/%Y"))
        return ""
    
    def update(self):
        self._maincontent.get_object("label_patient_name").set_text(self.get_examination_name())
        self._fill()
        self._readonly()
    
    def _readonly(self):
        self._maincontent.get_object("textview_orl").set_editable(False)
        self._maincontent.get_object("textview_visceral").set_editable(False)
        self._maincontent.get_object("textview_pulmo").set_editable(False)
        self._maincontent.get_object("textview_uro_gyneco").set_editable(False)
        self._maincontent.get_object("textview_peripherie").set_editable(False)
        self._maincontent.get_object("textview_general_state").set_editable(False)
        self._maincontent.get_object("textview_medical_examination").set_editable(False)
        self._maincontent.get_object("textview_test").set_editable(False)
        self._maincontent.get_object("textview_diagnostic").set_editable(False)
        self._maincontent.get_object("textview_treatment").set_editable(False)
        self._maincontent.get_object("textview_conclusion").set_editable(False)

    def get_widget(self):
        return self.get_maincontent()