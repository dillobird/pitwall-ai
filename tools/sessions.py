import requests

VALID_PARAMS = {
    "location",
    "session_name",
    "year",
    "meeting_key",
    "circuit_key",
    "country_name",
}

def get_sessions(**params):
    base_url = "https://api.openf1.org/v1/sessions"
    query = {
        k: v for k, v in params.items()
        if k in VALID_PARAMS and v is not None
    }

    resp = requests.get(base_url, params=query)
    resp.raise_for_status()
    return resp.json()