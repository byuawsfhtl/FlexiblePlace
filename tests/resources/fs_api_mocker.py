import json
import os
from unittest.mock import AsyncMock
from urllib.parse import unquote


async def fs_api_mocker(*args, **kwargs):
    """Mock the FamilySearch API by loading JSON responses from files offline.

    This mock is used as a side_effect for httpx.AsyncClient.get which is a bound
    method. When used as a side_effect, the first positional argument will be the
    AsyncClient instance (self) and the URL will usually be the next positional
    argument. To be robust we scan the args/kwargs for the URL string.
    """
    mock_resp = AsyncMock()
    mock_resp.status_code = 200

    # Find the URL argument (it may be the first or second positional arg,
    # or supplied as a kwarg). We look for something that looks like a URL or
    # contains the q=name: query used by the code under test.
    url = None
    for a in args:
        if isinstance(a, str) and (a.startswith("http") or "q=name:" in a):
            url = a
            break

    if url is None:
        # Common kwarg names to check
        for key in ("url", "request", "uri"):
            candidate = kwargs.get(key)
            if isinstance(candidate, str) and (candidate.startswith("http") or "q=name:" in candidate):
                url = candidate
                break

    if url is None:
        # nothing useful found; return a 204-like empty response
        mock_resp.status_code = 204
        mock_resp.json = AsyncMock(return_value={})
        return mock_resp

    # Extract location from URL query parameter safely.
    try:
        idx = url.find('q=name:"')
        if idx != -1:
            start = idx + len('q=name:"')
            end = url.find('"', start)
            if end == -1:
                location = url[start:]
            else:
                location = url[start:end]
        else:
            # If the URL isn't the expected search form, try to treat the whole
            # URL (or trailing part) as the location.
            # Strip protocol and path if present.
            # Fallback to the entire url string if nothing else works.
            location = url

        # Decode percent-encoding and remove wildcard/placeholder characters
        location = unquote(location)
        location = location.strip().replace("*", "").replace("?", "")
    except Exception:
        location = ""

    try:
        base_dir = os.path.join(os.path.dirname(__file__), "expected_API_call_responses")
        file_path = os.path.join(base_dir, f"{location}.json")
        with open(file_path, "r", encoding="utf-8") as expected:
            mock_resp.json = AsyncMock(return_value=json.load(expected))
    except (FileNotFoundError, json.JSONDecodeError):
        mock_resp.status_code = 204
        mock_resp.json = AsyncMock(return_value={})

    return mock_resp
