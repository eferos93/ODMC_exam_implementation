import os
from abc import ABC, abstractmethod

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django

django.setup()

import pandas as pd

from space_missions.models import (Country, Astronaut, Organisation)


class Populate(ABC):
    def __init__(self, data_frame_link, model):
        self.data_frame_link = data_frame_link
        self.model = model

    @abstractmethod
    def create_instance_of_model(self, fields):
        pass

    def collapse_rows_to_list(self, data_frame):
        return pd.Series(data_frame.values.tolist())

    def populate(self):
        self.model.objects.bulk_create(
            list(
                map(self.create_instance_of_model, self.collapse_rows_to_list(pd.read_csv(self.data_frame_link)))
            )
        )


# COUNTRY
class PopulateCountry(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(code=fields[0], name=fields[1], continent=fields[2])


class PopulateAstronaut(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(id=fields[0], name=fields[1],
                          original_name=fields[2], sex=fields[3],
                          year_of_birth=fields[4],
                          nationality=Country.objects.get(code__exact=fields[5]),
                          background=fields[6])


class PopulateOrganisation(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        print(fields)
        return self.model(code=fields[0],
                          name=fields[1], location=fields[2], longitude=fields[3],
                          latitude=fields[4], parent_organisation=None, english_name=fields[6],
                          country=Country.objects.get(code__exact=fields[7])
                          )


# PopulateCountry('Data/Country.csv', Country).populate()
# PopulateAstronaut('Data/Astronaut.csv', Astronaut).populate()
PopulateOrganisation('Data/Organisation.csv', Organisation).populate()