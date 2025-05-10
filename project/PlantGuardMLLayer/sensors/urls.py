from django.urls import path
from .views import FetchPiSensorDataView, LatestPiDataView


urlpatterns = [
   path('fetch/', FetchPiSensorDataView.as_view(), name='fetch-pi-data'), 
   path('latest/', LatestPiDataView.as_view(), name='latest-pi-data'),
    
]
