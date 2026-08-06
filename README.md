# FlexiblePlace
This package defines the FlexiblePlace object, which primarily does two things: 
1. Compare two FlexiblePlace objects and calculate a score that represents the likelihood that the two locations are the same place (`compare_places`).
2. Combine a list of FlexiblePlace objects into a single FlexiblePlace object that represents the closest match to all of the FlexiblePlace objects provided (`combine_flexible_places`).

## Initialization
The FlexiblePlace object is effectively a wrapper class of a string array. This object can be instantiated by providing either a string representation of a location (e.g. `'Walla Walla, Washington, United States'`), or a string array representation of a location (e.g. `['Walla Walla', 'Washington', 'United States']`). The Python version of this class also has the ability to lookup and add the FamilySearch "place description" (effectively an ID associated with a singular geographical location the FamilySearch database).
```python
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

fp1 = FlexiblePlace("Walla Walla, Washington, United States")
print(fp1) # Walla Walla, Washington, United States

fp2 = FlexiblePlace(["Walla Walla", "Washington", "United States"])
print(fp2) # Walla Walla, Washington, United States

print(fp1 == fp2) # True

online_fp = FlexiblePlace("Walla Walla, Washington, United States", online = True)
print(online_fp.place_description) # 396089
print(fp1.place_description) # 
```

## compare_places
This static method is used to calulate a score out of 100 that represents how likely two FlexiblePlace objects refer to the same location. Locations of differing specificity, but with otherwise aggreeing information, are a 100% match.
```python
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace
compare_places = FlexiblePlace.compare_places

walla_walla = FlexiblePlace("Walla Walla, Washington, United States")
washington = FlexiblePlace("Washington, United States")
united_states = FlexiblePlace("United States")

print(compare_places(walla_walla, washington)) # 100.0

print(washington.compare(united_states)) # 100.0
```

## combine_flexible_places
This static method is used to combine a list of FlexiblePlace objects to create a single FlexiblePlace object that represents the closest (and most specific) match of all the provided FlexiblePlace objects. The Python version of this method has the ability to lookup and add the FamilySearch "place description"
```python
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace
combine_flexible_places = FlexiblePlace.combine_flexible_places

walla_walla = FlexiblePlace("Walla Walla, Washington")
washington = FlexiblePlace("Washington, United States")
united_states = FlexiblePlace("United States")
dc = FlexiblePlace("Washington, D.C.")

combined_place = combined_flexible_places([walla_walla, washington, united_states, dc])
print(combined_place) # Walla Walla, Washington, United States

online_combined_place = combined_flexible_places([walla_walla, washington, united_states, dc], online = True)
print(online_combined_place.place_description) # 396089
```