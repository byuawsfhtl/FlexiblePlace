import httpx

async def get_place_description(location: str) -> str:
    """Given a location string, this function queries the FamilySearch API to retrieve the corresponding place description.
    Args:
        location (str): The location string to be queried.
    Returns:
        str: The place description retrieved from the API, or an empty string if the query fails or the score is below 95.0."""
    if not location or not location.strip():
        return ""
    
    location = location.strip()
    url: str = f'https://api.familysearch.org/platform/places/search?q=name:"{location}"'
    TIMEOUT = httpx.Timeout(
        connect=5,
        read=15,
        write=10,
        pool=5
    )
    try:        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=TIMEOUT)
    except httpx.TimeoutException:
        return ""
    except Exception:
        return ""
    
    if not response.status_code == 200:
        return ""
    
    try:
        response_dict: dict = response.json()
    except Exception:
        return ""
    
    if not response_dict.get('entries') or len(response_dict['entries']) == 0:
        return ""
    
    score: float = response_dict['entries'][0].get('score', 0)
    if score < 95.0:
        return ""
    
    place_description: str = response_dict['entries'][0].get('id', '')
    return place_description
