import requests

def get_place_description(location: str) -> str:
    if not location:
        return ""
    escaped_location: str = location.replace("?",r"\?").replace("*",r"\*")
    url: str = f'https://apibeta.familysearch.org/platform/places/search?q=name:"{escaped_location}"'
    response: requests.models.Response = requests.get(url)
    if not response.ok:
        return ""
    response_dict: dict = response.json()
    score: float = response_dict['entries'][0]['score']
    if score < 95.0:
        return ""
    place_description: str = response_dict['entries'][0]['id']
    return place_description