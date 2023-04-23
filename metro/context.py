from metro.load_csv import load_csv
from metro.util import filter_table

import io
import requests
import zipfile

CONTEXT_ZIP_URL = 'https://metro.kingcounty.gov/GTFS/google_transit.zip'

ASSET_FILE_NAMES = {
    'routes': './metro/data/routes.txt',
    'stops': './metro/data/stops.txt',
    'trips': './metro/data/trips.txt',
}


def download_context():
    resp = requests.get(CONTEXT_ZIP_URL)

    if not resp.ok:
        print(f'Error: {resp.status_code}: {str(resp)}')
        return None 
    
    z = zipfile.ZipFile(io.BytesIO(resp.content))

    for asset in ASSET_FILE_NAMES.values():
        zip_member_name = asset.split('/')[-1]
        zip_member_dir  = '/'.join(asset.split('/')[:-1])
        z.extract(zip_member_name, zip_member_dir)


def get_context(asset, filters=[]):
    context = load_csv(ASSET_FILE_NAMES[asset])

    for f in filters:
        context = filter_table(context, f['col'], f['value'], f['comparison'])
    
    return context
