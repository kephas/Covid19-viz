# Covid-19 statistics in France
#
# this module retrieves regional data from a Github repository
# https://github.com/opencovid19-fr/data

import datetime
import copy
import urllib
import yaml
import pdb

class FranceData:
    def __init__(self):
        self.loaded_data = {}
        self.config = yaml.load(open('france.yaml').read()) or {}

    def latest_date(self):
        if self.config.get('forced_date'):
            return self.config['forced_date']
        else:
            return self.load_date(date.today().isoformat())

    def load_latest_single(self):
        latest_date = self.latest_date()
        self.load_single_date(latest_date)
        return self.clean_data()[latest_date]

    def load_latest_consolidated(self):
        latest_date = self.latest_date()
        self.load_consolidated_date(latest_date)
        return self.clean_data()

    def load_consolidated_date(self, last_date):
        self.load_single_date(last_date)
        if len(self.loaded_data[last_date]['errors']) > 0:
            self.load_single_date(self.date_before(last_date))

    def load_single_date(self, date):
        self.loaded_data[date] = {'processed': 0, 'errors': []}
        for directory in self.config['region_directories']:
            self.load_region(date, directory)

    def load_region(self, date, region):
        try:
            region_data = yaml.safe_load(urllib.request.urlopen(self.config['url_template'].format(region=region, date=date)).read())
            self.loaded_data[date][region_data['donneesRegionales']['code']] = region_data
        except:
            self.loaded_data[date]['errors'].append(region)

        self.loaded_data[date]['processed'] += 1

    def clean_data(self):
        result = copy.deepcopy(self.loaded_data)
        for date in result.keys():
            result[date].pop('processed')
            result[date].pop('errors')
        return result

    def date_before(self, date):
        return (datetime.date.fromisoformat(date) - datetime.timedelta(1)).isoformat()
