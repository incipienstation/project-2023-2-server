from django.urls import path

from stations.views import StationListView, StationDetailView, PredictionListView

urlpatterns = [
    path('stations/', StationListView.as_view(), name='station-list'),
    path('stations/<int:pk>/', StationDetailView.as_view(), name='station-detail'),
    path('stations/<int:station_id>/predictions/', PredictionListView.as_view(), name='prediction-list'),
]
