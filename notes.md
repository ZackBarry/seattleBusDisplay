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

