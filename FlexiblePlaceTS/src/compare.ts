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
		const componentCount = Math.min(locationA.length, locationB.length);
		return Array.from({ length: componentCount }, (_, index) =>
			Compare._compareComponents(locationA[index], locationB[index])
		);
	}

	/**Calculates the fuzzy similarity ratio between two string components.
	 * 
	 * @param componentA - The first component string.
	 * @param componentB - The second component string.
	 * 
	 * @returns - Similarity score from 0.0 to 100.0. Returns -1 if either component is empty.
	 */
	private static _compareComponents = memoize(
		(componentA: string, componentB: string): number=>{
			if(!componentA || !componentB){
				return -1
			}
			return Math.floor(fuzzball_ratio(componentA, componentB) + 0.5)
		}, 
	{max:1000});

	/**Adjusts similarity scores in place based on component specificity.
	 *
	 * A -1 score marks a missing component and is preserved without penalty.
	 *
	 * @param scoresList - Component fuzzy scores ordered from least to most specific.
	 */
	static adjustScores(scoresList: Array<number>): void{
		for(let index = 0; index < scoresList.length; index++){
			const scoreIndex = scoresList.length - index - 1;
			scoresList[scoreIndex] = Compare._forgiveSmallDifferences(scoresList[scoreIndex], index);
		}
	}

	/**Forgives more of the score difference for more specific components.
	 *
	 * @param score - The component score.
	 * @param index - The component's index when scores are read in reverse order.
	 * @returns The adjusted score, or -1 for a missing component.
	 */
	private static _forgiveSmallDifferences(score: number, index: number): number{
		if(score === -1){
			return -1;
		}
		const componentPenalty = 0.5;
		const forgivenessFactor = 1 - 2 ** -(index * componentPenalty);
		const redeemedPoints = (100 - score) * forgivenessFactor;
		return score + redeemedPoints;
	}

	/**Calculates the average while ignoring scores for missing components.
	 *
	 * @param scoresList - Scores to average; negative scores are ignored.
	 * @returns The average of the nonnegative scores, or 100.0 if none remain.
	 */
	static getAverage(scoresList: Array<number>): number{
		const validScores = scoresList.filter(score => score >= 0);
		if(validScores.length === 0){
			return 100.0;
		}
		return validScores.reduce((sum, score) => sum + score, 0) / validScores.length;
	}
}
