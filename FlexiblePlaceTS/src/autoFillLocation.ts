const usStates: Set<String> = new Set(["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia", "wisconsin", "wyoming"])

/*
 * Given incomplete initial location information, additional information will be assumed. 
 * At this point this function only checks for US states and adds 'United States' to the 
 * string if it is missing.
 *
 * @param location - The location (ordered from least to most specific).
 */ 
function autoFillLocation(location: Array<String>): void{
    if (location.length > 0 && usStates.has(location[0])){
        location.unshift("united states");
    };
};