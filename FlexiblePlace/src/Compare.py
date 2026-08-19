from FlexiblePlace.src.LocationMatrix import LocationMatrix

def align(location_a: list[str], location_b: list[str]) -> list[list[str]]:
    location_matrix = LocationMatrix([location_a, location_b])
    return location_matrix.get_locations()