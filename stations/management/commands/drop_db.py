from django.core.management.base import BaseCommand

from stations.models import Station


class Command(BaseCommand):
    help = 'Drop database'

    def handle(self):
        Station.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data drop completed successfully.'))
