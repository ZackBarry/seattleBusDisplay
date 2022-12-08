from load_csv import load_csv
from util import filter_table

from datetime import datetime
import io
import os
import requests
import zipfile


CONTEXT_ZIP_URL = 'https://metro.kingcounty.gov/GTFS/google_transit.zip'

ASSET_FILE_NAMES = {
    'agency': './data/context/current/agency.txt',
    'routes': './data/context/current/routes.txt',
    'stops': './data/context/current/stops.txt',
    'trips': './data/context/current/trips.txt',
}


def download_context():
    resp = requests.get(CONTEXT_ZIP_URL)
    time = int(datetime.now().strftime('%s'))

    if not resp.ok:
        print(f'Error: {resp.status_code}: {str(resp)}')
        return None 
    
    z = zipfile.ZipFile(io.BytesIO(resp.content))

    os.makedirs('./tmp', exist_ok=True)

    z.extractall(f'./data/context/{time}')
    z.extractall(f'./data/context/current')


def get_context(asset, filters=[]):
    context = load_csv(ASSET_FILE_NAMES[asset])

    for f in filters:
        context = filter_table(context, f['col'], f['value'], f['comparison'])
    
    return context
