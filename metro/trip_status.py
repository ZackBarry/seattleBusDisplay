from collections import defaultdict
import requests

TRIP_STATUS_URL = 'https://s3.amazonaws.com/kcm-alerts-realtime-prod/tripupdates_pb.json'


def download_trip_statuses():
    resp = requests.get(TRIP_STATUS_URL)

    if resp.status_code != 200:
        print(f'Error: {resp.status_code}: {str(resp)}')
        return []
    
    return resp.json()['entity']


def get_stop_statuses():
    trips = download_trip_statuses()

    stop_statuses = []

    for trip in trips:
        trip_update = trip["trip_update"]
        trip_details = trip_update["trip"]
        stop_updates = trip_update["stop_time_update"]

        for stop in stop_updates:
            stop_statuses.append({
                "trip_id":       int(trip_details["trip_id"]),
                "direction_id":  int(trip_details["direction_id"]),
                "route_id":      int(trip_details["route_id"]),
                "trip_status":   trip_details["schedule_relationship"],
                "stop_id":       int(stop["stop_id"]),
                "arrival_time":  int(stop.get("arrival", dict()).get("time", -1)),
                "arrival_delay": int(stop.get("arrival", dict()).get("delay", -1)),
                "stop_status":   stop["schedule_relationship"],
            })        
    
    return stop_statuses
