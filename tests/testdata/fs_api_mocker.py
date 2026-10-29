import json
import os
from unittest.mock import MagicMock
from urllib.parse import unquote

async def fs_api_mocker(*args, **kwargs):
    """Mock the FamilySearch API by loading JSON responses from files offline.

    This mock is used as a side_effect for httpx.AsyncClient.get which is a bound
    method. When used as a side_effect, the first positional argument will be the
    AsyncClient instance (self) and the URL will usually be the next positional
    argument. To be robust we scan the args/kwargs for the URL string.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    request_url = _extract_url(args, kwargs)
    if request_url is None:
        return _create_empty_response()
    extracted_location = _extract_location(request_url)
    try:
        response_json_data = _load_json_response_file(extracted_location)
        mock_response.json = MagicMock(return_value=response_json_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return _create_empty_response()
    return mock_response


def _extract_url(args, kwargs):
    """Extract URL string from positional or keyword arguments."""
    for arg in args:
        if isinstance(arg, str) and (arg.startswith("http") or "q=name:" in arg):
            return arg
    for kwarg_key in ("url", "request", "uri"):
        candidate_value = kwargs.get(kwarg_key)
        if isinstance(candidate_value, str) and (candidate_value.startswith("http") or "q=name:" in candidate_value):
            return candidate_value
    return None

def _create_empty_response():
    """Create a 204 No Content response."""
    empty_mock_response = MagicMock()
    empty_mock_response.status_code = 204
    empty_mock_response.json = MagicMock(return_value={})
    return empty_mock_response

def _extract_location(url_string):
    """Extract location from URL query parameter and normalize it."""
    try:
        query_parameter_start = url_string.find('q=name:"')
        if query_parameter_start != -1:
            location_start_index = query_parameter_start + len('q=name:"')
            location_end_index = url_string.find('"', location_start_index)
            if location_end_index == -1:
                location = url_string[location_start_index:]
            else:
                location = url_string[location_start_index:location_end_index]
        else:
            location = url_string
        location = unquote(location)
        location = location.strip()
        for ch in ('*', '?', '/', '\\', ':', '|', '"', '<', '>'):
            location = location.replace(ch, "")
        location = location.replace("..", "")
        return location
    except Exception:
        return ""

def _load_json_response_file(location):
    """Load JSON response file for the given location."""
    response_directory = os.path.join(os.path.dirname(__file__), "expected_API_call_responses")
    response_file_path = os.path.join(response_directory, f"{location}.json")
    with open(response_file_path, "r", encoding="utf-8") as response_file:
        return json.load(response_file)
