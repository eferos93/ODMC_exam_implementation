import os
import django
import pandas as pd

from space_missions.models import Country

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'models.settings')
django.setup()


# COUNTRY
def create_country(fields):
    return Country(code=fields[0], name=fields[1], continent=fields[2])


def collapse_rows_to_list(data_frame):
    return pd.Series(data_frame.values.tolist())


Country.objects.bulk_create(list(map(create_country, collapse_rows_to_list(pd.read_csv('Data/Country.csv')))))
