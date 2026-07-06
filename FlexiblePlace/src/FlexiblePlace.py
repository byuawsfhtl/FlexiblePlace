class FlexiblePlace:
    def __init__(self, location: str | list[str]):
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location: list[str] = [location_component.strip().lower() for location_component in location_components]


    #Needs work to be able to output abreviations well (e.g. United States vs Usa, D.C. vs D.c)
    def __str__(self):
        return ", ".join(map(str.title, self.location))
    
    def __repr__(self):
        return f"FlexiblePlace({self.location})"
    
    def __eq__(self, other: object):
        if isinstance(other, FlexiblePlace):
            return self.location == other.location
        return False
    
    def __bool__(self):
        return bool(self.location)
    
    def compare(self, other: object) -> float | int:
        return compare_places(self, other)
    
    
@staticmethod
def combine_flexible_places(places: list[FlexiblePlace]) -> FlexiblePlace:
    # aligned_places: LocationMatrix = align_places(places)
    # combined_place: list[str] = generate_combined_place_format(aligned_places)
    # while true:
        # empty_indeces: list[int] = find_empty_indeces(combined_place)
        # for index in empty_indeces:
            # remove_outliers(aligned_places, index)
            # add_place_component(aligned_places, combined_place, index)
        # if nothing_has_changed:
            # if isFull(combined_place):
                # break
            # elif isEmpty(aligned_places):
                # resize_combined_place(combined_place)
                # break
            # else:
                # eliminate_partial_rows(aligned_places)
    # return FlexiblePlace(combined_place)
    return FlexiblePlace("place holder")

# def align_places(places: list[FlexiblePlace]) -> LocationMatrix:
    # aligned_places: LocationMatrix = LocationMatrix()
    # aligned_places.load_places(places)
    # aligned_places.align()
    # return aligned_places

# def align():
    ## This should actually be inside of the LocationMatrix class, but I don't want to make that class yet.
    # for row: int, location: list[str]  in enumerate(self.locations):
        # for column: int, component: str in enumerate(location):
            # match: tuple[int, int] = compare_with_previous(row, component) #this is where the customization will go down
            # link(row, column, match) #this is where moving then linking will happen

@staticmethod
def compare_places(place1: FlexiblePlace, place2: FlexiblePlace) -> int:
    """Compares two FlexiblePlace objects and returns a similarity score out of 100. Assumes that places
    are given in a standardized order, with no missing components (Street address, City, State/Province, Country).
    Note: 
     - All address components will be compared (e.g Paris, Tx and Paris, Fl will score higher than Tx and Fl)
     - More specific address components will be weighted lower than less specific ones (countries are weighted heavier than cities)
    
    Args:
        place1 (FlexiblePlace): The first FlexiblePlace object to compare.
        place2 (FlexiblePlace): The second FlexiblePlace object to compare.
    Returns:
        float | int: The similarity score out of 100.
    """


    return 100
