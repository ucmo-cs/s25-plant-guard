import requests
from sensors.models import Pi
from datetime import datetime

def fetch_and_store_pi_data():
    try:
        pi_url = "http://192.168.1.77:5000/data"
        print(f"[DEBUG] Fetching from: {pi_url}")

        response = requests.get(pi_url, timeout=5)
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Raw Response: {response.text}")

        response.raise_for_status()
        data = response.json()

        print(f"[DEBUG] Parsed JSON: {data}")

        timestamp = datetime.strptime(data['timestamp'], "%a, %d %b %Y %H:%M:%S %Z")

        Pi.objects.create(
            pi_id=data['pieId'],
            gas_resistance=data['gas resistance'],
            humidity=data['humidity'],
            lux=data['lux'],
            pressure=data['pressure'],
            rawVal=data['rawVal'],
            temperature=data['temperature'],
            timestamp=timestamp,
            volts=data['volts']
        )

        print("[DEBUG] Successfully saved data.")
        return True

    except requests.RequestException as e:
        print(f"[ERROR] RequestException: {e}")
        return False

    except KeyError as e:
        print(f"[ERROR] Missing expected key: {e}")
        return False

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False
