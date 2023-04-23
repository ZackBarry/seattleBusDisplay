from datetime import datetime

from metro.context import get_context
from metro.trip_status import get_stop_statuses
from metro.util import filter_table, table_to_dict

A = [
    26400, # "N 40th St & Wallingford Ave N" (Westbound)
    # 26965, # "N 40th St & Wallingford Ave N" (Eastbound)
    17310, # "N 45th St & Wallingford Ave N" (Westbound)
    # 17410, # "N 45th St & Wallingford Ave N" (Eastbound)
    # 7360,  # "Stone Way N & N 40th St" (Southbound)
]

B = [
    100224, # 44
    # 100252, # 62
    100184, # 31
    100193, # 32
]

HEADSIGN_DIR = {
    'University District': 'E',
    'Downtown Seattle Fremont': 'S',
    'University Of Washington Medical Center Wallingford': 'E',
    'Central Magnolia Fremont': 'S',
    'Ballard Wallingford': 'W',
    'Seattle Childrens Hospital U-District Station': 'N',
    'Sand Point East Green Lake': 'N',
    'Seattle Center Fremont': 'S',
}

STOP_PRINT_NAME = {
    'N 45th St & Wallingford Ave N': '45',
    'Stone Way N & N 43rd St': '43',
    'N 40th St & Wallingford Ave N': '40',
}

class Data:
    """
    If getting error 
        trip  = self.trips[status['trip_id']]
            KeyError: XXXXXXXX
    run metro.context.download_context() first
    """
    def __init__(self, stop_ids=A, route_ids=B):
        self.stop_ids  = stop_ids
        self.route_ids = route_ids

        stops = get_context(
            asset='stops',
            filters=[{
                'col': 'stop_id',
                'value': self.stop_ids,
                'comparison': 'is_one_of',
            }]
        )
        self.stops = table_to_dict(stops, 'stop_id')

        routes = get_context(
            asset='routes',
            filters=[{
                'col': 'route_id',
                'value': self.route_ids,
                'comparison': 'is_one_of',
            }]
        )
        self.routes = table_to_dict(routes, 'route_id')

        trips = get_context(
            asset='trips',
            filters=[{
                'col': 'route_id',
                'value': route_ids,
                'comparison': 'is_one_of',
            }]
        )
        self.trips = table_to_dict(trips, 'trip_id')
    
        self.stop_statuses = []
        self.update_stop_statuses()
    
    def format_stop_status(self, status):
        route = self.routes[status['route_id']]
        trip  = self.trips[status['trip_id']]
        stop  = self.stops[status['stop_id']]

        status['route_name'] = route['route_desc']
        status['route'] = route['route_short_name']
        status['headsign'] = trip['trip_headsign'].strip()
        status['stop_name'] = stop['stop_name']
        status['arrival_epoch'] = status['arrival_time']
        status['arrival_time'] = datetime.fromtimestamp(status['arrival_epoch']).strftime('%H-%M-%S')
        status['direction'] = HEADSIGN_DIR[status['headsign']]
        status['short_name'] = status['stop_name'] + status['direction']

        return status
    
    def update_stop_statuses(self):
        statuses = get_stop_statuses()

        for col, vals in zip(
            ['stop_id', 'route_id', 'trip_status', 'stop_status'],
            [self.stop_ids, self.route_ids, ['SCHEDULED'], ['SCHEDULED']] #['CANCELED'], ['SKIPPED']]  #
        ):
            statuses = filter_table(
                table=statuses,
                col=col,
                value=vals,
                comparison='is_one_of'
            )

        formatted = [
            self.format_stop_status(x) for x in statuses
            if int(x['arrival_time'] - datetime.now().timestamp()) > 0
        ]

        self.stop_statuses = sorted(formatted, key=lambda x: x['arrival_time'])


    def render_stop_status(x):
        sec_to_arrival = int(x['arrival_epoch'] - datetime.now().timestamp())

        seconds = sec_to_arrival % 60
        # seconds = seconds - (seconds % 5)
        seconds = str(seconds)
        if len(seconds) == 1:
            seconds = '0' + seconds
    
        minutes = str(sec_to_arrival // 60)
        if len(minutes) == 1:
            minutes = '0' + minutes
        elif len(minutes) > 2:
            minutes = '99'
        
        text = f"{x['short_name']} {minutes}:{seconds}"

        if x['arrival_delay'] > 60:
            status = 'delayed'
        elif x['arrival_delay'] < -60:
            status = 'ahead'
        else:
            status = 'on-time'

        return {
            'text': text,
            'status': status,
        }

    def get_specific_stop_statuses(self, short_name):
        statuses = filter_table(
            table=self.stop_statuses,
            col='short_name',
            value=short_name,
            comparison='equals'
        )
        return statuses

    def get_stop_status(self, index):
        if index >= len(self.stop_statuses):
            index = index % len(self.stop_statuses)
        
        x = self.stop_statuses[index]

        return self.render_stop_status(x)