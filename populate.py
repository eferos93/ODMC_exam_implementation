import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django
django.setup()

import pandas as pd
from space_missions.models import Country


# COUNTRY
class PopulateCountry:
    @classmethod
    def create_country(cls, fields):
        return Country(code=fields[0], name=fields[1], continent=fields[2])

    @classmethod
    def collapse_rows_to_list(cls, data_frame):
        return pd.Series(data_frame.values.tolist())

    @classmethod
    def populate(cls):
        Country.objects.bulk_create(
            list(
                map(cls.create_country, cls.collapse_rows_to_list(pd.read_csv('Data/Country.csv')))
            )
        )
