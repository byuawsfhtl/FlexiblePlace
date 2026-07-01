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
    
    