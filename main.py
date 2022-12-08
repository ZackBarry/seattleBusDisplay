from context import download_context, get_context
from trip_status import get_stop_statuses
from util import filter_table

from datetime import datetime


STOPS_OF_INTEREST = [
    26400, # "N 40th St & Wallingford Ave N" (Westbound)
    26965, # "N 40th St & Wallingford Ave N" (Eastbound)
    17310, # "N 45th St & Wallingford Ave N" (Westbound)
    17410, # "N 45th St & Wallingford Ave N" (Eastbound)
    7360,  # "Stone Way N & N 40th St" (Southbound)
]

ROUTES_OF_INTEREST = [
    100224, # 44
    100252, # 62
    100184, # 31
    100193, # 32
]

if __name__ == "__main__":
    download_context()

    stop_statuses = get_stop_statuses()

    interested = filter_table(
        table=stop_statuses, 
        col='stop_id', 
        value=STOPS_OF_INTEREST, 
        comparison='is_one_of',
    )

    interested = filter_table(
        table=interested,
        col='route_id',
        value=ROUTES_OF_INTEREST,
        comparison='is_one_of',
    )

    interested = filter_table(
        table = interested,
        col='trip_status',
        value='SCHEDULED',
    )

    interested = filter_table(
        table = interested,
        col='stop_status',
        value='SCHEDULED',
    )

    for x in interested:
        route_details = get_context(
            asset='routes',
            filters=[{
                'col': 'route_id',
                'value': x['route_id'],
                'comparison': 'equals'
            }]
        )[0]

        x['route_name'] = route_details['route_desc']

        x['route'] = route_details['route_short_name']
        

        stop_details = get_context(
            asset='stops',
            filters=[{
                'col': 'stop_id',
                'value': x['stop_id'],
                'comparison': 'equals'
            }]
        )[0]

        x["stop_name"] = stop_details["stop_name"]

        x['arrival_time'] = datetime.fromtimestamp(x['arrival_time']).strftime('%H-%M-%S')
    

    for x in sorted(interested, key=lambda x: x['route_id']):
        print(f"{x['route'], x['stop_name'], x['arrival_time'], x['arrival_delay']}")
