from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=17, decimal_places=14)
    longitude = models.DecimalField(max_digits=17, decimal_places=14)

    def __str__(self):
        return f"{self.name}"


class Prediction(models.Model):
    LUCK_CHOICES = [
        ('대흉', '대흉'),
        ('흉', '흉'),
        ('평', '평'),
        ('길', '길'),
        ('대길', '대길'),
    ]

    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="predictions")
    timestamp = models.DateField()
    quality = models.PositiveSmallIntegerField()
    quantity = models.FloatField()
    luck = models.CharField(max_length=10, choices=LUCK_CHOICES)

    def __str__(self):
        return f"Prediction for {self.station.name} on {self.timestamp}"
