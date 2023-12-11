from rest_framework import serializers

from stations.models import Station, Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class MyeongdangSerializer(serializers.ModelSerializer):
    avg_quality = serializers.FloatField()
    avg_quantity = serializers.FloatField()
    luck = serializers.CharField()

    class Meta:
        model = Station
        fields = ['id', 'name', 'latitude', 'longitude', 'avg_quality', 'avg_quantity', 'luck']
