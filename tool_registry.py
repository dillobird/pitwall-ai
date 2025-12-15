import json
from tools.sessions import get_sessions
from tools.drivers import get_drivers
from tools.locations import get_locations
from tools.meetings import get_meetings
from tools.session_results import get_session_result

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_sessions",
            "description": "Get F1 sessions from OpenF1 API using any combination of parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "session_name": {"type": "string"},
                    "year": {"type": "integer"},
                    "meeting_key": {"type": "integer"},
                    "circuit_key": {"type": "integer"},
                    "country_name": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "strict": False,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_drivers",
            "description": "Get driver metadata for a session or meeting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "driver_number": {"type": "integer"},
                    "session_key": {"type": "string"},
                    "meeting_key": {"type": "integer"}
                },
                "additionalProperties": False,
            },
            "strict": False,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_location",
            "description": "Get car location data for a session (track coordinates).",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_key": {"type": "string"},
                    "driver_number": {"type": "integer"},
                    "date_gt": {"type": "string"},
                    "date_lt": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "strict": False,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_meetings",
            "description": "Get meetings (race weekends) by filter.",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {"type": "integer"},
                    "meeting_key": {"type": "integer"},
                    "country_name": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "strict": False,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_session_result",
            "description": "Get results data for a specific session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_key": {"type": "string"},
                    "position": {"type": "integer"},
                    "driver_number": {"type": "integer"},
                },
                "additionalProperties": False,
            },
            "strict": False,
        },
    },
]

def call_tool(name, arguments_json):
    args = json.loads(arguments_json)

    if name == "get_sessions":
        return get_sessions(**args)
    if name == "get_drivers":
        return get_drivers(**args)
    if name == "get_location":
        return get_location(**args)
    if name == "get_meetings":
        return get_meetings(**args)
    if name == "get_session_result":
        return get_session_result(**args)

    return {"error": f"Unknown tool {name}"}
