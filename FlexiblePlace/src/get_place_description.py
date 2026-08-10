import requests

def get_place_description(location: str) -> str:
    """Given a location string, this function queries the FamilySearch API to retrieve the corresponding place description.
    Args:
        location (str): The location string to be queried.
    Returns:
        str: The place description retrieved from the API, or an empty string if the query fails or the score is below 95.0."""
    if not location:
        return ""
    url: str = f'https://api.familysearch.org/platform/places/search?q=name:"{location}"'
    response: requests.models.Response = requests.get(url)
    if not response.status_code == 200:
        return ""
    response_dict: dict = response.json()
    score: float = response_dict['entries'][0]['score']
    if score < 95.0:
        return ""
    place_description: str = response_dict['entries'][0]['id']
    return place_description