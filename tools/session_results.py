import requests

VALID_PARAMS = {"session_key", "position", "driver_number"}

def get_session_result(**params):
    base_url = "https://api.openf1.org/v1/session_result"
    query = {k: v for k, v in params.items() if k in VALID_PARAMS and v is not None}
    resp = requests.get(base_url, params=query)
    resp.raise_for_status()
    return resp.json()
