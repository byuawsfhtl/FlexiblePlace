us_states: set[str] = set(["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia", "wisconsin", "wyoming"])

def auto_fill_location(location: list[str]) -> None:
    """Given incomplete initial location information, additional information will be assumed.
    At this point this function only checks for US states and adds 'United States' to the string
    if it is missing.
    
    Args:
        location (list[str]): The location (ordered from least to most specific).
    Returns:
        None."""
    if location and location[-1] in us_states:
        location.append("united states")