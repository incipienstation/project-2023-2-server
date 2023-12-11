import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from stations.models import Station, Prediction


class Command(BaseCommand):
    help = 'Populate database with sample static'

    def read_csv_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def populate_stations(self, stations_data):
        for station_data in stations_data:
            Station.objects.create(
                name=station_data.get('name'),
                latitude=station_data.get('latitude'),
                longitude=station_data.get('longitude')
            )

    def populate_predictions(self, predictions_data):
        for prediction_data in predictions_data:
            station_name = prediction_data.get('station')
            timestamp_str = prediction_data.get('timestamp')

            try:
                station = Station.objects.get(name=station_name)
            except Station.DoesNotExist:
                self.stderr.write(f"Station with name '{station_name}' not found. Skipping prediction creation.")
                continue

            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
            except ValueError:
                self.stderr.write(f"Invalid timestamp format for prediction. Skipping prediction creation.")
                continue

            if prediction_data.get('luck') in ('대흉', '흉', '평', '길', '대길'):
                Prediction.objects.create(
                    station=station,
                    timestamp=timestamp,
                    # quantity=prediction_data.get('quantity'), # for debugging
                    quantity=0,
                    quality=prediction_data.get('quality'),
                    luck=prediction_data.get('luck')
                )

    def handle(self, *args, **options):
        stations_filename = options.get('stations_file', 'static/stations_final.csv')
        predictions_filename = options.get('predictions_file', 'static/predictions_final.csv')

        stations_data = self.read_csv_file(stations_filename)
        predictions_data = self.read_csv_file(predictions_filename)

        self.populate_stations(stations_data)
        self.populate_predictions(predictions_data)

        self.stdout.write(self.style.SUCCESS('Data population completed successfully.'))
