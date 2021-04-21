import os
from abc import ABC, abstractmethod

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django

django.setup()

import pandas as pd

from space_missions.models import (Country, Astronaut, Organisation, Engine)


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
        return self.model(code=fields[0],
                          name=fields[1], location=fields[2], longitude=fields[3],
                          latitude=fields[4], parent_organisation=None, english_name=fields[6],
                          country=Country.objects.get(code__exact=fields[7])
                          )

    def update_parent_organisation(self, fields):
        print(fields)
        model_entry = self.model.objects.get(pk=fields[0])
        if fields[5] is not None:
            model_entry.parent_organisation = self.model.objects.get(pk=fields[5])
            model_entry.save()
        # model_entry.parent_organisation = self.model.objects.get(pk=fields[5]) if (fields[5] != 'nan' or fields[5] is not None) else None

    def update(self):
        data_frame = pd.read_csv(self.data_frame_link)
        # map(self.update_parent_organisation, self.collapse_rows_to_list(pd.read_csv(self.data_frame_link)))
        for _, value in self.collapse_rows_to_list(data_frame[data_frame.parent.notnull()]).items():
            self.update_parent_organisation(value)


class PopulateEngines(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        print(fields)
        return self.model(name=fields[0], manufacturer=Organisation.objects.get(pk__exact=fields[1]), mass=fields[2],
                          impulse=fields[3], thrust=fields[4], isp=fields[5], burn_duration=fields[6],
                          chambers=fields[7])

# PopulateCountry('Data/Country.csv', Country).populate()
# PopulateAstronaut('Data/Astronaut.csv', Astronaut).populate()
# PopulateOrganisation('Data/Organisation.csv', Organisation).populate()
# PopulateOrganisation('Data/Organisation.csv', Organisation).update()
# PopulateEngines('Data/Engine.csv', Engine).populate()
