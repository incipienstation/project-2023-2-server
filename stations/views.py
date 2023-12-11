from django.db.models import Sum, Count, FloatField, Subquery, OuterRef
from django.db.models.functions import Cast
from rest_framework import generics

from stations.models import Station, Prediction
from stations.serializers import StationSerializer, PredictionSerializer, MyeongdangSerializer


class StationListView(generics.ListAPIView):
    def get_serializer_class(self):
        return MyeongdangSerializer if self.request.query_params.get('year', False) else StationSerializer

    def get_queryset(self):
        year = self.request.query_params.get('year', False)

        if year:
            # Top 10 stations of the year
            top_stations = (
                Station.objects
                .filter(predictions__timestamp__year=year)
                .annotate(avg_quality=Cast(Sum('predictions__quality'), FloatField()) / Count('predictions'),
                          avg_quantity=Sum('predictions__quantity') / Count('predictions'),
                          luck=Subquery(
                              Prediction.objects
                              .filter(station=OuterRef('pk'), timestamp__year=year)[:1]
                              .values('luck')
                          ))
                .order_by('avg_quality', '-avg_quantity')[:10]
            )
            return top_stations

        else:
            # List all stations
            return Station.objects.all()


class StationDetailView(generics.RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class PredictionListView(generics.ListAPIView):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.filter(station__id=self.kwargs.get('station_id')).order_by('timestamp')
