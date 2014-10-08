class Statistics(object):
    def __init__(self, *args, **kwargs):
        # Initialize variable that it should be needed
        self.week_statistics = {
            'nb_new_patient':0,
            'nb_urgent_feedback':0,
            'nb_non_paid':0,
            'nb_examination':0}
        self.month_statistics = {
            'nb_new_patient':0,
            'nb_urgent_feedback':0,
            'nb_non_paid':0,
            'nb_examination':0
        }
        self.year_statistics = {
            'nb_new_patient':0,
            'nb_urgent_feedback':0,
            'nb_non_paid':0,
            'nb_examination':0
        }

    def compute(self):
        # Do some computation there
        result = {'week':self.week_statistics,
                  'month':self.month_statistics,
                  'year' : self.year_statistics}
        return result
