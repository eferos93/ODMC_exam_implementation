import os
from abc import ABC, abstractmethod

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ODMC_exam_implementation.settings')
import django

django.setup()

import pandas as pd

from space_missions.models import (Country, Astronaut, Organisation, Engine, Mission, Launch, Selection, Stage,
                                   LaunchVehicle, AstronautSelection, AstronautOccupation, VehicleStage)


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
        return self.model(astronaut_id=fields[0], name=fields[1],
                          original_name=fields[2], sex=fields[3],
                          birth_year=fields[4],
                          nationality=Country.objects.get(code__exact=fields[5]),
                          background=fields[6])


class PopulateOrganisation(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        print(fields)
        country = None if pd.isnull(fields[7]) else Country.objects.get(code__exact=fields[7])
        return self.model(code=fields[0],
                          name=fields[1], location=fields[2], longitude=fields[3],
                          latitude=fields[4], parent_organisation=None, english_name=fields[6],
                          country=country
                          )

    def update_parent_organisation(self, fields):
        print(fields)
        model_entry = self.model.objects.get(code__exact=fields[0])
        if fields[5] is not None:
            try:
                model_entry.parent_organisation = self.model.objects.get(code__exact=fields[5])
                model_entry.save()
            except self.model.DoesNotExist:
                model_entry.parent_organisation = None
                model_entry.save()


    def update(self):
        data_frame = pd.read_csv(self.data_frame_link)
        for _, value in self.collapse_rows_to_list(data_frame[data_frame.parent.notnull()]).items():
            self.update_parent_organisation(value)


class PopulateEngines(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[0], manufacturer=Organisation.objects.get(code__exact=fields[1]), mass=fields[2],
                          impulse=fields[3], thrust=fields[4], isp=fields[5], burn_duration=fields[6],
                          chambers=fields[7])


class PopulateLaunch(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(launch_id=fields[0], date=fields[1],
                          organisation=Organisation.objects.get(code__exact=fields[3]),
                          launch_type=fields[4], success_or_fail=fields[5])

    def update_vehicle(self):
        for _, row in pd.read_csv(self.data_frame_link).iterrows():
            launch = self.model.objects.get(launch_id__exact=row['launch_id'])
            lv = None if pd.isnull(row['launch_vehicle']) else LaunchVehicle.objects.get(
                name__exact=row['launch_vehicle']
            )
            launch.launch_vehicle = lv
            launch.save()


class PopulateMission(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[1], launch=Launch.objects.get(launch_id__exact=fields[0]))


class PopulateSelection(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(name=fields[0])

    def populate(self):
        for selection in pd.read_csv(self.data_frame_link)['selection'].drop_duplicates():
            model_instance = self.model(name=selection)
            model_instance.save()

    def update_mission_field(self):
        for _, row in pd.read_csv(self.data_frame_link).iterrows():
            entry = self.model.objects.get(name__exact=row['selection'])
            entry.missions.add(Mission.objects.get(name__exact=row['mission']))
            entry.save()


class PopulateStage(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        engine = None if pd.isnull(fields[8]) else Engine.objects.get(name__exact=fields[8])
        manufacturer = None if pd.isnull(fields[1]) else Organisation.objects.get(code__exact=fields[1])
        return self.model(name=fields[0], manufacturer=manufacturer,
                          length=fields[2], diameter=fields[3], launch_mass=fields[4],
                          dry_mass=fields[5], thrust=fields[6], burn_duration=fields[7],
                          engine=engine)


class PopulateAstronautSelection(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(astronaut=Astronaut.objects.get(astronaut_id__exact=fields[0]),
                          selection=Selection.objects.get(name__exact=fields[1]),
                          selection_year=fields[2])


class PopulateAstronautOccupation(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        return self.model(astronaut=Astronaut.objects.get(astronaut_id__exact=fields[0]),
                          mission=Mission.objects.get(name__exact=fields[1]),
                          role=fields[2], join_year=fields[3])


class PopulateLaunchVehicle(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        organisation = None if pd.isnull(fields[1]) else Organisation.objects.get(code__exact=fields[1])
        return self.model(name=fields[0],
                          manufacturer=organisation,
                          min_stage=fields[2],
                          max_stage=fields[3], length=fields[4], diameter=fields[5],
                          launch_mass=fields[6], TO_thrust=fields[7], vehicle_class=fields[8])


class PopulateVehicleStage(Populate):
    def __init__(self, data_frame_link, model):
        super().__init__(data_frame_link, model)

    def create_instance_of_model(self, fields):
        stage = None if pd.isnull(fields[2]) else Stage.objects.get(name__exact=fields[2])
        return self.model(launch_vehicle=LaunchVehicle.objects.get(name__exact=fields[0]),
                          stage_number=fields[1],
                          stage=stage,
                          dummy=fields[3])

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
# PopulateLaunchVehicle('Data/LaunchVehicle.csv', LaunchVehicle).populate()
# PopulateLaunch('Data/Launch.csv', Launch).update_vehicle()
# PopulateVehicleStage('Data/VehicleStage.csv', VehicleStage).populate()
# ---------------------------------------------------
