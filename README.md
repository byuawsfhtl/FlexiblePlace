# FlexiblePlace

This package defines the FlexiblePlace object which primarily does two things: 
1. Compare two FlexiblePlace objects and calculate a score that represents the likelihood that the two locations are the same place (compareTwoPlaces).
2. Combine a list of FlexiblePlace objects into a single FlexiblePlace object that represents the closest match to all of the FlexiblePlace objects provided (combineFlexiblePlaces).

## Instantiation
The FlexiblePlace object is effectively a wrapper class of a string array. This object can be instantiated by providing either a string representation of a location (e.g. `'Walla Walla, Washington, United States'`), or a string array representation of a location (e.g. `['Walla Walla', 'Washington', 'United States']`)

## compareTwoPlaces
This function is used to calulate a score out of 100 that represents how likely two FlexiblePlace objects refer to the same location (e.g. A FlexiblePlace object containing `'Walla Walla, Washington, United States'` and another object containing `'Washington, United States'` would be a 100% match when compared). 

## combineFlexiblePlaces
This function is used to combine a list of FlexiblePlace objects to create a single FlexiblePlace object that represents the closest (and most specific) match of all the provided FlexiblePlace objects (e.g. `'Walla Walla, Washington, United States'`, `'Washington, United States'`, and `'Washington, Utah'` would be combined into `'Walla Walla, Washington, United States'`).