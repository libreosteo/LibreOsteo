from libreosteoweb.models import Patient, Examination
from datetime import date, timedelta

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

    def get_start_of_the_week(self):
        d = date.today()
        while d.weekday() != 0 :
            d = d - timedelta(days=1)
        return d

    def get_start_of_the_month(self):
        d = date.today()
        d = d.replace(day=1)
        return d

    def get_start_of_the_year(self):
        d = date.today()
        d = d.replace(day=1,month=1)
        return d

    def get_week_statistics(self):
        return self.get_statistics(self.get_start_of_the_week(), self.week_statistics)

    def get_month_statistics(self):
        return self.get_statistics(self.get_start_of_the_month(), self.month_statistics)

    def get_year_statistics(self):
        return self.get_statistics(self.get_start_of_the_year(), self.year_statistics)

    def get_statistics(self, limit_date, stats_obj):
        stats_obj['nb_new_patient'] = Patient.objects.filter(creation_date__gte= limit_date).count()
        stats_obj['nb_examination'] = Examination.objects.filter(date__gte = limit_date).count()
        stats_obj['nb_urgent_return'] = Examination.objects.filter(date__gte = limit_date).filter(type = 3).count()
        return stats_obj

    def compute(self):
        # Do some computation there
        result = {'week':  self.get_week_statistics(),
                  'month': self.get_month_statistics(),
                  'year' : self.get_year_statistics()
                }
        return result
