
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
from libreosteoweb.models import Patient, Examination
from datetime import date, timedelta
import datetime
import copy

class Statistics(object):
    def __init__(self, *args, **kwargs):
        # Initialize variable that it should be needed
        self.sub_classes_period = dict(week=WeekPeriod,month=MonthPeriod,year=YearPeriod)
        self.subclass = None

    def define_period_subclass(self, selector=None):
        if selector is None :
            self.subclass = self.sub_classes_period["week"]
        else :
            self.subclass = self.sub_classes_period[selector]
        return self.get_subclass()

    def get_subclass(self):
        return self.subclass

    def get_statistics(self, start_date=None, statistics_obj=None):
        if(start_date is None):
            start_date = date.today()
        if statistics_obj is None :
            statistics_obj = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0}
        period = self.subclass()
        return self.compute_statistics(period.get_start_of_period(start_date), datetime.datetime.combine(start_date, datetime.time.max), statistics_obj)

    def compute_statistics(self, start_date, end_date, stats_obj):
        stats_obj['nb_new_patient'] = Patient.objects.filter(creation_date__gte= start_date, creation_date__lte=end_date).count()
        stats_obj['nb_examination'] = Examination.objects.filter(date__gte = start_date, date__lte=end_date).count()
        stats_obj['nb_urgent_return'] = Examination.objects.filter(date__gte = start_date, date__lte=end_date, type = 3).count()
        return stats_obj

    def get_history_statistics(self):

        end_date = date.today()
        obj_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        history_statistics = { 
                'nb_new_patient' : [[],[]],
                'nb_examination' : [[],[]],
                'nb_urgent_return': [[],[]]
                }
        period = self.subclass()
        for i in range(1,12) :
            start_of_the_period = period.get_start_of_period(end_date)
            self.get_statistics(end_date, obj_statistics)
            history_statistics['nb_new_patient'][0].append("%s - %s" % (start_of_the_period, end_date))
            history_statistics['nb_new_patient'][1].append(obj_statistics['nb_new_patient'])
            history_statistics['nb_examination'][0].append("%s - %s" % (start_of_the_period, end_date))
            history_statistics['nb_examination'][1].append(obj_statistics['nb_examination'])
            history_statistics['nb_urgent_return'][0].append("%s - %s" % (start_of_the_period, end_date))
            history_statistics['nb_urgent_return'][1].append(obj_statistics['nb_urgent_return'])
            end_date = start_of_the_period - timedelta(days=period.get_timedelta_of_period())

        history_statistics['nb_new_patient'][0]= history_statistics['nb_new_patient'][0][::-1]
        history_statistics['nb_new_patient'][1]= history_statistics['nb_new_patient'][1][::-1]
        history_statistics['nb_examination'][0]= history_statistics['nb_examination'][0][::-1]
        history_statistics['nb_examination'][1]= history_statistics['nb_examination'][1][::-1]
        history_statistics['nb_urgent_return'][0]= history_statistics['nb_urgent_return'][0][::-1]
        history_statistics['nb_urgent_return'][1]= history_statistics['nb_urgent_return'][1][::-1]
        return history_statistics

    def compute(self):
        # Do some computation there
        result = {'week':  None,
                  'month': None,
                  'year' : None,
                  'history': {
                    'week': None,
                    'month': None,
                    'year': None
                  }
                }
        for period in ['week', 'month', 'year']:
            # Compute on the period
            self.define_period_subclass(period)
            result[period] = self.get_statistics()
            result['history'][period] = self.get_history_statistics()
        return result


class WeekPeriod(object):
    def get_start_of_period(self,current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        while d.weekday() != 0 :
            d = d - timedelta(days=1)
        return d

    def get_timedelta_of_period(self):
        # 8 days to backward a week
        return 8

class MonthPeriod(object):
    def get_start_of_period(self,current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        d = d.replace(day=1)
        return d

    def get_timedelta_of_period(self):
        # 1 day from the start of the month to backward to last day of the previous month
        return 1

class YearPeriod(object):
    def get_start_of_period(self,current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        d = d.replace(day=1,month=1)
        return d

    def get_timedelta_of_period(self):
        #1 day from the start of the year to backward to last day of the previous year
        return 1
