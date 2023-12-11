from django.core.management.base import BaseCommand

from stations.models import Station, Prediction


class Command(BaseCommand):
    help = 'Drop database'

    def handle(self, *args, **options):
        try:
            Station.objects.all().delete()
            Prediction.objects.all().delete()  # just in case
            self.stdout.write(self.style.SUCCESS('Successfully deleted all Station instances'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
