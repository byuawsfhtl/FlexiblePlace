from unittest.mock import MagicMock
import json
import os

def fs_api_mocker(url: str, *args, **kwargs) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    location = url.split('q=name:"')[1].rstrip('"').replace("*","").replace("?","")
    try:
        base_dir = os.path.join(os.path.dirname(__file__), "expected_API_call_responses")
        file_path = os.path.join(base_dir, f"{location}.json")
        with open(file_path, "r", encoding="utf-8") as expected:
            mock_resp.json.return_value = json.load(expected)
    except (FileNotFoundError, json.JSONDecodeError):
        mock_resp.status_code = 204
        mock_resp.json.return_value = {}

    return mock_resp

