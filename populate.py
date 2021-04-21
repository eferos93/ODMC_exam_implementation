import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django
django.setup()

import pandas as pd
from space_missions.models import (Country, Astronaut)


class Populate:
    @classmethod
    def collapse_rows_to_list(cls, data_frame):
        return pd.Series(data_frame.values.tolist())


# COUNTRY
class PopulateCountry(Populate):
    @classmethod
    def create_country(cls, fields):
        return Country(code=fields[0], name=fields[1], continent=fields[2])

    @classmethod
    def populate(cls):
        Country.objects.bulk_create(
            list(
                map(cls.create_country, cls.collapse_rows_to_list(pd.read_csv('Data/Country.csv')))
            )
        )

    @classmethod
    def update(cls):
        print([field.name for field in Country._meta.get_fields()])
        Country.objects.bulk_update(
            list(
                map(cls.create_country, cls.collapse_rows_to_list(pd.read_csv('Data/Country.csv')))
            ),
            fields=[field.name for field in Country._meta.get_fields()]
        )


class PopulateAstronaut(Populate):
    @classmethod
    def create_astronaut(cls, fields):
        print(fields)
        return Astronaut(id=fields[0], name=fields[1],
                         original_name=fields[2], sex=fields[3],
                         year_of_birth=fields[4],
                         nationality=Country.objects.get(code__exact=fields[5]),
                         background=fields[6])

    @classmethod
    def populate(cls):
        Astronaut.objects.bulk_create(
            list(
                map(cls.create_astronaut, cls.collapse_rows_to_list(pd.read_csv('Data/Astronaut.csv')))
            )
        )

PopulateCountry.update()
# PopulateAstronaut.populate()
