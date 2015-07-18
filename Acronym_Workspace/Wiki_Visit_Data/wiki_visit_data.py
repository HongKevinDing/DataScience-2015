__author__ = 'Hong (Kevin) Ding'
__status__ = "Production"
__date__ = "Jul 12, 2015"

from sets import Set
import ast
import requests
from lxml import html
from datetime import datetime

class WikiTitleVistMonthError(Exception):
    """
    Exception class for Structure.
    Raised when the WikiTitleVistMonth has problems, e.g., date does not exist
    """
    pass

class WikiTitleVistMonth():

    """
    Basic class for parsing the wiki title (url) visit during one particular month (format: YYYYMM) through http://stats.grok.se/
    """

    def __init__(self,title,month,lang):
        """
        Args:
            title : (TEXT)Enter a wikipedia article title
            month : (INTEGER)in the format of YYYYMM
            lang : (TEXT) must within dictionary
        """
        language_set = Set(['en','zh','de','ja'])
        url_prefix = 'http://stats.grok.se/json'
        self._month = month
        if lang in language_set:
            self._url = '%s/%s/%s/%s' % (url_prefix,lang, month,title)
            page = requests.get(self._url)
            self._monthly_data=ast.literal_eval(page.text)
    @property
    def url(self):
        return self._url

    @property
    def monthly_data(self):
        return self._monthly_data

    '''
    @property
    def monthly_view(self):
        return self_monthly_data['']
    '''


    def get_dayview(self,date):
        try:
            data_dictformat = datetime.strptime(str(self._month*100+date),"%Y%m%d").strftime("%Y-%m-%d")
        except:
            raise WikiTitleVistMonthError(("Date does not exist"))

        if self._monthly_data['daily_views'].has_key(data_dictformat):
            return self._monthly_data['daily_views'][data_dictformat]
        else:
            raise WikiTitleVistMonthError(("Date does not exist"))

    def get_monthview_sum(self):
        return reduce(lambda x,y:x+y,self._monthly_data['daily_views'].values())

    def get_monthview_average(self):
        return float(self.get_monthview_sum())/len(self._monthly_data['daily_views'])

    def get_monthview(self):
        return self._monthly_data['daily_views']

if __name__ == '__main__':
    for i in range(1, 13):
        print i, WikiTitleVistMonth('gold',2012*100+i,'en').get_monthview_sum()


## parse each