# Covid-19 statistics in France
#
# this module retrieves regional data from a Github repository
# https://github.com/opencovid19-fr/data

from datetime import date
import urllib
import yaml

class FranceData:
    def __init__(self):
        self.loaded_data = {}
        self.config = yaml.safe_load(open('france.yaml').read())

    def load_latest(self):
        date = ''
        if self.config['forced_date']:
            date = self.config['forced_date']
        else:
            date = self.load_date(date.today().isoformat())
        self.load_date(date)

        result = self.loaded_data[date]
        result.pop('processed')
        result.pop('errors')

        return result

    def load_date(self, date):
        self.loaded_data[date] = {'processed': 0, 'errors': 0}
        for directory in self.config['region_directories']:
            self.load_region(date, directory)

    def load_region(self, date, region):
        try:
            region_data = yaml.safe_load(urllib.request.urlopen(self.config['url_template'].format(region=region, date=date)).read())
            self.loaded_data[date][region_data['donneesRegionales']['code']] = region_data
        except:
            self.loaded_data[date]['errors'] += 1

        self.loaded_data[date]['processed'] += 1
