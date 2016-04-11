import logging
import csv
from django.utils.translation import ugettext_lazy as _
import random
from libreosteoweb.models import Patient, Examination
from datetime import date, datetime

logger = logging.getLogger(__name__)

class Extractor(object):

    def extract(self, instance):
        """
        return a dict with key patient and examination which gives some extract of the content,
        with list of dict which contains line number and the content.
        """
        result = {}

        extract_patient = self.extract_file(instance.file_patient)
        extract_examination = self.extract_file(instance.file_examination)

        result['patient'] = extract_patient
        result['examination'] = extract_examination

        return result

    def analyze(self, instance):
        """
        return a dict with key patient, and examination, which indicates if :
         - the expected file has the correct type.
         - the file is is_valid
         - the file is not is_empty
         - list of errors if found.
        """
        logger.info("* Analyze the instance")
        result = {}

        (type_file, is_valid, is_empty, errors) = self.analyze_file(instance.file_patient)
        result['patient'] = (type_file, is_valid, is_empty, errors)
        
        (type_file, is_valid, is_empty, errors) = self.analyze_file(instance.file_examination)
        result['examination'] = (type_file, is_valid, is_empty, errors)
        return result

    def analyze_file(self, file):
        if not bool(file) :
            return ('', False, True, [])
        logger.info("* Open the file %s "% (file.path))
        file.open(mode='rb')
        is_patient_file = False
        is_examination_file = False
        is_valid = True
        is_empty = False
        try :
            c = self.get_content(file)
            is_empty = c['nb_row'] <= 1
            header = c['header']
            logger.info(c)
            try :
                unicode(header[:]).lower().index('nom de famille')
                is_patient_file = True
            except ValueError:
                is_patient_file = False
            try:
                unicode(header[:]).lower().index('conclusion')
                is_examination_file = True
            except ValueError:
                is_examination_file = False
        except:
            logger.exception('Extractor failed.')
            is_valid = False
        
        if is_patient_file:
            return ('patient', is_valid, is_empty, [])
        if is_examination_file :
            return ('examination', is_valid, is_empty, [])
        else :
            return ('patient', False, True, [_('Cannot recognize the patient file')])

    def extract_file(self, file):
        if not bool(file) :
            return {}
        logger.info("* Open the file %s "% (file.path))
        result = {}
        file.open(mode='rb')
        try :
            c = self.get_content(file, as_line=False)
            nb_row = c['nb_row'] - 1
            if nb_row > 0:
                idx = sorted(random.sample(range(1, nb_row+1), min(5, nb_row)))
                logger.info("indexes = %s "% idx)
                for i in idx:
                    result['%s' % i] = c['content'][i-1]
        except:
            logger.exception('Extractor failed.')
        logger.info("result is %s" % result)
        return result

    def get_content(self, file, as_line=True):
        reader = self.get_reader(file)
        rownum = 0
        header = None
        content = []
        for row in reader:
            # Save header row.
            if rownum == 0:
                if not as_line:
                    header = [self.filter(r) for r in row]
                else :
                    header = unicode(row)
            else :
                if not as_line:
                    content.append([self.filter(r) for r in row])
                else :
                    content.append(unicode(row))
            rownum += 1
        file.close()
        return {
            'nb_row' : rownum ,
            'header' : header,
            'content' : content
        }

    def get_reader(self, file):
        if not bool(file):
            return None
        file.open(mode='rb')
        logger.info("* Try to guess the dialect on csv")
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        reader = csv.reader(file, dialect)
        return reader

    def filter(self, line):
        result_line = None
        try:
            result_line = line.decode('utf-8')
        except:
            pass
        if result_line is None :
            try:
                result_line = line.decode('iso-8859-1')
            except:
                result_line = _('Cannot read the content file. Check the encoding.')
        return result_line


class InvalidIntegrationFile(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class IntegratorHandler(object):
    def integrate(self, file, serializer_class=None):
        integrator = IntegratorFactory(serializer_class=serializer_class).get_instance(file)
        if integrator is None:
            raise InvalidIntegrationFile("This file %s is not valid to be integrated." % (file))

        result = integrator.integrate(file)
        return result
        

class IntegratorFactory(object):
    def __init__(self, serializer_class=None):
        self.extractor = Extractor()
        self.serializer_class = serializer_class
    def get_instance(self, file):
        result = self.extractor.analyze_file(file)
        if not result[1]:
            return None
        if result[0] == 'patient':
            return IntegratorPatient(serializer_class=self.serializer_class)
        elif result[0] == 'examination':
            return IntegratorExamination(serializer_class=self.serializer_class)

class AbstractIntegrator(object):
    def integrate(self, file):
        pass

class IntegratorPatient(AbstractIntegrator):
    def __init__(self, serializer_class=None):
        self.extractor = Extractor()
        self.serializer_class=serializer_class
    def integrate(self, file):
        content = self.extractor.get_content(file, as_line=False)
        nb_line = 0
        errors = []
        for idx, r in enumerate(content['content']):
            logger.info("* Load line from content")
            data = {
                'family_name' : r[1],
                'original_name' : r[2],
                'first_name' : r[3],
                'birth_date' : self.get_date(r[4]),
                'sex' : self.get_sex_value(r[5]),
                'address_street' : r[6],
                'address_complement' : r[7],
                'address_zipcode' : r[8],
                'address_city' : r[9],
                'phone' : r[10],
                'mobile_phone' : r[11],
                'job' : r[12],
                'hobbies' : r[13],
                'smoker'  : self.get_boolean_smoker(r[14]),
                'important_info' : r[15],
                'current_treatment' : r[16],
                'surgical_history' : r[17],
                'medical_history' : r[18],
                'family_history' : r[19],
                'trauma_history' : r[20],
                'medical_report' : r[21],
                'creation_date' : self.get_default_date(),
            }
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                nb_line += 1
            else :
                # idx + 2 because : we have header and the index start from 0
                # To have the line number we have to add 2 to the index....
                errors.append((idx+2, serializer.errors))
                logger.info("errors detected, data is = %s "% data)
        return ( nb_line, errors)
    
    def get_sex_value(self, value):
        if value.upper() == 'F':
            return 'F'
        else :
            return 'M'
    def get_boolean_smoker(self, value):
        if value.lower() == 'o' or value.lower() == 'oui' or value.lower() == 'true' or value.lower() == 't':
            return True
        else :
            return False
    def get_default_date(self):
        return date(2011, 01, 01)
    def get_date(self, value):
        f = "%d/%m/%Y"
        return datetime.strptime(value, f).date()

