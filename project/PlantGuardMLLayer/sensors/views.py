from rest_framework.views import APIView
from rest_framework.response import Response
from sensors.models import Pi
from sensors.services import fetch_and_store_pi_data


class FetchPiSensorDataView(APIView):
    def post(self, request):
        success = fetch_and_store_pi_data()
        if success:
            return Response({"message": "Data fetched and saved!"})
        else:
            return Response({"error": "Failed to fetch or save data"}, status=500)

    def get(self, request):
        latest = Pi.objects.last()
        if latest:
            return Response({
                "pi_id": latest.pi_id,
                "gas_resistance": latest.gas_resistance,
                "humidity": latest.humidity,
                "lux": latest.lux,
                "pressure": latest.pressure,
                "rawVal": latest.rawVal,
                "temperature": latest.temperature,
                "timestamp": latest.timestamp,
                "volts": latest.volts,
            })
        else:
            return Response({"message": "No sensor data found"}, status=404)

class LatestPiDataView(APIView):
    def get(self, request):
        limi = int(request.query_params.get('limit', 10))
        
        recent_data = Pi.objects.all().order_by('-timestamp')[:limit]

        results = []
        for entry in recent_data:
            results.append({
                "pi_id": entry.pi_id,
                "gas_resistance": entry.gas_resistance,
                "humidity": entry.humidity,
                "lux": entry.lux,
                "pressure": entry.pressure,
                "rawVal": entry.rawVal,
                "temperature": entry.temperature,
                "timestamp": entry.timestamp,
                "volts": entry.volts,
            })
        return Response(results)
