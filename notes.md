Trips can be SCHEDULED or CANCELED

Stops can be SCHEDULED or SKIPPED

CANCELED trips can be SKIPPED but not SCHEDULED
SCHEDULED trips can be either

```
stop_statuses = defaultdict(int)

for t in trips:
    tu = t["trip_update"]
    ts = tu["trip"]["schedule_relationship"]
    for stop in tu["stop_time_update"]:
        stop_statuses[f"{ts}: {stop['schedule_relationship']}"] += 1

{'SCHEDULED: SCHEDULED': 9768, 'CANCELED: SKIPPED': 8542, 'SCHEDULED: SKIPPED': 14}
```


arrival_time is epoch seconds to GMT

arrival_delay is in seconds

arrival_time takes into account arrival_delay

---

the `trip_headsign` and `direction_id` fields from `trips.txt` can be used together to assign a name for travel in each direction
```
route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,peak_flag,fare_id

100193,83193,535507942,"Seattle Center Fremont","LOCAL",0,6617997,31032002,0,101
100193,17345,535513532,"Seattle Childrens Hospital U-District Station","LOCAL",1,6618149,40032001,0,101
```
https://developers.google.com/transit/gtfs/reference#tripstxt