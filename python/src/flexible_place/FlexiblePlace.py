class FlexiblePlace:
    def __init__(self, location: str | list):
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location = [location_component.strip().lower() for location_component in location_components]


    #Needs work to be able to output abreviations well (e.g. United States vs Usa, D.C. vs D.c)
    def __str__(self):
        return ", ".join(map(str.title, self.location))
    
    def __repr__(self):
        return f"FlexiblePlace({self.location})"
    
    def __eq__(self, other):
        if isinstance(other, FlexiblePlace):
            return self.location == other.location
        return False
    
    def __bool__(self):
        return bool(self.location)
    
    # @staticmethod
    # def combine_flexible_places(places: list) -> FlexiblePlace:
        # 


    
    
