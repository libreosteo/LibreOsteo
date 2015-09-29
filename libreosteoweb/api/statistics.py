from libreosteoweb.models import Patient, Examination
from datetime import date, timedelta
import copy

class Statistics(object):
    def __init__(self, *args, **kwargs):
        # Initialize variable that it should be needed
        self.week_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0}
        self.month_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        self.year_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }

    def get_start_of_the_week(self, current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        while d.weekday() != 0 :
            d = d - timedelta(days=1)
        return d

    def get_start_of_the_month(self, current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        d = d.replace(day=1)
        return d

    def get_start_of_the_year(self, current_date=None):
        if current_date is None :
            d = date.today()
        else:
            d = copy.copy(current_date)

        d = d.replace(day=1,month=1)
        return d

    def get_week_statistics(self, start_date=None, statistics_obj=None):
        if(start_date is None):
            start_date = date.today()
        if statistics_obj is None :
            statistics_obj = self.week_statistics
        return self.get_statistics(self.get_start_of_the_week(start_date), start_date, statistics_obj)

    def get_month_statistics(self, start_date=None, statistics_obj=None):
        if(start_date is None):
            start_date = date.today()
        if statistics_obj is None :
            statistics_obj = self.month_statistics
        return self.get_statistics(self.get_start_of_the_month(start_date), start_date, statistics_obj)

    def get_year_statistics(self, start_date=None, statistics_obj=None):
        if(start_date is None):
            start_date = date.today()
        if statistics_obj is None :
            statistics_obj = self.year_statistics
        return self.get_statistics(self.get_start_of_the_year(start_date), start_date, statistics_obj)

    def get_statistics(self, start_date, end_date, stats_obj):
        stats_obj['nb_new_patient'] = Patient.objects.filter(creation_date__gte= start_date, creation_date__lte=end_date).count()
        stats_obj['nb_examination'] = Examination.objects.filter(date__gte = start_date, date__lte=end_date).count()
        stats_obj['nb_urgent_return'] = Examination.objects.filter(date__gte = start_date, date__lte=end_date, type = 3).count()
        return stats_obj

    def get_history_week_statistics(self):

        start_date = date.today()
        week_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        history_week_statistics = { 
                'nb_new_patient' : [[],[]],
                'nb_examination' : [[],[]],
                'nb_urgent_return': [[],[]]
                }

        for i in range(1,12) :
            start_of_the_week = self.get_start_of_the_week(start_date)
            self.get_week_statistics(start_date, week_statistics)
            history_week_statistics['nb_new_patient'][0].append("%s - %s" % (start_of_the_week, start_date))
            history_week_statistics['nb_new_patient'][1].append(week_statistics['nb_new_patient'])
            history_week_statistics['nb_examination'][0].append("%s - %s" % (start_of_the_week, start_date))
            history_week_statistics['nb_examination'][1].append(week_statistics['nb_examination'])
            history_week_statistics['nb_urgent_return'][0].append("%s - %s" % (start_of_the_week, start_date))
            history_week_statistics['nb_urgent_return'][1].append(week_statistics['nb_urgent_return'])
            start_date = start_of_the_week - timedelta(days=8)

        history_week_statistics['nb_new_patient'][0]= history_week_statistics['nb_new_patient'][0][::-1]
        history_week_statistics['nb_new_patient'][1]= history_week_statistics['nb_new_patient'][1][::-1]
        history_week_statistics['nb_examination'][0]= history_week_statistics['nb_examination'][0][::-1]
        history_week_statistics['nb_examination'][1]= history_week_statistics['nb_examination'][1][::-1]
        history_week_statistics['nb_urgent_return'][0]= history_week_statistics['nb_urgent_return'][0][::-1]
        history_week_statistics['nb_urgent_return'][1]= history_week_statistics['nb_urgent_return'][1][::-1]
        return history_week_statistics

    def get_history_month_statistics(self):
        start_date = date.today()
        month_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        history_month_statistics = { 
                'nb_new_patient' : [[],[]],
                'nb_examination' : [[],[]],
                'nb_urgent_return': [[],[]]
                }

        for i in range(1,12) :
            start_of_the_month = self.get_start_of_the_month(start_date)
            self.get_month_statistics(start_date, month_statistics)
            history_month_statistics['nb_new_patient'][0].append("%s - %s" % (start_of_the_month, start_date))
            history_month_statistics['nb_new_patient'][1].append(month_statistics['nb_new_patient'])
            history_month_statistics['nb_examination'][0].append("%s - %s" % (start_of_the_month, start_date))
            history_month_statistics['nb_examination'][1].append(month_statistics['nb_examination'])
            history_month_statistics['nb_urgent_return'][0].append("%s - %s" % (start_of_the_month, start_date))
            history_month_statistics['nb_urgent_return'][1].append(month_statistics['nb_urgent_return'])
            start_date = start_of_the_month - timedelta(days=1)

        history_month_statistics['nb_new_patient'][0]= history_month_statistics['nb_new_patient'][0][::-1]
        history_month_statistics['nb_new_patient'][1]= history_month_statistics['nb_new_patient'][1][::-1]
        history_month_statistics['nb_examination'][0]= history_month_statistics['nb_examination'][0][::-1]
        history_month_statistics['nb_examination'][1]= history_month_statistics['nb_examination'][1][::-1]
        history_month_statistics['nb_urgent_return'][0]= history_month_statistics['nb_urgent_return'][0][::-1]
        history_month_statistics['nb_urgent_return'][1]= history_month_statistics['nb_urgent_return'][1][::-1]
        return history_month_statistics

    def get_history_year_statistics(self):
        start_date = date.today()
        year_statistics = {
            'nb_new_patient':0,
            'nb_urgent_return':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        history_year_statistics = { 
                'nb_new_patient' : [[],[]],
                'nb_examination' : [[],[]],
                'nb_urgent_return': [[],[]]
                }

        for i in range(1,12) :
            start_of_the_year = self.get_start_of_the_year(start_date)
            self.get_year_statistics(start_date, year_statistics)
            history_year_statistics['nb_new_patient'][0].append("%s - %s" % (start_of_the_year, start_date))
            history_year_statistics['nb_new_patient'][1].append(year_statistics['nb_new_patient'])
            history_year_statistics['nb_examination'][0].append("%s - %s" % (start_of_the_year, start_date))
            history_year_statistics['nb_examination'][1].append(year_statistics['nb_examination'])
            history_year_statistics['nb_urgent_return'][0].append("%s - %s" % (start_of_the_year, start_date))
            history_year_statistics['nb_urgent_return'][1].append(year_statistics['nb_urgent_return'])
            start_date = start_of_the_year - timedelta(days=1)

        history_year_statistics['nb_new_patient'][0]= history_year_statistics['nb_new_patient'][0][::-1]
        history_year_statistics['nb_new_patient'][1]= history_year_statistics['nb_new_patient'][1][::-1]
        history_year_statistics['nb_examination'][0]= history_year_statistics['nb_examination'][0][::-1]
        history_year_statistics['nb_examination'][1]= history_year_statistics['nb_examination'][1][::-1]
        history_year_statistics['nb_urgent_return'][0]= history_year_statistics['nb_urgent_return'][0][::-1]
        history_year_statistics['nb_urgent_return'][1]= history_year_statistics['nb_urgent_return'][1][::-1]
        return history_year_statistics

    def compute(self):
        # Do some computation there
        result = {'week':  self.get_week_statistics(),
                  'month': self.get_month_statistics(),
                  'year' : self.get_year_statistics(),
                  'history': {
                    'week': self.get_history_week_statistics(),
                    'month': self.get_history_month_statistics(),
                    'year': self.get_history_year_statistics()
                  }
                }
        return result
