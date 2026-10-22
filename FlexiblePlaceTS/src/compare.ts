import { ratio as fuzzball_ratio } from "fuzzball";
import memoize from "memoizee";
import { Aligner } from "./aligner";

/**
 * Provides component-level string comparison and alignment utilities for location comparison.
 * Helper class containing methods to align location component lists, calculate component
 * similarity scores, and adjust comparison scores based on component specificity.
 */
export class Compare{
	/**Aligns two lists of strings representing locations.
	 * 
	 * Relies heavily on the built-in component alignment functionality of the Aligner class.
	 * 
	 * @param locationA - First list of location component strings.
	 * @param locationB - Second list of location component strings.
	 * 
	 * @returns A list containing the two aligned location component lists.
	 */
	static alignComponents(locationA: Array<string>, locationB: Array<string>): Array<Array<string>>{
		const aligner = new Aligner([locationA,locationB])
		return aligner.getLocations();
	}

	/**Compares corresponding components of two aligned location lists.
	 * 
	 * A missing component is represented by -1 rather than removed, preserving
	 * component order and spacing. This sentinel is ignored during score
	 * adjustment and does not penalize the comparison.
	 * 
	 * @param locations - A list containing two equal-length location component lists.
	 * 
	 * @returns - Similarity scores from 0.0 to 100.0; -1 marks a missing component.
	 */
	static compareEachComponent(locations: Array<Array<string>>): Array<number>{
		const locationA = locations[0];
		const locationB = locations[1];
	}

	/**Calculates the fuzzy similarity ratio between two string components.
	 * 
	 * @param componentA - The first component string.
	 * @param comopnentB - The second component string.
	 * 
	 * @returns - Similarity score from 0.0 to 100.0. Returns -1 if either component is empty.
	 */
	private static _compare_components = memoize(
		(componentA: string, componentB: string): number=>{
			if(!componentA || !componentB){
				return -1
			}
			return fuzzball_ratio(componentA, componentB) + 0.5
		}, 
	{max:1000});
}
