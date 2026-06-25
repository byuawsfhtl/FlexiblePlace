# FlexiblePlace

This package primarily does three things: 
1. Parse string to create a new FlexiblePlace object (createFlexiblePlace). 
2. Compare two FlexiblePlace objects and calculate a score that represents the likelihood that the two locations are the same place (compareTwoPlaces).
3. Combine a list of FlexiblePlace objects into a single FlexiblePlace object that represents the closest match to all of the FlexiblePlace objects provided (combineFlexiblePlaces).

## createFlexiblePlace
This function is used parse strings for address information, then create a FlexiblePlace object from that information.

More specifically, it will determine the country, state/providence, city, street address and unit number. Any attributes that are not found are set to `None`.

## compareTwoPlaces
This function is used to calulate a score out of 100 that represents how likely two FlexiblePlace objects refer to the same location. 

This number is calulated by measuring the quantity of values that match, and also the physical distance between the places.

## combineFlexiblePlaces
This function is used to combine a list of FlexiblePlace objects to create a single FlexiblePlace object that represents the closest (and most specific) match of all the provided FlexiblePlace objects.