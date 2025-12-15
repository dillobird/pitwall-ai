import requests

VALID_PARAMS = {"session_key", "driver_number", "date_gt", "date_lt"}

def get_locations(**params):
    base_url = "https://api.openf1.org/v1/location"
    query = {k: v for k, v in params.items() if k in VALID_PARAMS and v is not None}
    resp = requests.get(base_url, params=query)
    resp.raise_for_status()
    return resp.json()
