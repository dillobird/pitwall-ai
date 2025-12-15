import requests

VALID_PARAMS = {"driver_number", "session_key", "meeting_key"}

def get_drivers(**params):
    base_url = "https://api.openf1.org/v1/drivers"
    query = {k: v for k, v in params.items() if k in VALID_PARAMS and v is not None}
    resp = requests.get(base_url, params=query)
    resp.raise_for_status()
    return resp.json()