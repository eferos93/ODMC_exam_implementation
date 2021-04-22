import os
from abc import ABC, abstractmethod
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django

django.setup()

import pandas as pd

from space_missions.models import (Country, Astronaut, Organisation, Engine, Mission, Launch, Selection, Stage,
                                   AstronautSelection, AstronautOccupation)


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
        model_entry = self.model.objects.get(pk=fields[0])
        if fields[5] is not None:
            model_entry.parent_organisation = self.model.objects.get(pk=fields[5])
            model_entry.save()

    def update(self):
        data_frame = pd.read_csv(self.data_frame_link)
        for _, value in self.collapse_rows_to_list(data_frame[data_frame.parent.notnull()]).items():
            self.update_parent_organisation(value)


class PopulateEngines(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[0], manufacturer=Organisation.objects.get(pk__exact=fields[1]), mass=fields[2],
                          impulse=fields[3], thrust=fields[4], isp=fields[5], burn_duration=fields[6],
                          chambers=fields[7])


class PopulateLaunch(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(id=fields[0], date=fields[1],
                          organisation=Organisation.objects.get(pk=fields[3]),
                          type_of_launch=fields[4], success_or_fail=fields[5])


class PopulateMission(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[1], launch=Launch.objects.get(pk__exact=fields[0]))


class PopulateSelection(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[0])

    def populate(self):
        data_frame = pd.read_csv(self.data_frame_link)
        data_frame = data_frame['selection'].drop_duplicates()
        for selection in data_frame:
            model_instance = self.model(name=selection)
            model_instance.save()

    def update_mission_field(self):
        for _, row in pd.read_csv(self.data_frame_link).iterrows():
            entry = self.model.objects.get(pk__exact=row['selection'])
            entry.missions.add(Mission.objects.get(pk__exact=row['mission']))
            entry.save()


class PopulateStage(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        fields[8] = None if pd.isnull(fields[8]) else Engine.objects.get(pk__exact=fields[8])
        fields[1] = None if pd.isnull(fields[1]) else Organisation.objects.get(pk__exact=fields[1])
        return self.model(name=fields[0], manufacturer=fields[1],
                          length=fields[2], diameter=fields[3], launch_mass=fields[4],
                          dry_mass=fields[5], thrust=fields[6], burn_duration=fields[7],
                          engine=fields[8])


class PopulateAstronautSelection(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(astronaut=Astronaut.objects.get(pk__exact=fields[0]),
                          selection=Selection.objects.get(pk__exact=fields[1]),
                          year_of_selection=fields[2])


class PopulateAstronautOccupation(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(astronaut=Astronaut.objects.get(pk__exact=fields[0]),
                          mission=Mission.objects.get(pk__exact=fields[1]),
                          role=fields[2], year_of_join=fields[3])


# DONE --------------------------------------------------
# PopulateCountry('Data/Country.csv', Country).populate()
# PopulateAstronaut('Data/Astronaut.csv', Astronaut).populate()
# PopulateOrganisation('Data/Organisation.csv', Organisation).populate()
# PopulateOrganisation('Data/Organisation.csv', Organisation).update()
# PopulateEngines('Data/Engine.csv', Engine).populate()
# PopulateLaunch('Data/Launch.csv', Launch).populate()
# PopulateMission('Data/Mission.csv', Mission).populate()
# PopulateSelection('Data/Selection.csv', Selection).populate()
# PopulateSelection('Data/Selection.csv', Selection).update_mission_field()
# PopulateStage('Data/Stage.csv', Stage).populate()
# PopulateAstronautSelection('Data/AstronautSelection.csv', AstronautSelection).populate()
# PopulateAstronautOccupation('Data/AstronautOccupation.csv', AstronautOccupation).populate()
# ---------------------------------------------------
